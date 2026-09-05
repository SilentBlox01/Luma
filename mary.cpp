/*
 * ==============================================================================
 *  Luma - Mary 3.0 Apex Engine (C++17 Native)
 * ==============================================================================
 *  Perceptual Visual Computing & Computational Optics Super-Model for Terminals.
 *  Zero AI / Zero Neural Networks. Pure human biophysical vision mathematics:
 *   - Fast Guided Image Filter in Oklab Space (O(1) time per pixel)
 *   - Weber-Fechner Contrast Sensitivity Adaptive Thresholding
 *   - Oklab ΔE Perceptual Chromatic Distance
 *   - Subpixel K-Means Dual-Cluster Centroids with Minority-Cluster FG
 *   - Unicode 13.0 Sextants HD (2x3 Subpixels, 64 Glyphs, 100% Solid Blocks)
 *   - Braille Dual-Color Hybrid (2x4 Subpixels)
 *   - Quadrants HD (2x2 Subpixels)
 *   - Directional Scharr Gradient ASCII
 *   - Multi-Core OpenMP Row-Parallel Pipeline & Vectorized Loops
 *   - Zero-Latency ANSI Stream Compressor
 * ==============================================================================
 */

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

#define STB_IMAGE_RESIZE_IMPLEMENTATION
#include "stb_image_resize2.h"

#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>
#include <sstream>
#include <cstring>
#include <sys/ioctl.h>
#include <unistd.h>

#ifdef _OPENMP
#include <omp.h>
#endif

// ==============================================================================
// 1. ESPACIO DE COLOR PERCEPTUAL OKLAB Y TABLAS LUT
// ==============================================================================

struct Oklab {
    float L, a, b;
};

struct RGB {
    uint8_t r, g, b;
};

static float sRGB_to_Linear_LUT[256];
static bool g_lut_initialized = false;

static void init_oklab_luts() {
    if (g_lut_initialized) return;
    for (int i = 0; i < 256; ++i) {
        float v = i / 255.0f;
        sRGB_to_Linear_LUT[i] = (v <= 0.04045f) ? (v / 12.92f) : std::pow((v + 0.055f) / 1.055f, 2.4f);
    }
    g_lut_initialized = true;
}

inline uint8_t linear_to_srgb(float c) {
    if (c <= 0.0031308f) {
        float val = c * 12.92f;
        return (uint8_t)std::max(0.0f, std::min(255.0f, std::round(val * 255.0f)));
    } else {
        float val = 1.055f * std::pow(std::max(0.0f, c), 1.0f / 2.4f) - 0.055f;
        return (uint8_t)std::max(0.0f, std::min(255.0f, std::round(val * 255.0f)));
    }
}

inline Oklab rgb_to_oklab(uint8_t r, uint8_t g, uint8_t b) {
    float r_l = sRGB_to_Linear_LUT[r];
    float g_l = sRGB_to_Linear_LUT[g];
    float b_l = sRGB_to_Linear_LUT[b];

    float l = 0.4122214708f * r_l + 0.5363325363f * g_l + 0.0514459929f * b_l;
    float m = 0.2119034982f * r_l + 0.6883090962f * g_l + 0.0997874057f * b_l;
    float s = 0.0883024619f * r_l + 0.2817188376f * g_l + 0.6299787005f * b_l;

    float l_ = (l > 0.0f) ? std::cbrt(l) : 0.0f;
    float m_ = (m > 0.0f) ? std::cbrt(m) : 0.0f;
    float s_ = (s > 0.0f) ? std::cbrt(s) : 0.0f;

    return {
        0.2104542553f * l_ + 0.7936177850f * m_ - 0.0040720468f * s_,
        1.9779984951f * l_ - 2.4285922050f * m_ + 0.4505937099f * s_,
        0.0259040371f * l_ + 0.7827717662f * m_ - 0.8086757660f * s_
    };
}

inline RGB oklab_to_rgb(float L, float a, float b) {
    float l_ = L + 0.3963377774f * a + 0.2158037573f * b;
    float m_ = L - 0.1055613458f * a - 0.0638541728f * b;
    float s_ = L - 0.0894841775f * a - 1.2914855480f * b;

    float l = (l_ > 0.0f) ? (l_ * l_ * l_) : 0.0f;
    float m = (m_ > 0.0f) ? (m_ * m_ * m_) : 0.0f;
    float s = (s_ > 0.0f) ? (s_ * s_ * s_) : 0.0f;

    float r_l = +4.0767416621f * l - 3.3077115913f * m + 0.2309699292f * s;
    float g_l = -1.2684380046f * l + 2.6097574011f * m - 0.3413193965f * s;
    float b_l = -0.0041960863f * l - 0.7034186147f * m + 1.7076147010f * s;

    return { linear_to_srgb(r_l), linear_to_srgb(g_l), linear_to_srgb(b_l) };
}

inline float oklab_dist_sq(const Oklab& c1, const Oklab& c2) {
    float dL = c1.L - c2.L;
    float da = c1.a - c2.a;
    float db = c1.b - c2.b;
    return 1.25f * (dL * dL) + (da * da) + (db * db);
}

// ==============================================================================
// 2. FILTRO GUIADO ULTRA-RÁPIDO EN ESPACIO OKLAB (O(1) POR PÍXEL)
// ==============================================================================

static void box_filter_2d(const std::vector<float>& src, std::vector<float>& dst, int w, int h, int r) {
    std::vector<float> temp(w * h);

    // Horizontal pass
    for (int y = 0; y < h; ++y) {
        const float* row_src = &src[y * w];
        float* row_temp = &temp[y * w];
        float acc = 0.0f;
        for (int x = 0; x <= std::min(r, w - 1); ++x) acc += row_src[x];
        for (int x = 0; x < w; ++x) {
            int x_add = x + r;
            int x_sub = x - r - 1;
            if (x > 0) {
                if (x_add < w) acc += row_src[x_add];
                if (x_sub >= 0) acc -= row_src[x_sub];
            }
            int x0 = std::max(0, x - r);
            int x1 = std::min(w - 1, x + r);
            row_temp[x] = acc / (float)(x1 - x0 + 1);
        }
    }

    // Vertical pass
    for (int x = 0; x < w; ++x) {
        float acc = 0.0f;
        for (int y = 0; y <= std::min(r, h - 1); ++y) acc += temp[y * w + x];
        for (int y = 0; y < h; ++y) {
            int y_add = y + r;
            int y_sub = y - r - 1;
            if (y > 0) {
                if (y_add < h) acc += temp[y_add * w + x];
                if (y_sub >= 0) acc -= temp[y_sub * w + x];
            }
            int y0 = std::max(0, y - r);
            int y1 = std::min(h - 1, y + r);
            dst[y * w + x] = acc / (float)(y1 - y0 + 1);
        }
    }
}

static void apply_oklab_guided_filter(std::vector<uint8_t>& img_rgba, int w, int h, int r = 2, float eps = 0.0004f) {
    int total = w * h;
    std::vector<float> L(total), a_ch(total), b_ch(total);

    #pragma omp parallel for
    for (int i = 0; i < total; ++i) {
        Oklab ok = rgb_to_oklab(img_rgba[i * 4 + 0], img_rgba[i * 4 + 1], img_rgba[i * 4 + 2]);
        L[i] = ok.L;
        a_ch[i] = ok.a;
        b_ch[i] = ok.b;
    }

    // Filtrado guiado en canal de Luminosidad L (guía I = L)
    std::vector<float> mean_I(total);
    box_filter_2d(L, mean_I, w, h, r);

    std::vector<float> II(total);
    for (int i = 0; i < total; ++i) II[i] = L[i] * L[i];

    std::vector<float> corr_I(total);
    box_filter_2d(II, corr_I, w, h, r);

    std::vector<float> a_coeff(total), b_coeff(total);
    for (int i = 0; i < total; ++i) {
        float var_I = std::max(0.0f, corr_I[i] - mean_I[i] * mean_I[i]);
        float ak = var_I / (var_I + eps);
        float bk = (1.0f - ak) * mean_I[i];
        a_coeff[i] = ak;
        b_coeff[i] = bk;
    }

    std::vector<float> mean_a(total), mean_b(total);
    box_filter_2d(a_coeff, mean_a, w, h, r);
    box_filter_2d(b_coeff, mean_b, w, h, r);

    #pragma omp parallel for
    for (int i = 0; i < total; ++i) {
        float q_L = mean_a[i] * L[i] + mean_b[i];
        float detail = L[i] - q_L;
        // Realce de micro-contraste en bordes
        float sharp_L = L[i] + 1.45f * detail;
        sharp_L = std::clamp(sharp_L, 0.0f, 1.0f);

        // Curva sigmoidal S-curve que aumenta contraste pero preserva blancos (1.0) y negros (0.0)
        float L_curved = sharp_L;
        if (sharp_L < 0.5f) {
            L_curved = 0.5f * std::pow(2.0f * sharp_L, 1.15f);
        } else {
            L_curved = 1.0f - 0.5f * std::pow(2.0f * (1.0f - sharp_L), 1.15f);
        }

        // Realce cromático biofísico (+25%) en espacio Oklab
        float new_a = a_ch[i] * 1.25f;
        float new_b = b_ch[i] * 1.25f;

        RGB rgb = oklab_to_rgb(L_curved, new_a, new_b);
        img_rgba[i * 4 + 0] = rgb.r;
        img_rgba[i * 4 + 1] = rgb.g;
        img_rgba[i * 4 + 2] = rgb.b;
    }
}

// ==============================================================================
// 3. CLUSTERING K-MEANS SUBPÍXEL Y LEY DE WEBER-FECHNER
// ==============================================================================

struct ClusterResult {
    RGB fg;
    RGB bg;
    std::vector<bool> mask; // true: fg, false: bg
    float max_delta_e;
    float mean_L;
};

static ClusterResult cluster_cell_oklab(const std::vector<RGB>& pixels) {
    int n = pixels.size();
    if (n == 0) return { {255,255,255}, {0,0,0}, {}, 0.0f, 0.5f };

    std::vector<Oklab> pts(n);
    float mean_L = 0.0f, mean_a = 0.0f, mean_b = 0.0f;
    for (int i = 0; i < n; ++i) {
        pts[i] = rgb_to_oklab(pixels[i].r, pixels[i].g, pixels[i].b);
        mean_L += pts[i].L;
        mean_a += pts[i].a;
        mean_b += pts[i].b;
    }
    mean_L /= n; mean_a /= n; mean_b /= n;

    // Primer centroide: punto más lejano de la media
    float max_d1 = -1.0f;
    int c1_idx = 0;
    for (int i = 0; i < n; ++i) {
        float d = (pts[i].L - mean_L)*(pts[i].L - mean_L) + (pts[i].a - mean_a)*(pts[i].a - mean_a) + (pts[i].b - mean_b)*(pts[i].b - mean_b);
        if (d > max_d1) { max_d1 = d; c1_idx = i; }
    }
    Oklab c1 = pts[c1_idx];

    // Segundo centroide: punto más lejano de c1
    float max_d2 = -1.0f;
    int c2_idx = 0;
    for (int i = 0; i < n; ++i) {
        float d = oklab_dist_sq(pts[i], c1);
        if (d > max_d2) { max_d2 = d; c2_idx = i; }
    }
    Oklab c2 = pts[c2_idx];

    // 2 iteraciones de refinamiento K-Means rápido
    for (int it = 0; it < 2; ++it) {
        float g1_L = 0, g1_a = 0, g1_b = 0; int cnt1 = 0;
        float g2_L = 0, g2_a = 0, g2_b = 0; int cnt2 = 0;
        for (int i = 0; i < n; ++i) {
            if (oklab_dist_sq(pts[i], c1) <= oklab_dist_sq(pts[i], c2)) {
                g1_L += pts[i].L; g1_a += pts[i].a; g1_b += pts[i].b; cnt1++;
            } else {
                g2_L += pts[i].L; g2_a += pts[i].a; g2_b += pts[i].b; cnt2++;
            }
        }
        if (cnt1 > 0) c1 = { g1_L / cnt1, g1_a / cnt1, g1_b / cnt1 };
        if (cnt2 > 0) c2 = { g2_L / cnt2, g2_a / cnt2, g2_b / cnt2 };
    }

    // Asegurar que c1 sea el más luminoso
    if (c1.L < c2.L) std::swap(c1, c2);

    std::vector<bool> mask(n);
    for (int i = 0; i < n; ++i) {
        mask[i] = (oklab_dist_sq(pts[i], c1) <= oklab_dist_sq(pts[i], c2));
    }

    return { oklab_to_rgb(c1.L, c1.a, c1.b), oklab_to_rgb(c2.L, c2.a, c2.b), mask, max_d2, mean_L };
}

// ==============================================================================
// 4. COMPRESOR DE SECUENCIAS ANSI DE CERO LATENCIA
// ==============================================================================

class AnsiBuffer {
private:
    std::string stream;
    int cur_fg_r = -1, cur_fg_g = -1, cur_fg_b = -1;
    int cur_bg_r = -1, cur_bg_g = -1, cur_bg_b = -1;

public:
    void emit_cell(const std::string& glyph, const RGB* fg = nullptr, const RGB* bg = nullptr) {
        if (fg) {
            if (fg->r != cur_fg_r || fg->g != cur_fg_g || fg->b != cur_fg_b) {
                stream += "\033[38;2;" + std::to_string(fg->r) + ";" + std::to_string(fg->g) + ";" + std::to_string(fg->b) + "m";
                cur_fg_r = fg->r; cur_fg_g = fg->g; cur_fg_b = fg->b;
            }
        } else {
            if (cur_fg_r != -1) {
                stream += "\033[39m";
                cur_fg_r = cur_fg_g = cur_fg_b = -1;
            }
        }
        if (bg) {
            if (bg->r != cur_bg_r || bg->g != cur_bg_g || bg->b != cur_bg_b) {
                stream += "\033[48;2;" + std::to_string(bg->r) + ";" + std::to_string(bg->g) + ";" + std::to_string(bg->b) + "m";
                cur_bg_r = bg->r; cur_bg_g = bg->g; cur_bg_b = bg->b;
            }
        } else {
            if (cur_bg_r != -1) {
                stream += "\033[49m";
                cur_bg_r = cur_bg_g = cur_bg_b = -1;
            }
        }
        stream += glyph;
    }

    void end_line() {
        if (cur_fg_r != -1 || cur_bg_r != -1) {
            stream += "\033[0m";
            cur_fg_r = cur_fg_g = cur_fg_b = -1;
            cur_bg_r = cur_bg_g = cur_bg_b = -1;
        }
        stream += "\n";
    }

    std::string str() const {
        return stream;
    }
};

// ==============================================================================
// 5. TABLAS DE MAPAS UNICODE (BRAILLE, SEXTANTES, CUADRANTES)
// ==============================================================================

static const int BRAILLE_DOTS[4][2] = {
    { 0x01, 0x08 },
    { 0x02, 0x10 },
    { 0x04, 0x20 },
    { 0x40, 0x80 }
};

static const char* QUADRANTS[16] = {
    " ", "▘", "▝", "▀",
    "▖", "▌", "▞", "▛",
    "▗", "▚", "▐", "▜",
    "▄", "▙", "▟", "█"
};

static const char* SEXTANTS[64] = {
    " ", "🬀", "🬁", "🬂", "🬃", "🬄", "🬅", "🬆",
    "🬇", "🬈", "🬉", "🬊", "🬋", "🬌", "🬍", "🬎",
    "🬏", "🬐", "🬑", "🬒", "🬓", "▌", "🬔", "🬕",
    "🬖", "🬗", "🬘", "🬙", "🬚", "🬛", "🬜", "🬝",
    "🬞", "🬟", "🬠", "🬡", "🬢", "🬣", "🬤", "🬥",
    "🬦", "🬧", "▐", "🬨", "🬩", "🬪", "🬫", "🬬",
    "🬭", "🬮", "🬯", "🬰", "🬱", "🬲", "🬳", "🬴",
    "🬵", "🬶", "🬷", "🬸", "🬹", "🬺", "🬻", "█"
};

// ==============================================================================
// 6. PIPELINE APEX CON PARALELIZACIÓN MULTI-NÚCLEO MARY 3.0
// ==============================================================================

std::string render_mary_pipeline(const std::string& image_path, int target_w, const std::string& mode, bool raw_colors, bool invert, float font_ratio = 0.5f) {
    init_oklab_luts();

    int orig_w = 0, orig_h = 0, channels = 0;
    unsigned char* raw_data = stbi_load(image_path.c_str(), &orig_w, &orig_h, &channels, 4);
    if (!raw_data) {
        return "❌ Error: Could not load image " + image_path;
    }

    float aspect = (float)orig_h / (float)orig_w;

    // -------------------------------------------------------------
    // MODO A: SEXTANTES HD 2x3 (Unicode 13.0, 6 Subpíxeles, Bloques 100% Sólidos)
    // -------------------------------------------------------------
    if (mode == "sextants" || mode == "sextant" || mode == "s") {
        int sub_w = target_w * 2;
        int num_rows = (int)std::round(target_w * aspect * font_ratio);
        int sub_h = num_rows * 3;

        std::vector<uint8_t> scaled(sub_w * sub_h * 4);
        stbir_resize_uint8_linear(raw_data, orig_w, orig_h, 0, scaled.data(), sub_w, sub_h, 0, STBIR_RGBA);
        stbi_image_free(raw_data);

        if (!raw_colors) {
            apply_oklab_guided_filter(scaled, sub_w, sub_h, 2, 0.0004f);
        }

        std::vector<std::string> row_strings(num_rows);

        #pragma omp parallel for schedule(dynamic, 4)
        for (int row_idx = 0; row_idx < num_rows; ++row_idx) {
            int y = row_idx * 3;
            AnsiBuffer row_buf;

            for (int x = 0; x < sub_w; x += 2) {
                std::vector<RGB> cell_p(6);
                std::vector<uint8_t> cell_a(6);

                for (int dy = 0; dy < 3; ++dy) {
                    for (int dx = 0; dx < 2; ++dx) {
                        int cx = x + dx;
                        int cy = y + dy;
                        int idx = dy * 2 + dx;
                        if (cx < sub_w && cy < sub_h) {
                            int p_idx = (cy * sub_w + cx) * 4;
                            cell_p[idx] = { scaled[p_idx + 0], scaled[p_idx + 1], scaled[p_idx + 2] };
                            cell_a[idx] = scaled[p_idx + 3];
                        } else {
                            cell_p[idx] = { 0, 0, 0 };
                            cell_a[idx] = 0;
                        }
                    }
                }

                bool all_trans = true;
                for (uint8_t a : cell_a) if (a >= 64) { all_trans = false; break; }
                if (all_trans) {
                    row_buf.emit_cell(" ");
                    continue;
                }

                ClusterResult cr = cluster_cell_oklab(cell_p);

                // Umbral adaptativo Weber-Fechner dependiente de la luminosidad local
                float tau = 0.0075f * std::pow((cr.mean_L + 0.08f) / 0.58f, 0.80f);

                if (cr.max_delta_e < tau) {
                    // Superficie lisa o fondo uniforme: emisión limpia sin glifos parásitos
                    row_buf.emit_cell(" ", nullptr, &cr.bg);
                } else {
                    // Alto contraste (bordes de dibujo, ojos, pelo) -> Sextantes HD 2x3
                    int cnt_true = 0;
                    for (bool m : cr.mask) if (m) cnt_true++;
                    if (cnt_true > 3) {
                        std::swap(cr.fg, cr.bg);
                        for (int i = 0; i < 6; ++i) cr.mask[i] = !cr.mask[i];
                    }

                    int sextant_code = 0;
                    for (int i = 0; i < 6; ++i) {
                        if (cell_a[i] >= 64 && (cr.mask[i] != invert)) {
                            sextant_code |= (1 << i);
                        }
                    }

                    if (sextant_code == 0) {
                        row_buf.emit_cell(" ", nullptr, &cr.bg);
                    } else if (sextant_code == 63) {
                        row_buf.emit_cell(" ", nullptr, &cr.fg);
                    } else {
                        row_buf.emit_cell(SEXTANTS[sextant_code], &cr.fg, &cr.bg);
                    }
                }
            }
            row_buf.end_line();
            row_strings[row_idx] = row_buf.str();
        }

        std::string total;
        size_t total_sz = 0;
        for (const auto& s : row_strings) total_sz += s.size();
        total.reserve(total_sz);
        for (const auto& s : row_strings) total += s;
        return total;
    }
    // -------------------------------------------------------------
    // MODO B: BRAILLE SUPER-HYBRID (Bordes finos 2x4 + Superficies sólidas)
    // -------------------------------------------------------------
    else if (mode == "braille" || mode == "hybrid" || mode == "super" || mode == "b") {
        int sub_w = target_w * 2;
        int num_rows = (int)std::round(target_w * aspect * font_ratio);
        int sub_h = num_rows * 4;

        std::vector<uint8_t> scaled(sub_w * sub_h * 4);
        stbir_resize_uint8_linear(raw_data, orig_w, orig_h, 0, scaled.data(), sub_w, sub_h, 0, STBIR_RGBA);
        stbi_image_free(raw_data);

        if (!raw_colors) {
            apply_oklab_guided_filter(scaled, sub_w, sub_h, 2, 0.0004f);
        }

        std::vector<std::string> row_strings(num_rows);

        #pragma omp parallel for schedule(dynamic, 4)
        for (int row_idx = 0; row_idx < num_rows; ++row_idx) {
            int y = row_idx * 4;
            AnsiBuffer row_buf;

            for (int x = 0; x < sub_w; x += 2) {
                std::vector<RGB> cell_p(8);
                std::vector<uint8_t> cell_a(8);

                for (int dy = 0; dy < 4; ++dy) {
                    for (int dx = 0; dx < 2; ++dx) {
                        int cx = x + dx;
                        int cy = y + dy;
                        int idx = dy * 2 + dx;
                        if (cx < sub_w && cy < sub_h) {
                            int p_idx = (cy * sub_w + cx) * 4;
                            cell_p[idx] = { scaled[p_idx + 0], scaled[p_idx + 1], scaled[p_idx + 2] };
                            cell_a[idx] = scaled[p_idx + 3];
                        } else {
                            cell_p[idx] = { 0, 0, 0 };
                            cell_a[idx] = 0;
                        }
                    }
                }

                bool all_trans = true;
                for (uint8_t a : cell_a) if (a >= 64) { all_trans = false; break; }
                if (all_trans) {
                    row_buf.emit_cell(" ");
                    continue;
                }

                ClusterResult cr = cluster_cell_oklab(cell_p);

                // Umbral adaptativo Weber-Fechner
                float tau = 0.0075f * std::pow((cr.mean_L + 0.08f) / 0.58f, 0.80f);

                if (cr.max_delta_e < tau) {
                    row_buf.emit_cell(" ", nullptr, &cr.bg);
                } else {
                    int cnt_true = 0;
                    for (bool m : cr.mask) if (m) cnt_true++;
                    if (cnt_true > 4) {
                        std::swap(cr.fg, cr.bg);
                        for (int i = 0; i < 8; ++i) cr.mask[i] = !cr.mask[i];
                    }

                    int braille_code = 0;
                    for (int dy = 0; dy < 4; ++dy) {
                        for (int dx = 0; dx < 2; ++dx) {
                            int idx = dy * 2 + dx;
                            if (cell_a[idx] >= 64) {
                                bool is_on = cr.mask[idx] != invert;
                                if (is_on) braille_code |= BRAILLE_DOTS[dy][dx];
                            }
                        }
                    }

                    if (braille_code == 0) {
                        row_buf.emit_cell(" ", nullptr, &cr.bg);
                    } else if (braille_code == 0xFF) {
                        row_buf.emit_cell(" ", nullptr, &cr.fg);
                    } else {
                        uint32_t cp = 0x2800 + braille_code;
                        std::string glyph;
                        glyph += (char)(0xE0 | ((cp >> 12) & 0x0F));
                        glyph += (char)(0x80 | ((cp >> 6) & 0x3F));
                        glyph += (char)(0x80 | (cp & 0x3F));
                        row_buf.emit_cell(glyph, &cr.fg, &cr.bg);
                    }
                }
            }
            row_buf.end_line();
            row_strings[row_idx] = row_buf.str();
        }

        std::string total;
        size_t total_sz = 0;
        for (const auto& s : row_strings) total_sz += s.size();
        total.reserve(total_sz);
        for (const auto& s : row_strings) total += s;
        return total;
    }
    // -------------------------------------------------------------
    // MODO C: CUADRANTES HD 2x2 (4 Subpíxeles con Cobertura 100% Sólida)
    // -------------------------------------------------------------
    else if (mode == "quadrants" || mode == "quadrant" || mode == "q") {
        int sub_w = target_w * 2;
        int num_rows = (int)std::round(target_w * aspect * font_ratio);
        int sub_h = num_rows * 2;

        std::vector<uint8_t> scaled(sub_w * sub_h * 4);
        stbir_resize_uint8_linear(raw_data, orig_w, orig_h, 0, scaled.data(), sub_w, sub_h, 0, STBIR_RGBA);
        stbi_image_free(raw_data);

        if (!raw_colors) {
            apply_oklab_guided_filter(scaled, sub_w, sub_h, 2, 0.0004f);
        }

        std::vector<std::string> row_strings(num_rows);

        #pragma omp parallel for schedule(dynamic, 4)
        for (int row_idx = 0; row_idx < num_rows; ++row_idx) {
            int y = row_idx * 2;
            AnsiBuffer row_buf;

            for (int x = 0; x < sub_w; x += 2) {
                std::vector<RGB> quad_p(4);
                std::vector<uint8_t> quad_a(4);

                int order[4][2] = { {0,0}, {1,0}, {0,1}, {1,1} };
                for (int i = 0; i < 4; ++i) {
                    int cx = x + order[i][0];
                    int cy = y + order[i][1];
                    if (cx < sub_w && cy < sub_h) {
                        int p_idx = (cy * sub_w + cx) * 4;
                        quad_p[i] = { scaled[p_idx + 0], scaled[p_idx + 1], scaled[p_idx + 2] };
                        quad_a[i] = scaled[p_idx + 3];
                    } else {
                        quad_p[i] = { 0, 0, 0 };
                        quad_a[i] = 0;
                    }
                }

                bool all_trans = true;
                for (uint8_t a : quad_a) if (a >= 64) { all_trans = false; break; }
                if (all_trans) {
                    row_buf.emit_cell(" ");
                    continue;
                }

                ClusterResult cr = cluster_cell_oklab(quad_p);

                // Umbral adaptativo Weber-Fechner
                float tau = 0.0075f * std::pow((cr.mean_L + 0.08f) / 0.58f, 0.80f);

                if (cr.max_delta_e < tau) {
                    row_buf.emit_cell(" ", nullptr, &cr.bg);
                } else {
                    int cnt_true = 0;
                    for (bool m : cr.mask) if (m) cnt_true++;
                    if (cnt_true > 2) {
                        std::swap(cr.fg, cr.bg);
                        for (int i = 0; i < 4; ++i) cr.mask[i] = !cr.mask[i];
                    }

                    int q_mask = 0;
                    for (int i = 0; i < 4; ++i) {
                        if (quad_a[i] >= 64) {
                            bool is_on = cr.mask[i] != invert;
                            if (is_on) q_mask |= (1 << i);
                        }
                    }

                    const char* glyph = QUADRANTS[q_mask & 0x0F];
                    row_buf.emit_cell(glyph, &cr.fg, &cr.bg);
                }
            }
            row_buf.end_line();
            row_strings[row_idx] = row_buf.str();
        }

        std::string total;
        size_t total_sz = 0;
        for (const auto& s : row_strings) total_sz += s.size();
        total.reserve(total_sz);
        for (const auto& s : row_strings) total += s;
        return total;
    }
    // -------------------------------------------------------------
    // MODO D: MEDIOS BLOQUES 1x2 (▀)
    // -------------------------------------------------------------
    else if (mode == "blocks" || mode == "block" || mode == "k") {
        int sub_w = target_w;
        int num_rows = (int)std::round(target_w * aspect * font_ratio);
        int sub_h = num_rows * 2;

        std::vector<uint8_t> scaled(sub_w * sub_h * 4);
        stbir_resize_uint8_linear(raw_data, orig_w, orig_h, 0, scaled.data(), sub_w, sub_h, 0, STBIR_RGBA);
        stbi_image_free(raw_data);

        if (!raw_colors) {
            apply_oklab_guided_filter(scaled, sub_w, sub_h, 2, 0.0004f);
        }

        std::vector<std::string> row_strings(num_rows);

        #pragma omp parallel for schedule(dynamic, 4)
        for (int row_idx = 0; row_idx < num_rows; ++row_idx) {
            int y = row_idx * 2;
            AnsiBuffer row_buf;

            for (int x = 0; x < sub_w; ++x) {
                int top_idx = (y * sub_w + x) * 4;
                int bot_idx = ((y + 1) * sub_w + x) * 4;

                RGB top_c = { scaled[top_idx + 0], scaled[top_idx + 1], scaled[top_idx + 2] };
                RGB bot_c = { scaled[bot_idx + 0], scaled[bot_idx + 1], scaled[bot_idx + 2] };

                if (scaled[top_idx + 3] < 64 && scaled[bot_idx + 3] < 64) {
                    row_buf.emit_cell(" ");
                } else {
                    row_buf.emit_cell("▀", &top_c, &bot_c);
                }
            }
            row_buf.end_line();
            row_strings[row_idx] = row_buf.str();
        }

        std::string total;
        size_t total_sz = 0;
        for (const auto& s : row_strings) total_sz += s.size();
        total.reserve(total_sz);
        for (const auto& s : row_strings) total += s;
        return total;
    }
    // -------------------------------------------------------------
    // MODO E: ASCII DIRECCIONAL DE BORDES CON SCHARR
    // -------------------------------------------------------------
    else {
        int sub_w = target_w;
        int num_rows = (int)std::round(target_w * aspect * font_ratio);
        int sub_h = num_rows;

        std::vector<uint8_t> scaled(sub_w * sub_h * 4);
        stbir_resize_uint8_linear(raw_data, orig_w, orig_h, 0, scaled.data(), sub_w, sub_h, 0, STBIR_RGBA);
        stbi_image_free(raw_data);

        if (!raw_colors) {
            apply_oklab_guided_filter(scaled, sub_w, sub_h, 2, 0.0004f);
        }

        static const char* RAMP = "$@B%8&WM#*oahkbdpqwmZO0QLCJUXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ";
        int ramp_len = std::strlen(RAMP);

        std::vector<std::string> row_strings(num_rows);

        #pragma omp parallel for schedule(dynamic, 4)
        for (int y = 0; y < num_rows; ++y) {
            AnsiBuffer row_buf;

            for (int x = 0; x < sub_w; ++x) {
                int idx = (y * sub_w + x) * 4;
                if (scaled[idx + 3] < 64) {
                    row_buf.emit_cell(" ");
                    continue;
                }

                RGB rgb = { scaled[idx + 0], scaled[idx + 1], scaled[idx + 2] };
                Oklab ok = rgb_to_oklab(rgb.r, rgb.g, rgb.b);

                // Gradiente Scharr rápido
                float gx = 0, gy = 0;
                if (x > 0 && x < sub_w - 1 && y > 0 && y < sub_h - 1) {
                    auto lum = [&](int nx, int ny) {
                        int p = (ny * sub_w + nx) * 4;
                        return 0.299f * scaled[p] + 0.587f * scaled[p+1] + 0.114f * scaled[p+2];
                    };
                    gx = (lum(x+1, y-1) - lum(x-1, y-1)) * 3.0f + (lum(x+1, y) - lum(x-1, y)) * 10.0f + (lum(x+1, y+1) - lum(x-1, y+1)) * 3.0f;
                    gy = (lum(x-1, y+1) - lum(x-1, y-1)) * 3.0f + (lum(x, y+1) - lum(x, y-1)) * 10.0f + (lum(x+1, y+1) - lum(x+1, y-1)) * 3.0f;
                }

                float mag = std::sqrt(gx * gx + gy * gy);
                std::string glyph;
                if (mag > 150.0f) {
                    float angle = std::atan2(gy, gx) * 57.29578f;
                    if ((-22.5f <= angle && angle <= 22.5f) || angle >= 157.5f || angle <= -157.5f) glyph = "|";
                    else if (67.5f <= std::abs(angle) && std::abs(angle) <= 112.5f) glyph = "-";
                    else if ((22.5f < angle && angle < 67.5f) || (-157.5f < angle && angle < -112.5f)) glyph = "\\";
                    else glyph = "/";
                } else {
                    int r_idx = std::clamp((int)(ok.L * (ramp_len - 1)), 0, ramp_len - 1);
                    glyph = std::string(1, RAMP[r_idx]);
                }

                row_buf.emit_cell(glyph, &rgb);
            }
            row_buf.end_line();
            row_strings[y] = row_buf.str();
        }

        std::string total;
        size_t total_sz = 0;
        for (const auto& s : row_strings) total_sz += s.size();
        total.reserve(total_sz);
        for (const auto& s : row_strings) total += s;
        return total;
    }
}

// ==============================================================================
// 7. C-API EXPORTADA PARA BINDINGS CTYPES EN PYTHON
// ==============================================================================

extern "C" {
    const char* render_mary_c(const char* image_path, int width, const char* mode, bool raw_colors, bool invert) {
        std::string mode_str = mode ? mode : "braille";
        std::string res = render_mary_pipeline(image_path, width > 0 ? width : 90, mode_str, raw_colors, invert, 0.5f);
        char* buf = new char[res.size() + 1];
        std::strcpy(buf, res.c_str());
        return buf;
    }

    const char* render_mary_apex_c(const char* image_path, int width, const char* mode, bool raw_colors, bool invert, float font_ratio) {
        std::string mode_str = mode ? mode : "braille";
        if (font_ratio <= 0.05f || font_ratio >= 2.0f) font_ratio = 0.5f;
        std::string res = render_mary_pipeline(image_path, width > 0 ? width : 90, mode_str, raw_colors, invert, font_ratio);
        char* buf = new char[res.size() + 1];
        std::strcpy(buf, res.c_str());
        return buf;
    }

    void free_mary_buffer(char* ptr) {
        delete[] ptr;
    }
}

// ==============================================================================
// 8. BINARIO CLI INDEPENDIENTE (LUMA-MARY)
// ==============================================================================

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "Luma Mary Apex Engine v3.0 (C++17 Native Multi-Core)\n"
                  << "Usage: " << argv[0] << " <image_path> [-w width] [-m mode (sextants|braille|quadrants|blocks|ascii)] [-r font_ratio] [--raw-colors] [-i]\n";
        return 1;
    }
    std::string path = argv[1];
    int width = 80;
    std::string mode = "braille";
    float font_ratio = 0.5f;
    bool raw_colors = false;
    bool invert = false;

    for (int i = 2; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "-w" && i + 1 < argc) width = std::atoi(argv[++i]);
        else if (arg == "-m" && i + 1 < argc) mode = argv[++i];
        else if ((arg == "-r" || arg == "--font-ratio") && i + 1 < argc) font_ratio = std::atof(argv[++i]);
        else if (arg == "--raw-colors") raw_colors = true;
        else if (arg == "-i" || arg == "--invert") invert = true;
    }

    std::string out = render_mary_pipeline(path, width, mode, raw_colors, invert, font_ratio);
    std::cout << out;
    return 0;
}

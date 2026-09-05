/*
 * Luma Monochrome Engine (C++) - v2.1.2
 * Ultra-high-performance black & white terminal art generator.
 * Features:
 *  - Difference of Gaussians (DoG) artistic lineart extraction (G-pen / Maru-pen simulation)
 *  - Smart Manga Screentone 2.0 (zoned midtones with 8x8 Bayer, zero skin/paper noise)
 *  - Pure Sketch / Outline mode without halftoning
 *  - Bill Atkinson error diffusion dithering (1984) & Floyd-Steinberg
 *  - High-definition Braille micropoints (2x4 resolution per cell)
 *  - High-definition Quadrant Unicode blocks (2x2 subpixels per cell: ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█)
 *  - Extended 70-character perceptual ASCII luminance ramp
 *  - Autonomous single-binary compilation with stb_image & stb_image_resize2
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
#include <fstream>
#include <cstring>
#include <sys/ioctl.h>
#include <unistd.h>

// Extended 70-character ASCII density ramp (sorted dark to light)
static const char* ASCII_70 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ";
static const char* ASCII_10 = "@%#*+=-:. ";

// Unicode Quadrant Blocks (2x2 subpixels per character cell)
// Bitmask: bit 0 = Top-Left, bit 1 = Top-Right, bit 2 = Bottom-Left, bit 3 = Bottom-Right
static const char* QUADRANT_BLOCKS[16] = {
    " ", // 0000
    "▘", // 0001 (TL)
    "▝", // 0010 (TR)
    "▀", // 0011 (TL+TR)
    "▖", // 0100 (BL)
    "▌", // 0101 (TL+BL)
    "▞", // 0110 (TR+BL)
    "▛", // 0111 (TL+TR+BL)
    "▗", // 1000 (BR)
    "▚", // 1001 (TL+BR)
    "▐", // 1010 (TR+BR)
    "▜", // 1011 (TL+TR+BR)
    "▄", // 1100 (BL+BR)
    "▙", // 1101 (TL+BL+BR)
    "▟", // 1110 (TR+BL+BR)
    "█"  // 1111 (ALL)
};

// Unicode Density Blocks (UTF-8 encoded single-char shades)
static const char* BLOCK_SHADES[5] = {
    "█", // 100%
    "▓", // 75%
    "▒", // 50%
    "░", // 25%
    " "  // 0%
};

// Bayer Matrix 8x8 for retro ordered screentone dithering
static const int BAYER_8X8[8][8] = {
    {  0, 32,  8, 40,  2, 34, 10, 42 },
    { 48, 16, 56, 24, 50, 18, 58, 26 },
    { 12, 44,  4, 36, 14, 46,  6, 38 },
    { 60, 28, 52, 20, 62, 30, 54, 22 },
    {  3, 35, 11, 43,  1, 33,  9, 41 },
    { 51, 19, 59, 27, 49, 17, 57, 25 },
    { 15, 47,  7, 39, 13, 45,  5, 37 },
    { 63, 31, 55, 23, 61, 29, 53, 21 }
};

// Encode Braille Unicode code point (0x2800..0x28FF) into 3-byte UTF-8 string
static inline void encode_braille_utf8(int val, std::string& out) {
    val &= 0xFF;
    out.push_back(static_cast<char>(0xE2));
    out.push_back(static_cast<char>(0xA0 | ((val >> 6) & 0x03)));
    out.push_back(static_cast<char>(0x80 | (val & 0x3F)));
}

// Perceptual luminance calculation according to ITU-R BT.709
static inline float get_luminance(uint8_t r, uint8_t g, uint8_t b) {
    return 0.2126f * r + 0.7152f * g + 0.0722f * b;
}

// Contrast-limited histogram stretch (Autocontrast)
static void autocontrast_gray(std::vector<float>& gray, int count) {
    float min_v = 255.0f, max_v = 0.0f;
    for (int i = 0; i < count; ++i) {
        if (gray[i] < min_v) min_v = gray[i];
        if (gray[i] > max_v) max_v = gray[i];
    }
    float range = max_v - min_v;
    if (range < 1.0f) range = 1.0f;
    for (int i = 0; i < count; ++i) {
        gray[i] = ((gray[i] - min_v) / range) * 255.0f;
    }
}

// -------------------------------------------------------------
// Separable 1D Gaussian Blur & Difference of Gaussians (DoG)
// -------------------------------------------------------------
static std::vector<float> make_gaussian_kernel(float sigma) {
    int radius = static_cast<int>(std::ceil(2.5f * sigma));
    if (radius < 1) radius = 1;
    int size = 2 * radius + 1;
    std::vector<float> kernel(size);
    float sum = 0.0f;
    for (int i = -radius; i <= radius; ++i) {
        float val = std::exp(-(i * i) / (2.0f * sigma * sigma));
        kernel[i + radius] = val;
        sum += val;
    }
    for (float& v : kernel) v /= sum;
    return kernel;
}

static std::vector<float> gaussian_blur_2d(const std::vector<float>& src, int w, int h, float sigma) {
    std::vector<float> kernel = make_gaussian_kernel(sigma);
    int radius = static_cast<int>(kernel.size()) / 2;
    std::vector<float> temp(w * h, 0.0f);
    std::vector<float> out(w * h, 0.0f);

    // Horizontal pass
    for (int y = 0; y < h; ++y) {
        int row_offset = y * w;
        for (int x = 0; x < w; ++x) {
            float sum = 0.0f;
            for (int k = -radius; k <= radius; ++k) {
                int cx = std::max(0, std::min(w - 1, x + k));
                sum += src[row_offset + cx] * kernel[k + radius];
            }
            temp[row_offset + x] = sum;
        }
    }

    // Vertical pass
    for (int x = 0; x < w; ++x) {
        for (int y = 0; y < h; ++y) {
            float sum = 0.0f;
            for (int k = -radius; k <= radius; ++k) {
                int cy = std::max(0, std::min(h - 1, y + k));
                sum += temp[cy * w + x] * kernel[k + radius];
            }
            out[y * w + x] = sum;
        }
    }
    return out;
}

// Difference of Gaussians (DoG) for artistic line drawing
static std::vector<float> compute_dog_edges(const std::vector<float>& gray, int w, int h, float sigma1 = 0.7f, float sigma2 = 1.8f) {
    std::vector<float> g1 = gaussian_blur_2d(gray, w, h, sigma1);
    std::vector<float> g2 = gaussian_blur_2d(gray, w, h, sigma2);
    std::vector<float> dog(w * h, 0.0f);
    for (int i = 0; i < w * h; ++i) {
        // Dark ink lines have lower g1 than g2, so g2 - g1 is positive at line centers
        dog[i] = g2[i] - g1[i];
    }
    return dog;
}

// -------------------------------------------------------------
// Dithering Algorithms
// -------------------------------------------------------------

// Bill Atkinson error diffusion dithering (1984, MacPaint)
// Diffuses only 75% (6/8) of the error, leaving pure whites and deep blacks
static std::vector<uint8_t> atkinson_dither(const std::vector<float>& input, int w, int h, float threshold = 128.0f) {
    std::vector<float> buffer = input;
    std::vector<uint8_t> result(w * h, 0);

    for (int y = 0; y < h; ++y) {
        for (int x = 0; x < w; ++x) {
            int idx = y * w + x;
            float old_val = buffer[idx];
            uint8_t new_val = (old_val >= threshold) ? 255 : 0;
            result[idx] = new_val;
            float err = (old_val - new_val) / 8.0f;

            if (x + 1 < w) buffer[y * w + (x + 1)] += err;
            if (x + 2 < w) buffer[y * w + (x + 2)] += err;
            if (y + 1 < h) {
                if (x - 1 >= 0) buffer[(y + 1) * w + (x - 1)] += err;
                buffer[(y + 1) * w + x] += err;
                if (x + 1 < w) buffer[(y + 1) * w + (x + 1)] += err;
            }
            if (y + 2 < h) {
                buffer[(y + 2) * w + x] += err;
            }
        }
    }
    return result;
}

// Floyd-Steinberg error diffusion dithering
static std::vector<uint8_t> floyd_steinberg_dither(const std::vector<float>& input, int w, int h, float threshold = 128.0f) {
    std::vector<float> buffer = input;
    std::vector<uint8_t> result(w * h, 0);

    for (int y = 0; y < h; ++y) {
        for (int x = 0; x < w; ++x) {
            int idx = y * w + x;
            float old_val = buffer[idx];
            uint8_t new_val = (old_val >= threshold) ? 255 : 0;
            result[idx] = new_val;
            float err = old_val - new_val;

            if (x + 1 < w)
                buffer[y * w + (x + 1)] += err * (7.0f / 16.0f);
            if (y + 1 < h) {
                if (x - 1 >= 0)
                    buffer[(y + 1) * w + (x - 1)] += err * (3.0f / 16.0f);
                buffer[(y + 1) * w + x] += err * (5.0f / 16.0f);
                if (x + 1 < w)
                    buffer[(y + 1) * w + (x + 1)] += err * (1.0f / 16.0f);
            }
        }
    }
    return result;
}

// Bayer 8x8 ordered dithering
static std::vector<uint8_t> bayer_dither(const std::vector<float>& input, int w, int h) {
    std::vector<uint8_t> result(w * h, 0);
    for (int y = 0; y < h; ++y) {
        for (int x = 0; x < w; ++x) {
            float val = input[y * w + x];
            float threshold = (BAYER_8X8[y % 8][x % 8] + 0.5f) * (255.0f / 64.0f);
            result[y * w + x] = (val >= threshold) ? 255 : 0;
        }
    }
    return result;
}

struct RenderConfig {
    int target_width = 90;
    std::string mode = "braille"; // braille, manga, sketch, blocks, ascii, shades
    std::string dither = "none";  // atkinson, floyd, bayer, none
    bool invert = false;
    bool high_contrast = true;
    float gamma = 1.0f;
    std::string output_file = "";
};

std::string render_monochrome_image(const std::string& image_path, const RenderConfig& cfg) {
    int orig_w, orig_h, channels;
    uint8_t* raw_data = stbi_load(image_path.c_str(), &orig_w, &orig_h, &channels, 4);
    if (!raw_data) {
        return "❌ Error: Could not open image: " + image_path + "\n";
    }

    float aspect = static_cast<float>(orig_h) / static_cast<float>(orig_w);

    // Resolution dimensions based on selected mode
    int scaled_w = 0, scaled_h = 0;
    if (cfg.mode == "braille" || cfg.mode == "manga" || cfg.mode == "sketch") {
        // Braille has 2x4 dots per character cell
        scaled_w = cfg.target_width * 2;
        scaled_h = static_cast<int>(scaled_w * aspect * 0.5f * 2.0f);
        scaled_h = scaled_h + (4 - scaled_h % 4) % 4; // multiple of 4
    } else if (cfg.mode == "blocks") {
        // Quadrant HD Blocks (2x2 subpixels per character cell)
        scaled_w = cfg.target_width * 2;
        scaled_h = static_cast<int>(cfg.target_width * 2 * aspect * 0.5f);
        scaled_h = scaled_h + (2 - scaled_h % 2) % 2; // multiple of 2
    } else {
        // ASCII or single-character shades mode (1 char cell = 1 sample)
        scaled_w = cfg.target_width;
        scaled_h = static_cast<int>(cfg.target_width * aspect * 0.5f);
    }

    if (scaled_w < 2) scaled_w = 2;
    if (scaled_h < 4) scaled_h = 4;

    // High-quality resizing with Lanczos / Mitchell-Netravali
    std::vector<uint8_t> resized(scaled_w * scaled_h * 4);
    stbir_resize_uint8_linear(
        raw_data, orig_w, orig_h, 0,
        resized.data(), scaled_w, scaled_h, 0,
        STBIR_RGBA
    );
    stbi_image_free(raw_data);

    // Extract perceptual luminance & alpha channels
    int total_pixels = scaled_w * scaled_h;
    std::vector<float> luminance(total_pixels);
    std::vector<uint8_t> alpha(total_pixels);

    for (int i = 0; i < total_pixels; ++i) {
        uint8_t r = resized[i * 4 + 0];
        uint8_t g = resized[i * 4 + 1];
        uint8_t b = resized[i * 4 + 2];
        uint8_t a = resized[i * 4 + 3];
        alpha[i] = a;

        float lum = get_luminance(r, g, b);
        if (cfg.gamma != 1.0f) {
            lum = std::pow(lum / 255.0f, cfg.gamma) * 255.0f;
        }
        luminance[i] = lum;
    }

    if (cfg.high_contrast) {
        autocontrast_gray(luminance, total_pixels);
    }

    std::string ascii_art;
    ascii_art.reserve(cfg.target_width * (scaled_h / 2 + 1) * 4);

    // Ink density: 255 = dark ink, 0 = pure white paper
    std::vector<float> ink_density(total_pixels);
    for (int i = 0; i < total_pixels; ++i) {
        ink_density[i] = 255.0f - luminance[i];
    }

    // -------------------------------------------------------------
    // MODES: Braille, Manga 2.0, Sketch, Quadrants HD
    // -------------------------------------------------------------
    if (cfg.mode == "braille" || cfg.mode == "manga" || cfg.mode == "sketch") {
        std::vector<uint8_t> binary_grid(total_pixels, 0);

        if (cfg.mode == "sketch") {
            // Pure Sketch / Lineart: DoG edge contours without screentones
            std::vector<float> dog = compute_dog_edges(luminance, scaled_w, scaled_h, 0.7f, 1.8f);
            for (int i = 0; i < total_pixels; ++i) {
                if (dog[i] > 6.0f || luminance[i] < 35.0f) {
                    binary_grid[i] = 255;
                }
            }
        } else if (cfg.mode == "manga") {
            // Smart Manga Screentone 2.0:
            // 1. Clean paper & skin: pure white (zero dot noise)
            // 2. Line art: crisp solid ink via DoG filter
            // 3. Clothing / hair shadows: 8x8 Bayer screentone (Ami-tone)
            // 4. Deep shadows: solid black
            std::vector<float> dog = compute_dog_edges(luminance, scaled_w, scaled_h, 0.7f, 1.8f);

            for (int y = 0; y < scaled_h; ++y) {
                for (int x = 0; x < scaled_w; ++x) {
                    int i = y * scaled_w + x;
                    float ink = ink_density[i];
                    bool is_line = (dog[i] > 6.0f);

                    if (is_line) {
                        binary_grid[i] = 255; // Line art contour
                    } else if (ink > 215.0f) {
                        binary_grid[i] = 255; // Solid deep shadow
                    } else if (ink > 110.0f) {
                        // Midtones / clothing: Bayer screentone
                        float threshold = (BAYER_8X8[y % 8][x % 8] + 0.5f) * (255.0f / 64.0f);
                        if ((ink - 50.0f) >= threshold) {
                            binary_grid[i] = 255;
                        }
                    }
                }
            }
        } else if (cfg.dither == "atkinson" || cfg.dither == "1" || cfg.dither == "true" || cfg.dither == "default") {
            // Atkinson error diffusion: clean paper highlights
            std::vector<float> cleaned_ink = ink_density;
            for (float& val : cleaned_ink) {
                if (val < 25.0f) val = 0.0f;
            }
            binary_grid = atkinson_dither(cleaned_ink, scaled_w, scaled_h, 128.0f);
        } else if (cfg.dither == "floyd") {
            std::vector<float> cleaned_ink = ink_density;
            for (float& val : cleaned_ink) {
                if (val < 25.0f) val = 0.0f;
            }
            binary_grid = floyd_steinberg_dither(cleaned_ink, scaled_w, scaled_h, 128.0f);
        } else if (cfg.dither == "bayer") {
            binary_grid = bayer_dither(ink_density, scaled_w, scaled_h);
        } else {
            // Crisp luminance threshold
            for (int i = 0; i < total_pixels; ++i) {
                binary_grid[i] = (luminance[i] < 128.0f) ? 255 : 0;
            }
        }

        // Standard Braille dot map (Unicode U+2800)
        static const int dot_map[4][2] = {
            {0x01, 0x08},
            {0x02, 0x10},
            {0x04, 0x20},
            {0x40, 0x80}
        };

        for (int y = 0; y < scaled_h; y += 4) {
            for (int x = 0; x < scaled_w; x += 2) {
                int braille_val = 0;

                for (int dy = 0; dy < 4; ++dy) {
                    for (int dx = 0; dx < 2; ++dx) {
                        int cur_x = x + dx;
                        int cur_y = y + dy;
                        if (cur_x < scaled_w && cur_y < scaled_h) {
                            int idx = cur_y * scaled_w + cur_x;
                            if (alpha[idx] < 128) {
                                continue;
                            }
                            bool is_on = (binary_grid[idx] > 0);
                            if (cfg.invert) is_on = !is_on;
                            if (is_on) {
                                braille_val |= dot_map[dy][dx];
                            }
                        }
                    }
                }

                if (braille_val == 0) {
                    ascii_art.push_back(' ');
                } else {
                    encode_braille_utf8(braille_val, ascii_art);
                }
            }
            ascii_art.push_back('\n');
        }
    }
    // -------------------------------------------------------------
    // MODE: High-Definition Quadrant Blocks (2x2 subpixels)
    // -------------------------------------------------------------
    else if (cfg.mode == "blocks") {
        std::vector<uint8_t> binary_grid(total_pixels, 0);

        if (cfg.dither == "floyd") {
            binary_grid = floyd_steinberg_dither(ink_density, scaled_w, scaled_h, 128.0f);
        } else if (cfg.dither == "bayer") {
            binary_grid = bayer_dither(ink_density, scaled_w, scaled_h);
        } else {
            // Default to Atkinson for blocks: clean, sharp edges
            std::vector<float> cleaned_ink = ink_density;
            for (float& val : cleaned_ink) {
                if (val < 25.0f) val = 0.0f;
            }
            binary_grid = atkinson_dither(cleaned_ink, scaled_w, scaled_h, 128.0f);
        }

        for (int y = 0; y < scaled_h; y += 2) {
            for (int x = 0; x < scaled_w; x += 2) {
                int mask = 0;
                // Bit 0: Top-Left
                int idx_tl = y * scaled_w + x;
                if (alpha[idx_tl] >= 128 && (binary_grid[idx_tl] > 0) != cfg.invert) mask |= 1;

                // Bit 1: Top-Right
                if (x + 1 < scaled_w) {
                    int idx_tr = y * scaled_w + (x + 1);
                    if (alpha[idx_tr] >= 128 && (binary_grid[idx_tr] > 0) != cfg.invert) mask |= 2;
                }

                // Bit 2: Bottom-Left
                if (y + 1 < scaled_h) {
                    int idx_bl = (y + 1) * scaled_w + x;
                    if (alpha[idx_bl] >= 128 && (binary_grid[idx_bl] > 0) != cfg.invert) mask |= 4;
                }

                // Bit 3: Bottom-Right
                if (y + 1 < scaled_h && x + 1 < scaled_w) {
                    int idx_br = (y + 1) * scaled_w + (x + 1);
                    if (alpha[idx_br] >= 128 && (binary_grid[idx_br] > 0) != cfg.invert) mask |= 8;
                }

                ascii_art += QUADRANT_BLOCKS[mask];
            }
            ascii_art.push_back('\n');
        }
    }
    // -------------------------------------------------------------
    // MODE: Extended 70-character ASCII Density Ramp
    // -------------------------------------------------------------
    else if (cfg.mode == "ascii") {
        int ramp_len = strlen(ASCII_70);
        for (int y = 0; y < scaled_h; ++y) {
            for (int x = 0; x < scaled_w; ++x) {
                int idx = y * scaled_w + x;
                if (alpha[idx] < 128) {
                    ascii_art.push_back(' ');
                    continue;
                }
                float val = luminance[idx];
                int char_idx = static_cast<int>((val / 255.0f) * (ramp_len - 1));
                char_idx = std::max(0, std::min(ramp_len - 1, char_idx));
                if (cfg.invert) char_idx = (ramp_len - 1) - char_idx;
                ascii_art.push_back(ASCII_70[char_idx]);
            }
            ascii_art.push_back('\n');
        }
    }
    // -------------------------------------------------------------
    // MODE: Unicode Shading Blocks (░, ▒, ▓, █)
    // -------------------------------------------------------------
    else {
        for (int y = 0; y < scaled_h; ++y) {
            for (int x = 0; x < scaled_w; ++x) {
                int idx = y * scaled_w + x;
                if (alpha[idx] < 128) {
                    ascii_art.push_back(' ');
                    continue;
                }
                float val = luminance[idx];
                int shade_idx = static_cast<int>((val / 255.0f) * 4);
                shade_idx = std::max(0, std::min(4, shade_idx));
                if (cfg.invert) shade_idx = 4 - shade_idx;
                ascii_art += BLOCK_SHADES[shade_idx];
            }
            ascii_art.push_back('\n');
        }
    }

    return ascii_art;
}

// C-compatible Exported API for Python ctypes bindings
extern "C" {
    const char* render_monochrome_c(const char* image_path, int width, const char* mode, const char* dither, bool invert) {
        RenderConfig cfg;
        cfg.target_width = width > 0 ? width : 90;
        cfg.mode = mode ? mode : "braille";
        cfg.dither = dither ? dither : "none";
        cfg.invert = invert;

        std::string result = render_monochrome_image(image_path, cfg);
        char* buffer = new char[result.size() + 1];
        std::strcpy(buffer, result.c_str());
        return buffer;
    }

    void free_monochrome_buffer(char* ptr) {
        delete[] ptr;
    }
}

static void print_banner() {
    std::cout << "\033[1;37m"
              << " █    █ █ █▄ ▄█ ▄▀▄   █▄ ▄█ ▄▀▄ █▄ █ ▄▀▄\n"
              << " █▄▄▄ ▀▄█ █ ▀ █ █▀█ ▀ █ ▀ █ ▀▄▀ █ ▀█ ▀▄▀ (B&W Engine v2.1.2)\033[0m\n\n";
}

static void print_usage(const char* prog) {
    print_banner();
    std::cout << "Usage: " << prog << " [options] <image_path>\n\n"
              << "Options:\n"
              << "  -w, --width <num>    Output width in terminal cells (default: auto-detected)\n"
              << "  -m, --mode <type>    Rendering mode: braille (default), manga, sketch, blocks, ascii, shades\n"
              << "  -d, --dither <algo>  Dithering algorithm: atkinson (default), floyd, bayer, none\n"
              << "  -i, --invert         Invert lightness (useful for dark vs light terminals)\n"
              << "  -g, --gamma <val>    Adjust gamma curve (e.g. 1.5 for punchier contrast)\n"
              << "  -o, --output <file>  Save output directly to text file\n"
              << "  -h, --help           Show this help message\n";
}

int main(int argc, char** argv) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }

    RenderConfig cfg;
    std::string image_path = "";

    // Auto-detect terminal width
    struct winsize ws;
    if (ioctl(STDOUT_FILENO, TIOCGWINSZ, &ws) == 0 && ws.ws_col > 10) {
        cfg.target_width = std::min(120, std::max(30, (int)ws.ws_col));
    } else {
        cfg.target_width = 90;
    }

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "-h" || arg == "--help") {
            print_usage(argv[0]);
            return 0;
        } else if (arg == "-w" || arg == "--width") {
            if (i + 1 < argc) cfg.target_width = std::atoi(argv[++i]);
        } else if (arg == "-m" || arg == "--mode") {
            if (i + 1 < argc) cfg.mode = argv[++i];
        } else if (arg == "-d" || arg == "--dither") {
            if (i + 1 < argc && argv[i + 1][0] != '-') {
                cfg.dither = argv[++i];
            } else {
                cfg.dither = "atkinson";
            }
        } else if (arg == "-b" || arg == "--bayer") {
            cfg.dither = "bayer";
        } else if (arg == "-i" || arg == "--invert") {
            cfg.invert = true;
        } else if (arg == "-g" || arg == "--gamma") {
            if (i + 1 < argc) cfg.gamma = std::atof(argv[++i]);
        } else if (arg == "-o" || arg == "--output") {
            if (i + 1 < argc) cfg.output_file = argv[++i];
        } else if (arg[0] != '-') {
            image_path = arg;
        }
    }

    if (image_path.empty()) {
        std::cerr << "Error: No image path specified.\n";
        return 1;
    }

    std::string art = render_monochrome_image(image_path, cfg);

    if (!cfg.output_file.empty()) {
        std::ofstream out(cfg.output_file);
        if (!out) {
            std::cerr << "Error writing to " << cfg.output_file << "\n";
            return 1;
        }
        out << art;
        std::cout << "Monochrome ASCII art successfully saved to " << cfg.output_file << "\n";
    } else {
        std::cout << art;
    }

    return 0;
}

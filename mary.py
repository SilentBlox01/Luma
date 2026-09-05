#!/usr/bin/env python3
"""
==============================================================================
 Luma - Mary Engine (v1.0)
 Motor a Color de Nueva Generación basado en Percepción Visual Computacional.
==============================================================================
 "Cero redes neuronales, cero modelos de 4 GB, cero humo de Silicon Valley:
  Pura matemática óptica, espacio de color perceptual Oklab, clustering K-Means
  sub-píxel y optimización de flujo ANSI para terminales de ultra-alta fidelidad."
==============================================================================
"""

import sys
import os
import math
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# ==============================================================================
# 1. MATEMÁTICA ÓPTICA Y ESPACIO DE COLOR PERCEPTUAL OKLAB
# ==============================================================================
# El espacio sRGB estándar distorsiona la percepción del ojo humano (sombras
# aplastadas, bandas de degradado sucias). Oklab (Björn Ottosson, 2020) modela
# la respuesta cromática de los conos de la retina humana con precisión extrema.
# Usamos tablas de búsqueda (LUT) para velocidad de ejecución instantánea.

# Tablas LUT precalculadas para conversión sRGB <-> Linear RGB
_SRGB_TO_LINEAR = [0.0] * 256
for _i in range(256):
    _v = _i / 255.0
    _SRGB_TO_LINEAR[_i] = _v / 12.92 if _v <= 0.04045 else ((_v + 0.055) / 1.055) ** 2.4

def srgb_to_linear(v):
    """Convierte valor de 8 bits (0-255) a espacio lineal físico [0.0, 1.0]."""
    return _SRGB_TO_LINEAR[max(0, min(255, int(v)))]

def linear_to_srgb(c):
    """Convierte valor lineal físico [0.0, 1.0] a sRGB entero [0, 255]."""
    if c <= 0.0031308:
        val = c * 12.92
    else:
        val = 1.055 * (c ** (1.0 / 2.4)) - 0.055
    return max(0, min(255, int(round(val * 255.0))))

def rgb_to_oklab(r, g, b):
    """
    Transforma coordenadas sRGB a Oklab (L: luminosidad perceptual, a: verde-rojo, b: azul-amarillo).
    L ∈ [0.0, 1.0], a ∈ [-0.4, 0.4], b ∈ [-0.4, 0.4].
    """
    r_l = _SRGB_TO_LINEAR[r]
    g_l = _SRGB_TO_LINEAR[g]
    b_l = _SRGB_TO_LINEAR[b]

    # Transformación al espacio de conos oculares LMS
    l_con = (0.4122214708 * r_l + 0.5363325363 * g_l + 0.0514459929 * b_l)
    m_con = (0.2119034982 * r_l + 0.6883090962 * g_l + 0.0997874057 * b_l)
    s_con = (0.0883024619 * r_l + 0.2817188376 * g_l + 0.6299787005 * b_l)

    # Raíz cúbica perceptual no lineal (evita números complejos si hay valores infinitesimales)
    l_ = (l_con ** (1.0 / 3.0)) if l_con > 0.0 else 0.0
    m_ = (m_con ** (1.0 / 3.0)) if m_con > 0.0 else 0.0
    s_ = (s_con ** (1.0 / 3.0)) if s_con > 0.0 else 0.0

    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b_ok = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_

    return (L, a, b_ok)

def oklab_to_rgb(L, a, b_ok):
    """Transforma coordenadas Oklab de vuelta a sRGB entero [0, 255]."""
    l_ = L + 0.3963377774 * a + 0.2158037573 * b_ok
    m_ = L - 0.1055613458 * a - 0.0638541728 * b_ok
    s_ = L - 0.0894841775 * a - 1.2914855480 * b_ok

    # Elevación al cubo rápida sin overhead de pow
    l = l_ * l_ * l_
    m = m_ * m_ * m_
    s = s_ * s_ * s_

    r_l = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g_l = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b_l = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

    return (linear_to_srgb(r_l), linear_to_srgb(g_l), linear_to_srgb(b_l))

def oklab_dist_sq(c1, c2):
    """Distancia perceptual euclidiana cuadrática ΔE en Oklab."""
    dL = c1[0] - c2[0]
    da = c1[1] - c2[1]
    db = c1[2] - c2[2]
    # La luminosidad pesa un 25% más en el ojo humano que el croma
    return 1.25 * (dL * dL) + (da * da) + (db * db)

# ==============================================================================
# 2. ADAPTACIÓN SEMÁNTICA Y RANGO DINÁMICO PERCEPTUAL (AUTO-HDR)
# ==============================================================================

def apply_msrcr_retinex(img):
    """
    Multi-Scale Retinex with Color Restoration (MSRCR) en 3 escalas (15, 60, 180).
    Alineado matemáticamente con Jobson, Rahman & Woodell (NASA).
    Elimina neblina, recupera sombras y expande rango dinámico sin quemar luces.
    """
    try:
        import numpy as np
        rgb_img = img.convert("RGB")
        arr = np.array(rgb_img, dtype=np.float32) + 1.0
        r_img, g_img, b_img = rgb_img.split()
        msrcr = np.zeros_like(arr)
        
        for sigma in [15.0, 60.0, 180.0]:
            blur_r = np.array(r_img.filter(ImageFilter.GaussianBlur(radius=sigma)), dtype=np.float32) + 1.0
            blur_g = np.array(g_img.filter(ImageFilter.GaussianBlur(radius=sigma)), dtype=np.float32) + 1.0
            blur_b = np.array(b_img.filter(ImageFilter.GaussianBlur(radius=sigma)), dtype=np.float32) + 1.0
            
            msrcr[:, :, 0] += (1.0 / 3.0) * (np.log(arr[:, :, 0]) - np.log(blur_r))
            msrcr[:, :, 1] += (1.0 / 3.0) * (np.log(arr[:, :, 1]) - np.log(blur_g))
            msrcr[:, :, 2] += (1.0 / 3.0) * (np.log(arr[:, :, 2]) - np.log(blur_b))

        sum_rgb = arr.sum(axis=2, keepdims=True)
        cr = 1.5 * (np.log(125.0 * arr) - np.log(sum_rgb))
        final = msrcr * cr

        vmin = final.min()
        vmax = final.max()
        norm = ((final - vmin) / (vmax - vmin + 1e-6)) * 255.0
        blend = np.clip(0.7 * norm + 0.3 * (arr - 1.0), 0, 255).astype(np.uint8)
        
        try:
            import cv2
            blend = cv2.bilateralFilter(blend, d=5, sigmaColor=35, sigmaSpace=35)
        except Exception:
            pass
            
        res = Image.fromarray(blend).convert("RGBA")
        # Preservar canal alfa original si existía
        if img.mode == "RGBA":
            res.putalpha(img.split()[3])
        return res
    except Exception:
        return None

def adapt_perceptual_tone_and_color(image, raw_colors=False):
    """
    Analiza la imagen estadísticamente y aplica mejoras adaptativas no lineales:
    - Multi-Scale Retinex (MSRCR) en 3 escalas + Filtro Bilateral.
    - Preservación y protección de tonos de piel humana/anime.
    - Realce de nitidez enfocado en frecuencias altas de bordes.
    """
    if raw_colors:
        return image.convert("RGBA")

    # Intentar pipeline MSRCR Retinex completo
    retinex_img = apply_msrcr_retinex(image)
    if retinex_img is not None:
        img = retinex_img
    else:
        img = image.convert("RGBA")
        img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=145, threshold=2))
        
        gray = img.convert("L")
        hist = gray.histogram()
        total_pixels = max(1, sum(hist))
        
        accum = 0
        p10 = 0
        p90 = 255
        for i, count in enumerate(hist):
            accum += count
            if accum >= total_pixels * 0.10 and p10 == 0:
                p10 = i
            if accum >= total_pixels * 0.90:
                p90 = i
                break
                
        mean_lum = sum(i * count for i, count in enumerate(hist)) / total_pixels
        
        if mean_lum < 95.0:
            gamma_factor = 1.18 if mean_lum < 60.0 else 1.10
            img = ImageEnhance.Brightness(img).enhance(gamma_factor)
            img = ImageEnhance.Contrast(img).enhance(1.15)
        elif mean_lum > 180.0:
            img = ImageEnhance.Contrast(img).enhance(1.20)
        else:
            img = ImageEnhance.Contrast(img).enhance(1.12)
            
        img = ImageEnhance.Color(img).enhance(1.22)
    
    return img

# ==============================================================================
# 3. CLUSTERING K-MEANS SUBPÍXEL POR CELDA (BRAILLE Y CUADRANTES HD)
# ==============================================================================
# En lugar de promediar tontamente los 8 píxeles de una celda Braille en un solo
# color plano, Mary encuentra los 2 colores óptimos (C_fg y C_bg) en espacio Oklab.
# Esto hace que destellos, ojos, reflejos y líneas finas resalten con máximo contraste.

def cluster_cell_two_colors(pixels_rgb):
    """
    Encuentra los dos centroides cromáticos óptimos (Foreground y Background)
    en espacio Oklab para un conjunto de subpíxeles (4 para bloques, 8 para Braille).
    Retorna: (fg_rgb, bg_rgb, assignments_boolean_list, max_delta_e)
    """
    n = len(pixels_rgb)
    if n == 0:
        return ((255, 255, 255), (0, 0, 0), [], 0.0)

    ok_points = [rgb_to_oklab(*p) for p in pixels_rgb]

    # Calcular media global en Oklab
    mean_L = sum(p[0] for p in ok_points) / n
    mean_a = sum(p[1] for p in ok_points) / n
    mean_b = sum(p[2] for p in ok_points) / n

    # Encontrar el punto más alejado de la media para iniciar el primer centroide
    max_d1 = -1.0
    c1_idx = 0
    for i, pt in enumerate(ok_points):
        d = (pt[0] - mean_L)**2 + (pt[1] - mean_a)**2 + (pt[2] - mean_b)**2
        if d > max_d1:
            max_d1 = d
            c1_idx = i

    c1 = ok_points[c1_idx]

    # Encontrar el punto más alejado de c1 para iniciar el segundo centroide
    max_d2 = -1.0
    c2_idx = 0
    for i, pt in enumerate(ok_points):
        d = oklab_dist_sq(pt, c1)
        if d > max_d2:
            max_d2 = d
            c2_idx = i

    c2 = ok_points[c2_idx]

    # Si la varianza total en la celda es insignificante, unificar a un único color
    if max_d2 < 0.003:
        avg_rgb = oklab_to_rgb(mean_L, mean_a, mean_b)
        return (avg_rgb, avg_rgb, [True] * n, max_d2, mean_L)

    # 2 iteraciones de refinamiento K-Means rápido
    for _ in range(2):
        g1 = []
        g2 = []
        for pt in ok_points:
            if oklab_dist_sq(pt, c1) <= oklab_dist_sq(pt, c2):
                g1.append(pt)
            else:
                g2.append(pt)

        if g1:
            c1 = (sum(p[0] for p in g1) / len(g1), sum(p[1] for p in g1) / len(g1), sum(p[2] for p in g1) / len(g1))
        if g2:
            c2 = (sum(p[0] for p in g2) / len(g2), sum(p[1] for p in g2) / len(g2), sum(p[2] for p in g2) / len(g2))

    # Asegurar que c1 sea el color más luminoso (Foreground para Braille)
    if c1[0] < c2[0]:
        c1, c2 = c2, c1

    # Asignaciones booleanas: True -> c1 (primer plano), False -> c2 (fondo)
    assignments = [oklab_dist_sq(pt, c1) <= oklab_dist_sq(pt, c2) for pt in ok_points]

    fg_rgb = oklab_to_rgb(*c1)
    bg_rgb = oklab_to_rgb(*c2)

    return (fg_rgb, bg_rgb, assignments, max_d2, mean_L)

# ==============================================================================
# 4. OPTIMIZADOR DE SECUENCIAS ANSI TRUECOLOR (ZERO LATENCY)
# ==============================================================================
# En lugar de escupir escapes ANSI redundantes en cada carácter (que saturan
# el búfer de la terminal y causan lentitud), Mary utiliza una máquina de estado
# que solo emite códigos de escape cuando el color cambia efectivamente.

class AnsiStreamBuilder:
    def __init__(self):
        self.lines = []
        self.current_line = []
        self.cur_fg = None
        self.cur_bg = None

    def emit_cell(self, char, fg=None, bg=None):
        out = []
        if fg is not None:
            if fg != self.cur_fg:
                out.append(f"\033[38;2;{fg[0]};{fg[1]};{fg[2]}m")
                self.cur_fg = fg
        else:
            if self.cur_fg is not None:
                out.append("\033[39m")
                self.cur_fg = None
        if bg is not None:
            if bg != self.cur_bg:
                out.append(f"\033[48;2;{bg[0]};{bg[1]};{bg[2]}m")
                self.cur_bg = bg
        else:
            if self.cur_bg is not None:
                out.append("\033[49m")
                self.cur_bg = None
        out.append(char)
        self.current_line.append("".join(out))

    def end_line(self):
        # Reset al final de línea para evitar desbordes visuales en el margen
        if self.cur_fg is not None or self.cur_bg is not None:
            self.current_line.append("\033[0m")
            self.cur_fg = None
            self.cur_bg = None
        self.lines.append("".join(self.current_line))
        self.current_line = []

    def get_output(self):
        if self.current_line:
            self.end_line()
        return "\n".join(self.lines)

# ==============================================================================
# 5. RENDERIZADORES DE ALTA DEFINICIÓN DE MARY 3.0 APEX
# ==============================================================================

# Matriz estándar de mapeo de bits Unicode Braille (2x4 micropuntos)
BRAILLE_DOT_MAP = [
    [0x01, 0x08],
    [0x02, 0x10],
    [0x04, 0x20],
    [0x40, 0x80]
]

# Glifos de Cuadrantes Unicode (2x2 subpíxeles)
QUADRANT_BLOCKS = [
    " ", "▘", "▝", "▀",
    "▖", "▌", "▞", "▛",
    "▗", "▚", "▐", "▜",
    "▄", "▙", "▟", "█"
]

# Glifos de Sextantes Unicode 13.0 (2x3 subpíxeles, 100% bloques sólidos)
SEXTANT_BLOCKS = [
    " ", "🬀", "🬁", "🬂", "🬃", "🬄", "🬅", "🬆",
    "🬇", "🬈", "🬉", "🬊", "🬋", "🬌", "🬍", "🬎",
    "🬏", "🬐", "🬑", "🬒", "🬓", "▌", "🬔", "🬕",
    "🬖", "🬗", "🬘", "🬙", "🬚", "🬛", "🬜", "🬝",
    "🬞", "🬟", "🬠", "🬡", "🬢", "🬣", "🬤", "🬥",
    "🬦", "🬧", "▐", "🬨", "🬩", "🬪", "🬫", "🬬",
    "🬭", "🬮", "🬯", "🬰", "🬱", "🬲", "🬳", "🬴",
    "🬵", "🬶", "🬷", "🬸", "🬹", "🬺", "🬻", "█"
]

def render_mary_sextants(image, width, font_ratio=0.5, invert=False):
    """
    Renderizador de Sextantes HD Mary 3.0 Apex (2x3 subpíxeles por celda, Unicode 13.0).
    Proporciona cobertura 100% sólida sin micropuntos ni perforaciones, con umbral
    adaptativo biofísico de Weber-Fechner y retención de bordes.
    """
    orig_w, orig_h = image.size
    aspect = orig_h / orig_w
    
    num_rows = int(round(width * aspect * font_ratio))
    sub_w = width * 2
    sub_h = num_rows * 3
    
    resample_filter = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
    scaled = image.resize((sub_w, sub_h), resample=resample_filter)
    
    pixels = list(scaled.getdata())
    stream = AnsiStreamBuilder()
    
    for row_idx in range(num_rows):
        y = row_idx * 3
        for x in range(0, sub_w, 2):
            cell_pixels = []
            cell_alphas = []
            
            for dy in range(3):
                for dx in range(2):
                    cur_x = x + dx
                    cur_y = y + dy
                    if cur_x < sub_w and cur_y < sub_h:
                        p = pixels[cur_y * sub_w + cur_x]
                        r, g, b, a = p[0], p[1], p[2], p[3] if len(p) > 3 else 255
                        cell_pixels.append((r, g, b))
                        cell_alphas.append(a)
                    else:
                        cell_pixels.append((0, 0, 0))
                        cell_alphas.append(0)
                        
            if all(a < 64 for a in cell_alphas):
                stream.emit_cell(" ", None, None)
                continue
                
            fg_col, bg_col, mask, max_delta_e, mean_L = cluster_cell_two_colors(cell_pixels)
            
            # Ley perceptual de Weber-Fechner: umbral adaptativo dependiente de la luminosidad
            tau = 0.0075 * (((mean_L + 0.08) / 0.58) ** 0.80)
            
            if max_delta_e < tau:
                stream.emit_cell(" ", None, bg_col)
            else:
                cnt_true = sum(1 for m in mask if m)
                if cnt_true > 3:
                    fg_col, bg_col = bg_col, fg_col
                    mask = [not m for m in mask]
                    
                code = 0
                for i in range(6):
                    if cell_alphas[i] >= 64 and (mask[i] != invert):
                        code |= (1 << i)
                        
                if code == 0:
                    stream.emit_cell(" ", None, bg_col)
                elif code == 63:
                    stream.emit_cell(" ", None, fg_col)
                else:
                    stream.emit_cell(SEXTANT_BLOCKS[code], fg_col, bg_col)
                    
        stream.end_line()
        
    return stream.get_output()

def render_mary_braille(image, width, font_ratio=0.5, invert=False):
    """
    Renderizador Braille Perceptual Dual-Color (8 subpíxeles por celda).
    Calcula simultáneamente el color del micropunto y el color del fondo de la celda.
    """
    orig_w, orig_h = image.size
    aspect = orig_h / orig_w
    
    num_rows = int(round(width * aspect * font_ratio))
    sub_w = width * 2
    sub_h = num_rows * 4
    
    resample_filter = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
    scaled = image.resize((sub_w, sub_h), resample=resample_filter)
    
    pixels = list(scaled.getdata())
    stream = AnsiStreamBuilder()
    
    for row_idx in range(num_rows):
        y = row_idx * 4
        for x in range(0, sub_w, 2):
            cell_pixels = []
            cell_alphas = []
            
            for dy in range(4):
                for dx in range(2):
                    cur_x = x + dx
                    cur_y = y + dy
                    if cur_x < sub_w and cur_y < sub_h:
                        p = pixels[cur_y * sub_w + cur_x]
                        r, g, b, a = p[0], p[1], p[2], p[3] if len(p) > 3 else 255
                        cell_pixels.append((r, g, b))
                        cell_alphas.append(a)
                    else:
                        cell_pixels.append((0, 0, 0))
                        cell_alphas.append(0)

            # Si todos los 8 subpíxeles son transparentes, emitir espacio vacío
            if all(a < 64 for a in cell_alphas):
                stream.emit_cell(" ", None, None)
                continue

            # Clustering Oklab para determinar Foreground y Background óptimos
            fg_col, bg_col, mask, max_delta_e, mean_L = cluster_cell_two_colors(cell_pixels)
            
            # Umbral adaptativo Weber-Fechner dependiente de luminosidad
            tau = 0.0075 * (((mean_L + 0.08) / 0.58) ** 0.80)
            
            if max_delta_e < tau:
                stream.emit_cell(" ", None, bg_col)
            else:
                # Alto contraste (borde, ojo, cabello, detalle fino) -> Braille Dual-Color
                # Minority-Cluster FG: los micropuntos siempre representan el detalle fino
                cnt_true = sum(1 for m in mask if m)
                if cnt_true > 4:
                    fg_col, bg_col = bg_col, fg_col
                    mask = [not m for m in mask]

                braille_code = 0
                has_opaque = False
                for dy in range(4):
                    for dx in range(2):
                        idx = dy * 2 + dx
                        if cell_alphas[idx] >= 64:
                            has_opaque = True
                            is_dot_on = mask[idx] != invert
                            if is_dot_on:
                                braille_code |= BRAILLE_DOT_MAP[dy][dx]

                if not has_opaque:
                    stream.emit_cell(" ", None, None)
                elif braille_code == 0:
                    stream.emit_cell(" ", None, bg_col)
                elif braille_code == 0xFF:
                    stream.emit_cell(" ", None, fg_col)
                else:
                    glyph = chr(0x2800 + braille_code)
                    stream.emit_cell(glyph, fg_col, bg_col)
                
        stream.end_line()
        
    return stream.get_output()

def render_mary_quadrants(image, width, font_ratio=0.5, invert=False):
    """
    Renderizador de Cuadrantes HD (2x2 subpíxeles por celda en TrueColor Dual).
    Utiliza los 16 glifos Unicode de cuadrante con primer plano y fondo independientes.
    """
    orig_w, orig_h = image.size
    aspect = orig_h / orig_w
    
    num_rows = int(round(width * aspect * font_ratio))
    sub_w = width * 2
    sub_h = num_rows * 2
    
    resample_filter = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
    scaled = image.resize((sub_w, sub_h), resample=resample_filter)
    
    pixels = list(scaled.getdata())
    stream = AnsiStreamBuilder()
    
    for row_idx in range(num_rows):
        y = row_idx * 2
        for x in range(0, sub_w, 2):
            cell_pixels = []
            cell_alphas = []
            
            coords = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
            for cx, cy in coords:
                if cx < sub_w and cy < sub_h:
                    p = pixels[cy * sub_w + cx]
                    r, g, b, a = p[0], p[1], p[2], p[3] if len(p) > 3 else 255
                    cell_pixels.append((r, g, b))
                    cell_alphas.append(a)
                else:
                    cell_pixels.append((0, 0, 0))
                    cell_alphas.append(0)

            if all(a < 64 for a in cell_alphas):
                stream.emit_cell(" ", None, None)
                continue

            fg_col, bg_col, mask, max_delta_e, mean_L = cluster_cell_two_colors(cell_pixels)
            
            tau = 0.0075 * (((mean_L + 0.08) / 0.58) ** 0.80)
            
            if max_delta_e < tau:
                stream.emit_cell(" ", None, bg_col)
            else:
                # Minority-Cluster FG en cuadrantes
                cnt_true = sum(1 for m in mask if m)
                if cnt_true > 2:
                    fg_col, bg_col = bg_col, fg_col
                    mask = [not m for m in mask]

                q_mask = 0
                for i, bit in enumerate([1, 2, 4, 8]):
                    if cell_alphas[i] >= 64:
                        if mask[i] != invert:
                            q_mask |= bit

                glyph = QUADRANT_BLOCKS[q_mask]
                stream.emit_cell(glyph, fg_col, bg_col)
            
        stream.end_line()
        
    return stream.get_output()

def render_mary_halfblocks(image, width, font_ratio=0.5):
    """
    Renderizador clásico de Medios Bloques de Alta Fidelidad (2 píxeles verticales por celda).
    Superior en foreground '▀', inferior en background.
    """
    orig_w, orig_h = image.size
    aspect = orig_h / orig_w
    
    num_rows = int(round(width * aspect * font_ratio))
    target_w = width
    target_h = num_rows * 2
    
    resample_filter = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
    scaled = image.resize((target_w, target_h), resample=resample_filter)
    
    pixels = list(scaled.getdata())
    stream = AnsiStreamBuilder()
    
    for row_idx in range(num_rows):
        y = row_idx * 2
        for x in range(target_w):
            top_p = pixels[y * target_w + x]
            bot_p = pixels[(y + 1) * target_w + x]
            
            top_a = top_p[3] if len(top_p) > 3 else 255
            bot_a = bot_p[3] if len(bot_p) > 3 else 255
            
            top_rgb = (top_p[0], top_p[1], top_p[2])
            bot_rgb = (bot_p[0], bot_p[1], bot_p[2])
            
            if top_a < 64 and bot_a < 64:
                stream.emit_cell(" ", None, None)
            elif top_a >= 64 and bot_a < 64:
                stream.emit_cell("▀", top_rgb, None)
            elif top_a < 64 and bot_a >= 64:
                stream.emit_cell("▄", bot_rgb, None)
            else:
                stream.emit_cell("▀", top_rgb, bot_rgb)
                
        stream.end_line()
        
    return stream.get_output()

def render_mary_ascii(image, width, font_ratio=0.5, invert=False):
    """
    Renderizador ASCII Perceptual con Análisis Direccional de Bordes (Sobel/Scharr).
    Mapea contornos direccionales a '/', '\\', '|', '-', '_', '+', y densidades Oklab.
    """
    orig_w, orig_h = image.size
    aspect = orig_h / orig_w
    
    target_w = width
    target_h = int(round(target_w * aspect * font_ratio))
    
    resample_filter = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
    scaled = image.resize((target_w, target_h), resample=resample_filter)
    
    gray = scaled.convert("L")
    g_pix = list(gray.getdata())
    rgba_pix = list(scaled.getdata())
    
    # Rampa perceptual de 16 niveles de densidad
    RAMP = " .:-=+*#%@MWB8&"
    if invert:
        RAMP = RAMP[::-1]
        
    stream = AnsiStreamBuilder()
    
    for y in range(target_h):
        for x in range(target_w):
            idx = y * target_w + x
            p = rgba_pix[idx]
            a = p[3] if len(p) > 3 else 255
            
            if a < 64:
                stream.emit_cell(" ", None, None)
                continue
                
            rgb = (p[0], p[1], p[2])
            
            # Cálculo de gradiente direccional mediante kernel Sobel 3x3
            gx = 0
            gy = 0
            if 0 < x < target_w - 1 and 0 < y < target_h - 1:
                gx = (g_pix[idx + 1] - g_pix[idx - 1]) * 2 + \
                     (g_pix[(y - 1) * target_w + (x + 1)] - g_pix[(y - 1) * target_w + (x - 1)]) + \
                     (g_pix[(y + 1) * target_w + (x + 1)] - g_pix[(y + 1) * target_w + (x - 1)])
                     
                gy = (g_pix[(y + 1) * target_w + x] - g_pix[(y - 1) * target_w + x]) * 2 + \
                     (g_pix[(y + 1) * target_w + (x - 1)] - g_pix[(y - 1) * target_w + (x - 1)]) + \
                     (g_pix[(y + 1) * target_w + (x + 1)] - g_pix[(y - 1) * target_w + (x + 1)])

            grad_mag = math.sqrt(gx * gx + gy * gy)
            
            # Si el gradiente es fuerte, asignar glifo direccional
            if grad_mag > 130.0:
                angle = math.degrees(math.atan2(gy, gx))
                if -22.5 <= angle <= 22.5 or angle >= 157.5 or angle <= -157.5:
                    glyph = "|"  # Borde vertical
                elif 67.5 <= abs(angle) <= 112.5:
                    glyph = "-"  # Borde horizontal
                elif 22.5 < angle < 67.5 or -157.5 < angle < -112.5:
                    glyph = "\\" # Diagonal positiva
                else:
                    glyph = "/"  # Diagonal negativa
            else:
                # Luminancia Oklab para mapeo continuo de densidad
                ok_L, _, _ = rgb_to_oklab(*rgb)
                ramp_idx = int(ok_L * (len(RAMP) - 1))
                ramp_idx = max(0, min(len(RAMP) - 1, ramp_idx))
                glyph = RAMP[ramp_idx]

            stream.emit_cell(glyph, rgb, None)
            
        stream.end_line()
        
    return stream.get_output()

# ==============================================================================
# 6. PUNTO DE ENTRADA PRINCIPAL DEL MOTOR MARY 3.0 APEX
# ==============================================================================

def render_mary(image, width, mode="sextants", raw_colors=False, invert=False, font_ratio=0.5):
    """
    Punto de entrada maestro para el motor Mary 3.0 Apex:
    - Preprocesamiento perceptual adaptativo (Auto-HDR).
    - Despacho al modo solicitado (sextants, braille, blocks, quadrants, ascii).
    - Compresión de flujo ANSI TrueColor.
    """
    # 1. Adaptación semántica de luminancia y color
    enhanced = adapt_perceptual_tone_and_color(image, raw_colors=raw_colors)
    
    # 2. Despacho según modo de subpíxel
    mode_lower = mode.lower() if mode else "sextants"
    if mode_lower in ("sextants", "sextant", "s"):
        return render_mary_sextants(enhanced, width, font_ratio=font_ratio, invert=invert)
    elif mode_lower in ("braille", "hybrid", "super", "b"):
        return render_mary_braille(enhanced, width, font_ratio=font_ratio, invert=invert)
    elif mode_lower in ("quadrants", "quadrant", "q"):
        return render_mary_quadrants(enhanced, width, font_ratio=font_ratio, invert=invert)
    elif mode_lower in ("blocks", "block", "k"):
        return render_mary_halfblocks(enhanced, width, font_ratio=font_ratio)
    elif mode_lower in ("ascii", "a"):
        return render_mary_ascii(enhanced, width, font_ratio=font_ratio, invert=invert)
    else:
        # Por defecto Sextantes HD de alta definición sólida
        return render_mary_sextants(enhanced, width, font_ratio=font_ratio, invert=invert)


#!/usr/bin/env python3
import argparse
import sys
import locale
import os
try:
    from PIL import Image, ImageEnhance
except ImportError:
    import subprocess
    print("[luma] Pillow no encontrado. Instalando dependencias...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "Pillow", "-q"]
    )
    from PIL import Image, ImageEnhance

# Extended ASCII character set for better shading (from darkest to lightest)
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

COLOR_MAP = {
    "red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255),
    "yellow": (255, 255, 0), "purple": (128, 0, 128), "pink": (255, 192, 203),
    "cyan": (0, 255, 255), "orange": (255, 165, 0), "white": (255, 255, 255),
    "black": (0, 0, 0), "gray": (128, 128, 128), "magenta": (255, 0, 255)
}

TRANSLATIONS = {
    "en": {
        "pillow_not_found": "[luma] Pillow not found. Installing dependencies...",
        "usage": "Usage: lumart [options] <image_path>\n\nTry 'lumart --help' for more options.",
        "desc": "Lumart - Epic Terminal Art Engine",
        "help_image_path": "Path to the input image file.",
        "help_width": "Width of the output ASCII art (in characters). Default: 100",
        "help_color": "Output ASCII art in color.",
        "help_invert": "Invert the ASCII characters (useful for dark terminals).",
        "help_output": "Save the ASCII art to a file instead of printing to the console.",
        "help_binary": "Use only 1s and 0s for the ASCII characters.",
        "help_blocks": "Use half-blocks for high resolution true-color (overrides binary and ascii).",
        "help_braille": "Use Braille characters for smooth edges and high resolution shape (overrides binary).",
        "help_epic": "(Deprecated) Epic Color Engine is now enabled by default.",
        "help_raw_colors": "Disable the Epic Color Engine and use the original raw image colors.",
        "help_os_style": "Use classic Neofetch/OS style characters (dots, letters, shapes).",
        "help_swap": "Swap colors using names (e.g. --swap purple pink blue red). Must provide an even number of arguments.",
        "help_lang": "Force a specific language (en, es).",
        "error_open": "Error opening image: {}",
        "error_swap": "Error: --swap requires pairs of colors (e.g. --swap purple pink).",
        "saved_to": "ASCII art saved to {}",
        "error_save": "Error saving to file: {}"
    },
    "es": {
        "pillow_not_found": "[luma] Pillow no encontrado. Instalando dependencias...",
        "usage": "Uso: lumart [opciones] <ruta_imagen>\n\nIntenta 'lumart --help' para más opciones.",
        "desc": "Lumart - Motor Épico de Arte de Terminal",
        "help_image_path": "Ruta al archivo de imagen de entrada.",
        "help_width": "Ancho del arte ASCII de salida (en caracteres). Por defecto: 100",
        "help_color": "Generar arte ASCII en color.",
        "help_invert": "Invertir los caracteres ASCII (útil para terminales oscuras).",
        "help_output": "Guardar el arte ASCII en un archivo en lugar de imprimirlo en consola.",
        "help_binary": "Usar solo 1s y 0s para los caracteres ASCII.",
        "help_blocks": "Usar medio-bloques para alta resolución (sobrescribe binary y ascii).",
        "help_braille": "Usar caracteres Braille para bordes suaves y formas de alta resolución.",
        "help_epic": "(Obsoleto) El Motor Épico de Color ahora está activado por defecto.",
        "help_raw_colors": "Desactiva el Motor Épico y utiliza los colores originales sin procesar.",
        "help_os_style": "Usar caracteres clásicos estilo Neofetch/OS (puntos, letras, formas).",
        "help_swap": "Intercambiar colores por nombre (ej. --swap purple pink blue red). Debe ser un número par de argumentos.",
        "help_lang": "Forzar un idioma específico (en, es).",
        "error_open": "Error abriendo imagen: {}",
        "error_swap": "Error: --swap requiere pares de colores (ej: --swap purple pink).",
        "saved_to": "Arte ASCII guardado en {}",
        "error_save": "Error guardando en archivo: {}"
    }
}

CURRENT_LANG = "en"

def set_language(lang_code):
    global CURRENT_LANG
    if lang_code in TRANSLATIONS:
        CURRENT_LANG = lang_code
    elif lang_code and lang_code.startswith("es"):
        CURRENT_LANG = "es"
    else:
        CURRENT_LANG = "en"

def _(key, *args):
    text = TRANSLATIONS.get(CURRENT_LANG, TRANSLATIONS["en"]).get(key, TRANSLATIONS["en"].get(key, key))
    if args:
        return text.format(*args)
    return text

def auto_detect_language():
    try:
        lang, _ = locale.getdefaultlocale()
        if lang:
            set_language(lang[:2])
    except Exception:
        pass

def apply_color_swap(image, swap_args):
    if not swap_args or len(swap_args) % 2 != 0:
        return image
        
    swaps = []
    for i in range(0, len(swap_args), 2):
        src_name = swap_args[i].lower()
        dst_name = swap_args[i+1].lower()
        if src_name in COLOR_MAP and dst_name in COLOR_MAP:
            swaps.append((COLOR_MAP[src_name], COLOR_MAP[dst_name]))
            
    if not swaps:
        return image
        
    img = image.convert("RGBA")
    pixels = img.load()
    width, height = img.size
    
    # Euclidean distance threshold (out of max distance ~441)
    THRESHOLD = 150
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a == 0: continue
            
            for src_rgb, dst_rgb in swaps:
                dist = ((r - src_rgb[0])**2 + (g - src_rgb[1])**2 + (b - src_rgb[2])**2)**0.5
                if dist < THRESHOLD:
                    # Blend towards destination color based on brightness
                    orig_brightness = max((r + g + b) / 765.0, 0.05)
                    dst_brightness = max((dst_rgb[0] + dst_rgb[1] + dst_rgb[2]) / 765.0, 0.05)
                    
                    ratio = orig_brightness / dst_brightness
                    new_r = min(255, int(dst_rgb[0] * ratio))
                    new_g = min(255, int(dst_rgb[1] * ratio))
                    new_b = min(255, int(dst_rgb[2] * ratio))
                    
                    pixels[x, y] = (new_r, new_g, new_b, a)
                    break
                    
    return img

def resize_image(image, new_width=100, is_blocks=False, is_braille=False):
    """
    Resizes the image while maintaining aspect ratio, using mathematically perfect Lanczos resampling.
    """
    width, height = image.size
    aspect_ratio = height / width
    
    # Use high-quality resampling filter
    resample_filter = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
    
    if is_braille:
        target_pixel_width = new_width * 2
        target_pixel_height = int(target_pixel_width * aspect_ratio)
        target_pixel_height = target_pixel_height + (4 - target_pixel_height % 4) % 4
        return image.resize((target_pixel_width, target_pixel_height), resample=resample_filter)
    elif is_blocks:
        # Quadrant blocks: 2x2 pixels per character for maximum geometry
        # Terminal characters are twice as tall as they are wide.
        # To maintain aspect ratio, we must squish the image vertically by 0.5.
        target_pixel_width = new_width * 2
        target_pixel_height = int(target_pixel_width * aspect_ratio * 0.5)
        target_pixel_height = target_pixel_height + (2 - target_pixel_height % 2) % 2
        return image.resize((target_pixel_width, target_pixel_height), resample=resample_filter)
    else:
        new_height = int(new_width * aspect_ratio * 0.5)
        return image.resize((new_width, new_height), resample=resample_filter)

def get_ansi_color_code(r, g, b):
    """
    Returns the ANSI escape sequence for 24-bit (True Color) foreground color.
    """
    return f"\033[38;2;{r};{g};{b}m"

def reset_ansi_color_code():
    """
    Returns the ANSI escape sequence to reset colors.
    """
    return "\033[0m"

def convert_image_to_blocks(image):
    """
    Converts an image using Smart Quadrants (2x2 subpixels).
    Uses Exhaustive RMSE (Root Mean Square Error) minimization in Premultiplied 4D RGBA space
    to mathematically guarantee the highest possible geometric precision and anti-aliasing.
    """
    # Ensure image is RGBA
    img = image.convert("RGBA")
    width, height = img.size
    
    # 2x2 bit mapping: TL=1, TR=2, BL=4, BR=8
    quad_map = {
        0: " ", 1: "▘", 2: "▝", 3: "▀", 
        4: "▖", 5: "▌", 6: "▞", 7: "▛", 
        8: "▗", 9: "▚", 10: "▐", 11: "▜", 
        12: "▄", 13: "▙", 14: "▟", 15: "█"
    }
    
    # Pre-multiply alpha for mathematical correctness
    pixels_data = img.load()
    pm_pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b, a = pixels_data[x, y]
            alpha = a / 255.0
            row.append((r * alpha, g * alpha, b * alpha, a))
        pm_pixels.append(row)
        
    def from_premult(pm):
        r_p, g_p, b_p, a = pm
        if a == 0: return (0, 0, 0, 0)
        alpha = a / 255.0
        return (int(r_p / alpha), int(g_p / alpha), int(b_p / alpha), int(a))
        
    ascii_str = ""
    for y in range(0, height, 2):
        for x in range(0, width, 2):
            P = []
            for dy in range(2):
                for dx in range(2):
                    if x+dx < width and y+dy < height:
                        P.append(pm_pixels[y+dy][x+dx])
                    else:
                        P.append((0, 0, 0, 0))
            
            best_shape = 0
            min_error = float('inf')
            best_fg_pm = (0,0,0,0)
            best_bg_pm = (0,0,0,0)
            
            # Exhaustive search over all 16 quadrant combinations
            for shape in range(16):
                fg_indices = [i for i in range(4) if (shape & (1 << i))]
                bg_indices = [i for i in range(4) if not (shape & (1 << i))]
                
                fg_pm = (0,0,0,0)
                if fg_indices:
                    fg_pm = (
                        sum(P[i][0] for i in fg_indices) / len(fg_indices),
                        sum(P[i][1] for i in fg_indices) / len(fg_indices),
                        sum(P[i][2] for i in fg_indices) / len(fg_indices),
                        sum(P[i][3] for i in fg_indices) / len(fg_indices)
                    )
                
                bg_pm = (0,0,0,0)
                if bg_indices:
                    bg_pm = (
                        sum(P[i][0] for i in bg_indices) / len(bg_indices),
                        sum(P[i][1] for i in bg_indices) / len(bg_indices),
                        sum(P[i][2] for i in bg_indices) / len(bg_indices),
                        sum(P[i][3] for i in bg_indices) / len(bg_indices)
                    )
                
                error = 0
                for i in fg_indices:
                    error += (P[i][0]-fg_pm[0])**2 + (P[i][1]-fg_pm[1])**2 + (P[i][2]-fg_pm[2])**2 + (P[i][3]-fg_pm[3])**2
                for i in bg_indices:
                    error += (P[i][0]-bg_pm[0])**2 + (P[i][1]-bg_pm[1])**2 + (P[i][2]-bg_pm[2])**2 + (P[i][3]-bg_pm[3])**2
                    
                # Significant penalty to favor pure solid blocks over 2-color shapes.
                # This prevents subpixel noise (overfitting) in smooth gradients.
                if shape not in (0, 15):
                    error += 2000
                    
                if error < min_error:
                    min_error = error
                    best_shape = shape
                    best_fg_pm = fg_pm
                    best_bg_pm = bg_pm

            fg_rgba = from_premult(best_fg_pm)
            bg_rgba = from_premult(best_bg_pm)
            
            fg_opaque = fg_rgba[3] >= 128
            bg_opaque = bg_rgba[3] >= 128
            
            color_code = reset_ansi_color_code()
            
            # Print logic using shape inversion to allow terminal background to show through perfectly
            if fg_opaque and bg_opaque:
                char = quad_map[best_shape]
                color_code += f"\033[38;2;{fg_rgba[0]};{fg_rgba[1]};{fg_rgba[2]}m"
                color_code += f"\033[48;2;{bg_rgba[0]};{bg_rgba[1]};{bg_rgba[2]}m"
                ascii_str += color_code + char
            elif fg_opaque and not bg_opaque:
                char = quad_map[best_shape]
                color_code += f"\033[38;2;{fg_rgba[0]};{fg_rgba[1]};{fg_rgba[2]}m"
                ascii_str += color_code + char
            elif not fg_opaque and bg_opaque:
                inv_shape = 15 - best_shape
                char = quad_map[inv_shape]
                color_code += f"\033[38;2;{bg_rgba[0]};{bg_rgba[1]};{bg_rgba[2]}m"
                ascii_str += color_code + char
            else:
                ascii_str += color_code + " "
                
        ascii_str += reset_ansi_color_code() + "\n"
        
    return ascii_str

def _srgb_to_linear(c):
    """Convert sRGB channel [0,255] to linear light [0,1]."""
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def _linear_to_srgb(c):
    """Convert linear light [0,1] to sRGB [0,255]."""
    c = max(0.0, min(1.0, c))
    return round((c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1/2.4) - 0.055) * 255)

def convert_image_to_braille(image, use_color=False):
    """
    Combines Unicode Braille (for smooth anti-aliased curves and high-contrast details)
    with Half-blocks (▀) for solid, gap-less gradients.
    """
    has_alpha = image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info)
    img = image.convert("RGBA") if has_alpha else image.convert("RGB")
    
    width, height = img.size
    
    dot_map = [
        [0x01, 0x08],
        [0x02, 0x10],
        [0x04, 0x20],
        [0x40, 0x80]
    ]
    
    def color_dist(c1, c2):
        return (c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2
    
    ascii_str = ""
    for y in range(0, height, 4):
        for x in range(0, width, 2):
            pixels = []
            has_transparent = False
            
            for dy in range(4):
                row = []
                for dx in range(2):
                    px = x + dx
                    py = y + dy
                    if px < width and py < height:
                        p = img.getpixel((px, py))
                        is_transp = has_alpha and p[3] < 128
                        if is_transp:
                            has_transparent = True
                        row.append((p[:3], is_transp))
                    else:
                        row.append(((0,0,0), True))
                        has_transparent = True
                pixels.append(row)
                
            braille_val = 0
            
            if has_transparent:
                # Edge/transparent block: use Braille for smooth 2x4 shapes
                fg_pixels = []
                for dy in range(4):
                    for dx in range(2):
                        color, is_transp = pixels[dy][dx]
                        if not is_transp:
                            braille_val += dot_map[dy][dx]
                            fg_pixels.append(color)
                            
                if braille_val == 0:
                    ascii_str += reset_ansi_color_code() + " "
                else:
                    char = chr(0x2800 + braille_val)
                    if use_color and fg_pixels:
                        lr = sum(_srgb_to_linear(p[0]) for p in fg_pixels) / len(fg_pixels)
                        lg = sum(_srgb_to_linear(p[1]) for p in fg_pixels) / len(fg_pixels)
                        lb = sum(_srgb_to_linear(p[2]) for p in fg_pixels) / len(fg_pixels)
                        avg_r, avg_g, avg_b = _linear_to_srgb(lr), _linear_to_srgb(lg), _linear_to_srgb(lb)
                        ascii_str += reset_ansi_color_code() + f"\033[38;2;{avg_r};{avg_g};{avg_b}m" + char
                    else:
                        ascii_str += char
            else:
                # Fully opaque interior block: use Half-block ▀ for solid colors (no dot gaps)
                top_pixels = [pixels[dy][dx][0] for dy in (0,1) for dx in (0,1)]
                bottom_pixels = [pixels[dy][dx][0] for dy in (2,3) for dx in (0,1)]
                
                char = "▀"
                if use_color:
                    tlr = sum(_srgb_to_linear(p[0]) for p in top_pixels) / 4
                    tlg = sum(_srgb_to_linear(p[1]) for p in top_pixels) / 4
                    tlb = sum(_srgb_to_linear(p[2]) for p in top_pixels) / 4
                    tr, tg, tb = _linear_to_srgb(tlr), _linear_to_srgb(tlg), _linear_to_srgb(tlb)
                    
                    blr = sum(_srgb_to_linear(p[0]) for p in bottom_pixels) / 4
                    blg = sum(_srgb_to_linear(p[1]) for p in bottom_pixels) / 4
                    blb = sum(_srgb_to_linear(p[2]) for p in bottom_pixels) / 4
                    br, bg, bb = _linear_to_srgb(blr), _linear_to_srgb(blg), _linear_to_srgb(blb)
                    
                    ascii_str += f"\033[38;2;{tr};{tg};{tb}m\033[48;2;{br};{bg};{bb}m" + char
                else:
                    ascii_str += char
                    
        ascii_str += reset_ansi_color_code() + "\n"
        
    return ascii_str

def convert_image_to_ascii(image, use_color=False, invert=False, binary=False, os_style=False):
    """
    Converts an image to an ASCII string (with optional color and inversion).
    """
    grayscale_image = image.convert("L")
    rgb_image = image.convert("RGB")
    
    # Check if image has transparency
    has_alpha = image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info)
    rgba_image = image.convert("RGBA") if has_alpha else None
    
    ascii_str = ""
    width, height = image.size
    
    if binary:
        base_chars = "01"
    elif os_style:
        base_chars = " .-+*=#%@WM"
    else:
        base_chars = ASCII_CHARS
    
    chars = base_chars[::-1] if invert else base_chars
    
    for y in range(height):
        for x in range(width):
            if has_alpha:
                _, _, _, a = rgba_image.getpixel((x, y))
                if a < 128:  # Transparent pixel
                    ascii_str += " "
                    continue
            
            grayscale_pixel = grayscale_image.getpixel((x, y))
            
            # Map pixel to index
            index = round(grayscale_pixel / 255 * (len(chars) - 1))
            char = chars[index]
            
            if use_color:
                r, g, b = rgb_image.getpixel((x, y))
                ascii_str += get_ansi_color_code(r, g, b) + char
            else:
                ascii_str += char
        
        # Reset color at the end of each row if using color, and add newline
        if use_color:
            ascii_str += reset_ansi_color_code()
        ascii_str += "\n"
        
    return ascii_str

def main():
    # First pass to just detect the --lang argument early, before argparse initializes its strings
    lang_override = None
    if "--lang" in sys.argv:
        try:
            lang_idx = sys.argv.index("--lang")
            lang_override = sys.argv[lang_idx + 1]
        except IndexError:
            pass
            
    if lang_override:
        set_language(lang_override)
    else:
        auto_detect_language()

    banner = """\033[1;36m
 █    █ █ █▄ ▄█ ▄▀▄ █▀▄ ▀█▀
 █▄▄▄ ▀▄█ █ ▀ █ █▀█ █▀▄  █
 \033[0;36mv2.0.0 - Epic Terminal Art Engine\033[0m
"""
    
    # Custom help and banner intercept
    if len(sys.argv) == 1:
        print(banner)
        print(_("usage"))
        sys.exit(1)

    parser = argparse.ArgumentParser(prog="lumart", description=_( "desc" ))
    parser.add_argument("-v", "--version", action="version", version=f"{banner}")

    parser.add_argument("image_path", help=_("help_image_path"))
    parser.add_argument("-w", "--width", type=int, default=100, help=_("help_width"))
    parser.add_argument("-c", "--color", action="store_true", help=_("help_color"))
    parser.add_argument("-i", "--invert", action="store_true", help=_("help_invert"))
    parser.add_argument("-o", "--output", help=_("help_output"))
    parser.add_argument("-b", "--binary", action="store_true", help=_("help_binary"))
    parser.add_argument("--blocks", action="store_true", help=_("help_blocks"))
    parser.add_argument("--braille", action="store_true", help=_("help_braille"))
    parser.add_argument("--epic", action="store_true", help=_("help_epic"))
    parser.add_argument("--raw-colors", action="store_true", help=_("help_raw_colors"))
    parser.add_argument("--os-style", action="store_true", help=_("help_os_style"))
    parser.add_argument("--swap", nargs="+", help=_("help_swap"))
    parser.add_argument("--lang", help=_("help_lang"))
    
    args = parser.parse_args()
    
    try:
        image = Image.open(args.image_path)
    except Exception as e:
        print(_("error_open", e))
        sys.exit(1)
        
    if args.swap:
        if len(args.swap) % 2 != 0:
            print(_("error_swap"))
            sys.exit(1)
        image = apply_color_swap(image, args.swap)

    # Epic Color Engine is now default!
    if not args.raw_colors:
        # Convert to RGBA first because ImageEnhance fails on palettized ('P' mode) images
        image = image.convert("RGBA")
        image = ImageEnhance.Color(image).enhance(1.5)
        image = ImageEnhance.Contrast(image).enhance(1.2)
        image = ImageEnhance.Sharpness(image).enhance(1.5)

    image = resize_image(image, args.width, is_blocks=args.blocks, is_braille=args.braille)
    
    if args.braille:
        ascii_art = convert_image_to_braille(image, args.color)
    elif args.blocks:
        ascii_art = convert_image_to_blocks(image)
    else:
        ascii_art = convert_image_to_ascii(image, args.color, args.invert, args.binary, args.os_style)
    
    if args.output:
        try:
            with open(args.output, "w") as f:
                f.write(ascii_art)
            print(_("saved_to", args.output))
        except Exception as e:
            print(_("error_save", e))
    else:
        print(ascii_art)

if __name__ == "__main__":
    main()

[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

# Luma

**Un motor de renderizado de imagen a terminal de alta fidelidad escrito en Python y C/C++ moderno.**

Luma es un motor de renderizado de terminal de código abierto centrado en un único objetivo:

> **Máxima fidelidad visual en el mínimo espacio de terminal.**

A diferencia de los conversores ASCII tradicionales que simplemente mapean el brillo de la imagen a caracteres, Luma explora diferentes sistemas de glifos de terminal, matemáticas de color RGB Lineal y algoritmos nativos de visión artificial en C/C++ para preservar la mayor cantidad de información visual posible dentro de un número limitado de celdas de terminal.

## Características

* Renderizado de imágenes de alta fidelidad en la terminal
* Renderizado basado en ASCII, Braille, Cuadrantes 2x2 y Medios Bloques
* **Arquitectura de Tres Motores Especializados (`-E`, `--engine`)**:
  * **Mary 3.0 Apex (Buque Insignia de Color - C++17 Nativo & Python Fallback)**: Cero IA, 100% óptica computacional y biofísica de conos retinianos humanos. Acelerado en C++17 multihilo OpenMP con SIMD (`libmary.so` y binario `luma-mary`). Incorpora Filtro Guiado Rápido $O(1)$ en espacio de color Oklab ($\Delta E$), umbral adaptativo perceptual Weber-Fechner ($\tau = 0.0075 \times ((L + 0.08)/0.58)^{0.80}$), Sextantes Unicode 2x3 (`-S`, 64 bloques sólidos subpíxel), Braille 2x4 dual-color (`-B`), Cuadrantes 2x2 (`-Q`) y compresor de flujo ANSI con estado de latencia cero.
  * **Trumble (Motor de Color Clásico)**: El motor clásico original y probado en batalla. Mezcla en espacio de color lineal ($C_{\text{lineal}} = C_{\text{srgb}}^{2.2}$), remuestreo Lanczos, tramado ordenado Bayer y TrueColor ANSI de 24 bits. 100% preservado e intacto.
  * **Luris (Motor Monocromático y Manga Nativo C++17)**: Ejecución en menos de 10 milisegundos, extracción de trazos finos con Diferencia de Gaussianas (DoG), difusión de error Atkinson (MacPaint 1984), tramas de semitono Bayer 8x8 (*Ami-tone*) y bloques cuadrantes HD 2x2.
* **Selector de Motor (`-E`, `--engine`)**: Alterna dinámicamente entre `mary`, `trumble` y `luris` (con alias compatibles: `color`, `mono`, `bw`, `manga`, `sketch`).
* **Bloques Sextantes Unicode 2x3 (`-S`, `--sextants`)**: 6 subpíxeles por celda usando la tabla de 64 sextantes Unicode 13.0 (`🬀`-`🬻`, `█`, `▌`, `▐`). Renderizador insignia de Mary para gráficos sólidos e impecables en terminal.
* **Modo Boceto de Trazo Puro (`-s`, `-E sketch`)**: Extracción de contornos limpios sin ruido para anime e ilustraciones.
* **Manga Screentone 2.0 (`-m`, `-E manga`)**: Auténticas tramas de impresión de cómic japonés para tonos medios con blancos de papel puros y tinta negra sólida.
* **Tramado Atkinson y Halftone (`-d` / `--dither`)**: Soporta `atkinson`, `floyd`, `bayer` y `none`.
* **Bloques Cuadrantes HD 2x2 (`--quadrants`, `--blocks`)**: 4 subpíxeles por celda usando caracteres de cuadrante Unicode (`▘▝▀▖▌▞▛▗▚▐▜▄▙▟█`).
* **Renderizado Estilo OS (`--os-style`)**: Caracteres de terminal clásicos (puntos, letras) para logotipos al estilo Neofetch.
* **Intercambio de Color en Tiempo Real (`--swap`)**: Intercambia dinámicamente colores basados en distancia de color Euclidiana en 3D.
* **Cero Dependencias Externas Nativas**: El motor C++ está autocontenido con cabeceras libres de dominio público (`stb_image.h` y `stb_image_resize2.h`). No requiere OpenCV ni libpng.
* **Paridad Total con Fallback en Python**: Si un sistema no cuenta con compilador C++, Luma conmuta a la implementación pura en Python sin romperse.
* Ancho de salida configurable y autodetección de fondos claros/oscuros (`-i`, `--invert`)
* Suite interactiva de actualización (`-uu`), restauración/downgrade (`-dg`) y chequeo (`-u`)
* Panel de diagnóstico integral del sistema y motores (`-v`, `--version`)

## Ejemplo

```bash
# Convierte una imagen usando caracteres Braille, colores, y reemplazando el púrpura por el rosa
luma image.png -w 45 --braille -c --swap purple pink
```

## Instalación

Puedes instalar Luma con un solo comando, ejecutarlo directamente desde el código fuente o compilarlo en un paquete nativo de Linux (DEB, RPM, o Arch PKGBUILD).

**Instalación Rápida (Recomendado):**
```bash
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

**Opción 1: Ejecutar directamente desde el código fuente / Instalador local**
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
./install.sh
```

**Opción 2: Descargar Paquetes Precompilados**
Puedes descargar los paquetes `.deb` o `.rpm` listos para usar directamente desde la página de [GitHub Releases](https://github.com/SilentBlox01/Luma/releases).

**Opción 3: Compilar y construir los paquetes nativos tú mismo**
Luma incluye un script de construcción automático para empaquetar la herramienta en un binario independiente utilizando PyInstaller.
```bash
chmod +x build_packages.sh
./build_packages.sh
```
Después de compilar, puedes instalarlo globalmente a través de tu administrador de paquetes:
- **Debian/Ubuntu**: `sudo apt install ./dist/lumart-*.deb`
- **Fedora/RHEL**: `sudo dnf install ./dist/lumart-*.rpm`
- **Arch Linux**: `cd dist/arch && makepkg -si`

**Opción 4: Compilación manual del motor nativo C++**
Si solo deseas compilar el motor nativo en C++ sin construir paquetes completos:
```bash
# Binario CLI independiente:
g++ -O3 -std=c++17 monochrome.cpp -o luma-mono

# Librería compartida (para aceleración en proceso vía ctypes desde Python):
g++ -O3 -std=c++17 -fPIC -shared monochrome.cpp -o libmonochrome.so
```
*(Sin dependencias externas pesadas — utiliza las cabeceras embebidas `stb_image.h` y `stb_image_resize2.h`)*

## Uso

Si instalaste el paquete o utilizaste el instalador, puedes ejecutar `lumart` o `luma` desde cualquier directorio. De lo contrario, ejecuta el script de python directamente.

> **💡 Consejo Pro:** ¡Luma funciona de maravilla con imágenes sin fondo (transparentes)! El motor ignora automáticamente los píxeles transparentes, lo que hace que los logos y personajes resalten perfectamente contra el fondo de tu terminal.

```bash
# Uso básico
python3 lumart.py image.png
```

Especificar el ancho de salida (en caracteres):
```bash
python3 lumart.py image.png -w 30
```

Renderizar con el buque insignia Mary 3.0 Apex en Sextantes 2x3 (Bloques Sólidos, por defecto):
```bash
python3 lumart.py image.png -E mary -S -w 80
```

Renderizar con Mary en Braille Oklab con K-Means dual (Subpíxeles 2x4):
```bash
python3 lumart.py image.png -E mary -B -w 80
```

Renderizar con Mary en Bloques Cuadrantes HD 2x2 (color de fondo y frente TrueColor):
```bash
python3 lumart.py image.png -E mary -Q -w 80
```

Renderizar con el Motor Clásico Trumble (RGB Lineal 2.2):
```bash
python3 lumart.py image.png -E trumble --braille -w 80
```

Renderizar en Modo Boceto de Trazo Puro (contornos nítidos DoG sin ruido):
```bash
python3 lumart.py image.png -E sketch -w 100
# o: python3 lumart.py image.png -s -w 100
```

Renderizar con el motor Manga Screentone 2.0 (trazos DoG + retícula Bayer 8x8 inteligente):
```bash
python3 lumart.py image.png -E manga -w 120
# o: python3 lumart.py image.png -m -w 120
```

Renderizar en monocromático con Tramado Atkinson (difusión de error de MacPaint 1984):
```bash
python3 lumart.py image.png -E mono -d atkinson -w 100
# o floyd-steinberg clásico: python3 lumart.py image.png -E mono -d floyd -w 100
```

Renderizar en Bloques Cuadrantes HD (2x2 subpíxeles por celda en B&W):
```bash
python3 lumart.py image.png -E mono --blocks -w 80
```

Renderizar en monocromático puro sin colores:
```bash
python3 lumart.py image.png -E mono --braille -w 100
```

Forzar renderizado de caracteres estilo OS retro (útil para logotipos de SO):
```bash
python3 lumart.py image.png --os-style -c
```

Mostrar Diagnóstico Completo del Sistema y Motores:
```bash
luma -v
# o: luma --version
```

## Actualizaciones y Rollback

Luma te da control explícito sobre las actualizaciones y restauraciones:

- **Comprobar si hay actualizaciones (sin descargar ni tocar nada):**
  ```bash
  luma -u
  # o: luma --update / luma --check-update
  ```
  *(Muestra tu versión actual, la última versión en GitHub, historial de versiones y estado)*

- **Actualización Interactiva:**
  ```bash
  luma -uu
  # o: luma --upgrade
  ```
  *(Permite seleccionar a qué versión subir o instalar la última con notas de versión, guardando backup en `~/.config/luma/backup/`)*

- **Restauración Interactiva / Downgrade:**
  ```bash
  luma -dg
  # o: luma --downgrade / luma --rollback
  ```
  *(Abre un selector interactivo en la terminal para elegir entre copias locales de seguridad o versiones publicadas en GitHub)*

  También puedes especificar la versión directamente:
  ```bash
  luma -dg 2.1.0
  ```

Además, Luma comprueba periódicamente en segundo plano si existen nuevas versiones y te notifica de forma no invasiva en la terminal cuando hay una actualización disponible.


## Desinstalación

Si quieres eliminar Luma de tu sistema, el comando depende de cómo lo instalaste:

**Si fue instalado vía Administrador de Paquetes (.deb, .rpm, PKGBUILD):**
- **Debian/Ubuntu**: `sudo apt remove lumart`
- **Fedora/RHEL**: `sudo dnf remove lumart`
- **Arch Linux**: `sudo pacman -Rns lumart`

**Si fue instalado vía pip:**
```bash
pip uninstall lumart
```

**Si fue instalado manualmente:**
Puedes ejecutar el script de desinstalación provisto:
```bash
chmod +x uninstall.sh
./uninstall.sh
```

## Filosofía

El renderizado de terminal es una forma de compresión visual.

El desafío no es simplemente convertir una imagen en caracteres. El desafío es representar la mayor cantidad de información visual posible utilizando el menor número de celdas de terminal.

Luma, por lo tanto, se enfoca en la **fidelidad perceptual**, utilizando espacios de color matemáticamente precisos (RGB Lineal vs sRGB) y curvas HDR dinámicas, en lugar de simplemente producir arte ASCII reconocible.

## Solución de Problemas

¿Tienes problemas con fuentes, colores o módulos faltantes? Consulta nuestra [Guía de Solución de Problemas](TROUBLESHOOTING.md) para arreglar problemas comunes.

## Hoja de Ruta

* [x] Renderizador inicial de imagen a terminal
* [x] Renderizado Braille
* [x] Renderizado basado en bloques
* [x] Renderizado perceptual mejorado (Motor RGB Lineal)
* [x] Procesamiento de contraste y luminancia (Motor de Color HDR)
* [x] Arquitectura de Motor Dual (Color y Monocromático/Manga nativo C++)
* [x] Mapeo de colores en tiempo real y umbrales
* [x] Dithering ordenado avanzado (matriz de Bayer)
* [ ] Selección automática de glifos
* [ ] Benchmarks de similitud de imagen
* [ ] Optimización de renderizado
* [ ] Renderizado asistido por aprendizaje automático (Machine Learning)
* [ ] Soporte para renderizado de Video y GIF
* [ ] Expansión de sistemas de glifos de terminal

## Contribuir

Luma es un proyecto de código abierto y las contribuciones son bienvenidas.

Si tienes una idea para un algoritmo de renderizado, optimización, sistema de glifos, benchmark, o mejora, siéntete libre de abrir un issue o enviar un pull request. (Consulta [CONTRIBUTING.es.md](CONTRIBUTING.es.md) para más detalles).

## Licencia

Luma es liberado bajo la Licencia Pública General de GNU Affero v3.0 (AGPL-3.0). Consulta el archivo `LICENSE` para más detalles.

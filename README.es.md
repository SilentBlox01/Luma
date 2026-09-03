[English](README.md) | [Español](README.es.md)

# Luma

**Un motor de renderizado de imagen a terminal de alta fidelidad escrito en Python.**

Luma es un motor de renderizado de terminal de código abierto centrado en un único objetivo:

> **Máxima fidelidad visual en el mínimo espacio de terminal.**

A diferencia de los conversores ASCII tradicionales que simplemente mapean el brillo de la imagen a caracteres, Luma explora diferentes sistemas de glifos de terminal, matemáticas de color RGB Lineal y técnicas de renderizado para preservar la mayor cantidad de información visual posible dentro de un número limitado de celdas de terminal.

## Características

* Renderizado de imágenes de alta fidelidad en la terminal
* Renderizado basado en ASCII, Braille y Bloques
* **Renderizado Estilo OS (`--os-style`)**: Caracteres de terminal clásicos (puntos, letras) para logotipos al estilo Neofetch.
* **Intercambio de Color en Tiempo Real (`--swap`)**: Intercambia dinámicamente hasta 5 colores basados en distancia de color Euclidiana en 3D.
* **Motor de Color Épico (Por defecto)**: Promedia colores en el espacio RGB Lineal para evitar resultados opacos, al mismo tiempo que aplica contraste y saturación dinámica (HDR).
* Ancho de salida configurable
* Soporte para terminales Truecolor (ANSI 24-bit)
* Diseñado para tamaños de salida extremadamente pequeños
* Basado en Python y altamente extensible

## Ejemplo

```bash
# Convierte una imagen usando caracteres Braille, colores, y reemplazando el púrpura por el rosa
luma image.png -w 45 --braille -c --swap purple pink
```

## Instalación

Puedes ejecutar Luma directamente desde el código fuente o compilarlo en un paquete nativo de Linux (DEB, RPM, o Arch PKGBUILD).

**Opción 1: Descargar Paquetes Precompilados (Recomendado)**
Puedes descargar los paquetes `.deb` o `.rpm` listos para usar directamente desde la página de [GitHub Releases](https://github.com/SilentBlox01/Luma/releases).

**Opción 2: Ejecutar directamente desde el código fuente**
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
# Asegúrate de tener Pillow instalado
pip install -r requirements.txt
python3 lumart.py --help
```

**Opción 3: Compilar y construir los paquetes nativos tú mismo**
Luma incluye un script de construcción automático para empaquetar la herramienta en un binario independiente utilizando PyInstaller.
```bash
chmod +x build_packages.sh
./build_packages.sh
```
Después de compilar, puedes instalarlo globalmente a través de tu administrador de paquetes:
- **Debian/Ubuntu**: `sudo apt install ./dist/lumart-2.0.0.deb`
- **Fedora/RHEL**: `sudo dnf install ./dist/lumart-2.0.0.rpm`
- **Arch Linux**: `cd dist/arch && makepkg -si`

## Uso

Si instalaste el paquete, puedes ejecutar `lumart` o `luma` desde cualquier lugar. De lo contrario, ejecuta el script de python directamente.

```bash
# Uso básico
python3 lumart.py image.png
```

Especificar el ancho de salida (en caracteres):
```bash
python3 lumart.py image.png -w 30
```

Habilitar renderizado Braille de alta fidelidad con Truecolor:
```bash
python3 lumart.py image.png --braille -c
```

Forzar renderizado de caracteres estilo OS retro (útil para logotipos de SO):
```bash
python3 lumart.py image.png --os-style -c
```

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

## Hoja de Ruta

* [x] Renderizador inicial de imagen a terminal
* [x] Renderizado Braille
* [x] Renderizado basado en bloques
* [x] Renderizado perceptual mejorado (Motor RGB Lineal)
* [x] Procesamiento de contraste y luminancia (Motor Épico)
* [x] Mapeo de colores en tiempo real y umbrales
* [ ] Dithering avanzado
* [ ] Selección automática de glifos
* [ ] Benchmarks de similitud de imagen
* [ ] Optimización de renderizado
* [ ] Renderizado asistido por aprendizaje automático (Machine Learning)
* [ ] Soporte para renderizado de Video y GIF
* [ ] Expansión de sistemas de glifos de terminal

## Contribuir

Luma es un proyecto de código abierto y las contribuciones son bienvenidas.

Si tienes una idea para un algoritmo de renderizado, optimización, sistema de glifos, benchmark, o mejora, siéntete libre de abrir un issue o enviar un pull request. (Consulta `CONTRIBUTING.md` para más detalles).

## Licencia

Luma es liberado bajo la Licencia Pública General de GNU Affero v3.0 (AGPL-3.0). Consulta el archivo `LICENSE` para más detalles.

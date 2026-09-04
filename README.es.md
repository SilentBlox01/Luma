[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

# Luma

**Un motor de renderizado de imagen a terminal de alta fidelidad escrito en Python.**

Luma es un motor de renderizado de terminal de código abierto centrado en un único objetivo:

> **Máxima fidelidad visual en el mínimo espacio de terminal.**

A diferencia de los conversores ASCII tradicionales que simplemente mapean el brillo de la imagen a caracteres, Luma explora diferentes sistemas de glifos de terminal, matemáticas de color RGB Lineal y técnicas de renderizado para preservar la mayor cantidad de información visual posible dentro de un número limitado de celdas de terminal.

## Características

* Renderizado de imágenes de alta fidelidad en la terminal
* Renderizado basado en ASCII, Braille y Bloques
* **Arquitectura de Motor Dual**: Cuenta con un **Motor de Color RGB Lineal** (curvas HDR y promediado de color sub-píxel) y un **Motor Monocromático y Manga** nativo (dithering ordenado Bayer, preservación de trazo y entintado).
* **Selector de Motor (`-E`, `--engine`)**: Alterna dinámicamente entre `color`, `mono`, `bw` y `manga`.
* **Renderizado Estilo OS (`--os-style`)**: Caracteres de terminal clásicos (puntos, letras) para logotipos al estilo Neofetch.
* **Intercambio de Color en Tiempo Real (`--swap`)**: Intercambia dinámicamente hasta 5 colores basados en distancia de color Euclidiana en 3D.
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

Habilitar renderizado Braille de alta fidelidad con Truecolor:
```bash
python3 lumart.py image.png --braille -c
```

Renderizar con el motor Manga Screentone (tramado de semitono y trazo de tinta):
```bash
python3 lumart.py image.png -E manga -w 120
```

Renderizar en monocromático puro sin colores:
```bash
python3 lumart.py image.png -E mono --braille -w 100
```

Forzar renderizado de caracteres estilo OS retro (útil para logotipos de SO):
```bash
python3 lumart.py image.png --os-style -c
```

## Actualizaciones

Para actualizar Luma a la versión más reciente en cualquier momento, simplemente ejecuta:
```bash
luma --update
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

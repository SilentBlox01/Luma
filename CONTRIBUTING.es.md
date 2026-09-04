[English](CONTRIBUTING.md) | [Español](CONTRIBUTING.es.md) | [Português](CONTRIBUTING.pt.md) | [Русский](CONTRIBUTING.ru.md) | [日本語](CONTRIBUTING.ja.md) | [Deutsch](CONTRIBUTING.de.md) | [한국어](CONTRIBUTING.ko.md)

# Contribuir a Luma

¡Gracias por mostrar interés en mejorar Luma! Este proyecto busca empujar los límites gráficos de la terminal, y todas las contribuciones son súper bienvenidas.

## 🐛 Reportar Bugs o Sugerir Ideas

Si encuentras un error o tienes una gran idea (como un nuevo algoritmo de renderizado, patrón de dithering o soporte de animación), abre un **Issue** en GitHub. Por favor incluye:
- El sistema operativo y emulador de terminal que estás utilizando (ej. Fedora con Alacritty, Ubuntu con Kitty, Windows Terminal).
- El comando exacto y los argumentos que causaron el error.
- Si es posible, un ejemplo del arte ASCII generado o la imagen original.

## 🛠️ Contribuir con Código

1. **Haz un Fork del repositorio** en GitHub.
2. **Crea una nueva rama** para tu funcionalidad o corrección (`git checkout -b feature/nueva-magia`).
3. **Escribe y prueba tu código**. La lógica principal del motor vive en `lumart.py`.
4. **Haz commit de tus cambios** con un mensaje claro (`git commit -m 'feat: nuevo algoritmo XYZ'`).
5. **Haz push a la rama** (`git push origin feature/nueva-magia`).
6. **Abre un Pull Request**.

### Estructura del Proyecto
- `lumart.py`: Todo el núcleo del motor: procesamiento perceptivo en Linear RGB, difuminado con Matriz de Bayer, esculpido con Braille/medio-bloques y la CLI con soporte multilingüe.
- `install.sh`: Instalador universal Plug & Play compatible con Fedora, Debian/Ubuntu, Arch Linux, openSUSE y macOS.
- `build_packages.sh`: Script automatizado para compilar binarios autónomos con `PyInstaller` y generar paquetes `.deb`, `.rpm` y `PKGBUILD`.
- `pyproject.toml`: Definición de empaquetado moderno para soportar `pipx install .` y `pip install --user .`.

### Directrices de Código
- **Cero dependencias pesadas**: Mantén Luma ligero y plug-and-play. Depende únicamente de Pillow (`PIL`) y la biblioteca estándar de Python. Evita dependencias masivas como OpenCV o PyTorch.
- **Estética de Terminal**: Cada nuevo modo o mejora debe priorizar la fidelidad visual y el rendimiento en terminales reales.
- **Soporte Multilingüe**: Si añades nuevas opciones de línea de comandos o mensajes al usuario, añade las traducciones a los 7 idiomas en el diccionario `TRANSLATIONS` (`en`, `es`, `pt`, `ru`, `ja`, `de`, `ko`).

¡Diviértete hackeando colores y gráficos en la terminal! 🎨

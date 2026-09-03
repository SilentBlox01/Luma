# Contribuir a Lumart

¡Gracias por mostrar interés en mejorar Lumart! Este proyecto busca empujar los límites gráficos de la terminal, y todas las contribuciones son súper bienvenidas.

## 🐛 Reportar Bugs o Sugerir Ideas
Si encuentras un error o tienes una gran idea (como un nuevo algoritmo de renderizado o soporte de animación), abre un **Issue** en GitHub. Por favor incluye:
- El sistema operativo y emulador de terminal que estás utilizando.
- El comando exacto que causó el error.
- Si es posible, un ejemplo del arte ASCII generado o la imagen original.

## 🛠️ Contribuir con Código

1. **Haz un Fork del repositorio**
2. **Crea una nueva rama** para tu funcionalidad (`git checkout -b feature/nueva-magia`).
3. **Escribe y prueba tu código**. La lógica principal vive en `lumart.py`.
4. **Haz commit de tus cambios** (`git commit -m 'Añadido nuevo algoritmo XYZ'`).
5. **Haz push a la rama** (`git push origin feature/nueva-magia`).
6. **Abre un Pull Request**.

### Estructura del Proyecto
- `lumart.py`: Todo el núcleo matemático, el procesamiento de imágenes, las transformaciones de color (Linear RGB), y el sistema CLI.
- `build_packages.sh`: El script que automatiza la creación del binario autónomo usando `PyInstaller` y el empaquetado para `apt`, `dnf` y `yay`. Si añades dependencias nuevas, asegúrate de que este script las soporte correctamente.

¡Diviértete hackeando colores en la terminal!

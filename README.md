# TablaTraductorOCR
TablaTraductorOCR es una herramienta en Python que automatiza la traducción de tablas en imágenes. Convierte la imagen a escala de grises, extrae cada línea en español con OCR (pytesseract), traduce al inglés usando googletrans y genera un JSON con pares español.

## Instalación rápida

Ejecuta el instalador para configurar las dependencias:

```bash
python instalador.py
```

Esto instalará las bibliotecas indicadas en `requirements.txt`. Luego podrás ejecutar la utilidad así:

```bash
python tabla_traductor.py ruta/a/imagen.png
```

También puedes abrir la interfaz gráfica con:

```bash
python tabla_traductor.py --gui
```

Si al ejecutar el script aparecen errores de importación para `opencv-python`,
`pytesseract` o `googletrans`, asegúrate de haber ejecutado previamente el
instalador. También debes tener **Tesseract OCR** instalado en tu sistema.
En Debian/Ubuntu puedes instalarlo con:

```bash
sudo apt-get install tesseract-ocr
```

"""Herramienta sencilla para extraer texto en español de una imagen,
traducirlo al inglés y guardar el resultado en un JSON.

Uso:
    python tabla_traductor.py ruta/a/imagen.png
"""

import argparse
import json

import cv2
import pytesseract
from googletrans import Translator


def preprocess_image(path: str):
    """Carga una imagen y realiza un preprocesamiento básico para OCR."""
    # 1. Cargar la imagen con OpenCV
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"No se pudo abrir la imagen: {path}")

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Suavizar ligeramente para eliminar ruido
    gray = cv2.medianBlur(gray, 3)
    # Aplicar umbral automático para mejorar contraste
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def extraer_lineas(image) -> list:
    """Ejecuta OCR sobre la imagen y devuelve una lista de líneas."""
    # 2. Ejecutar OCR con pytesseract
    texto = pytesseract.image_to_string(image, lang='spa')
    # Dividir por saltos de línea e ignorar líneas vacías
    return [line.strip() for line in texto.splitlines() if line.strip()]


def traducir_lineas(lineas: list) -> dict:
    """Traduce cada línea de español a inglés y devuelve un diccionario."""
    # 3. Traducir cada línea con googletrans
    traductor = Translator()
    traducciones = {}
    for linea in lineas:
        try:
            # Traducir la línea actual
            traduccion = traductor.translate(linea, src='es', dest='en').text
            traducciones[linea] = traduccion
        except Exception as exc:
            print(f"Advertencia: no se pudo traducir '{linea}': {exc}")
    return traducciones


def guardar_json(diccionario: dict, ruta: str = "translations.json") -> None:
    """Guarda el diccionario de traducciones en un archivo JSON."""
    # 4. Escribir el diccionario en disco
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(diccionario, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Extrae texto español de una imagen, lo traduce al inglés y guarda un JSON."
    )
    parser.add_argument("imagen", help="Ruta a la imagen (PNG/JPEG) con la tabla de texto")
    args = parser.parse_args()

    try:
        preprocesada = preprocess_image(args.imagen)
    except Exception as exc:
        print(f"Error al procesar la imagen: {exc}")
        return

    # Obtener las líneas de texto detectado
    lineas = extraer_lineas(preprocesada)
    if not lineas:
        print("Advertencia: no se encontró texto en la imagen")

    traducciones = traducir_lineas(lineas)
    guardar_json(traducciones)
    print("Traducciones guardadas en translations.json")


if __name__ == "__main__":
    main()

"""Herramienta sencilla para extraer texto en español de una imagen,
traducirlo al inglés y guardar el resultado en un JSON.

Uso en consola:
    python tabla_traductor.py ruta/a/imagen.png
o bien abrir la interfaz gráfica:
    python tabla_traductor.py --gui
"""

import argparse
import json

 Translator

import tkinter as tk
from tkinter import filedialog, messagebox


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


def run_gui() -> None:
    """Abre una interfaz gráfica para seleccionar la imagen y traducirla."""

    root = tk.Tk()
    root.title("Tabla Traductor OCR")
    root.geometry("400x200")

    path_var = tk.StringVar()

    def select_image() -> None:
        path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg"),
                ("Todos los archivos", "*.*"),
            ],
        )
        if path:
            path_var.set(path)

    def process_image() -> None:
        ruta = path_var.get()
        if not ruta:
            messagebox.showwarning(
                "Imagen no seleccionada", "Elige una imagen primero")
            return
        try:
            preproc = preprocess_image(ruta)
            lineas = extraer_lineas(preproc)
            if not lineas:
                messagebox.showwarning(
                    "Sin texto", "No se encontró texto en la imagen")
            traducciones = traducir_lineas(lineas)
            guardar_json(traducciones)
            messagebox.showinfo(
                "Finalizado", "Traducciones guardadas en translations.json")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    tk.Button(root, text="Seleccionar imagen", command=select_image).pack(pady=10)
    tk.Label(root, textvariable=path_var, wraplength=380).pack(pady=5)
    tk.Button(root, text="Traducir y guardar", command=process_image).pack(pady=20)

    root.mainloop()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Extrae texto español de una imagen, lo traduce al inglés y guarda un JSON."
        )
    )
    parser.add_argument(
        "imagen",
        nargs="?",
        help="Ruta a la imagen (PNG/JPEG) con la tabla de texto",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Mostrar interfaz gráfica para seleccionar la imagen",
    )
    args = parser.parse_args()

    if args.gui:
        run_gui()
        return

    if not args.imagen:
        parser.error("debes especificar la ruta de la imagen o usar --gui")

    try:
        preprocesada = preprocess_image(args.imagen)
    except Exception as exc:
        print(f"Error al procesar la imagen: {exc}")
        return

    lineas = extraer_lineas(preprocesada)
    if not lineas:
        print("Advertencia: no se encontró texto en la imagen")

    traducciones = traducir_lineas(lineas)
    guardar_json(traducciones)
    print("Traducciones guardadas en translations.json")


if __name__ == "__main__":
    main()

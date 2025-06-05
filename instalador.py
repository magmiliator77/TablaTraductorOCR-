import os
import subprocess
import sys


def main():
    """Instala las dependencias listadas en requirements.txt."""
    req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if not os.path.exists(req_file):
        print(f"No se encontró {req_file}")
        sys.exit(1)

    print("Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
    except subprocess.CalledProcessError as exc:
        print(f"Error al instalar dependencias: {exc}")
        sys.exit(exc.returncode)

    print("Dependencias instaladas. Ahora puedes ejecutar:")
    print("    python tabla_traductor.py ruta/a/imagen.png")


if __name__ == "__main__":
    main()

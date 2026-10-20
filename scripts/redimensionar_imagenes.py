
from pathlib import Path
from PIL import Image, ImageOps
import pandas as pd

# ==========================================
# 1. CONFIGURACIÓN
# ==========================================

BASE = Path(__file__).resolve().parent.parent

CARPETA_ORIGEN = BASE / "datos"
CARPETA_DESTINO = BASE / "datos_procesados"

CARPETAS = [
    "Training-All_Photos_updated",
    "Test_All_Photos"
]

MAX_RESOLUCION = 1024

EXTENSIONES = {".jpg", ".jpeg", ".png", ".webp"}

# ==========================================
# 2. REDIMENSIONAR UNA IMAGEN
# ==========================================

def redimensionar_imagen(origen, destino):

    with Image.open(origen) as imagen:

        # Respetar orientación original de la foto
        imagen = ImageOps.exif_transpose(imagen)

        ancho_original, alto_original = imagen.size

        # Mantener proporciones y evitar ampliar imágenes
        imagen.thumbnail(
            (MAX_RESOLUCION, MAX_RESOLUCION),
            Image.Resampling.LANCZOS
        )

        ancho_nuevo, alto_nuevo = imagen.size

        # Crear carpeta de destino
        destino.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # Guardar imagen redimensionada
        if destino.suffix.lower() in [".jpg", ".jpeg"]:
            imagen = imagen.convert("RGB")
            imagen.save(destino, quality=95)
        else:
            imagen.save(destino)

        return {
            "archivo": str(origen.relative_to(CARPETA_ORIGEN)),
            "ancho_original": ancho_original,
            "alto_original": alto_original,
            "ancho_nuevo": ancho_nuevo,
            "alto_nuevo": alto_nuevo,
            "escala_x": ancho_nuevo / ancho_original,
            "escala_y": alto_nuevo / alto_original
        }


# ==========================================
# 3. PROCESAR DATASET
# ==========================================

def procesar_dataset():

    registros = []
    errores = []

    for carpeta in CARPETAS:

        origen = CARPETA_ORIGEN / carpeta
        destino = CARPETA_DESTINO / carpeta

        if not origen.exists():
            print(f"No se encontró: {origen}")
            continue

        imagenes = sorted(
            archivo
            for archivo in origen.rglob("*")
            if archivo.is_file()
            and archivo.suffix.lower() in EXTENSIONES
        )

        print(f"\nCarpeta: {carpeta}")
        print(f"Imágenes encontradas: {len(imagenes)}")

        for i, archivo in enumerate(imagenes, start=1):

            ruta_relativa = archivo.relative_to(origen)
            salida = destino / ruta_relativa

            try:
                info = redimensionar_imagen(
                    archivo,
                    salida
                )

                registros.append(info)

            except Exception as error:
                errores.append({
                    "archivo": str(archivo),
                    "error": str(error)
                })

            if i % 50 == 0 or i == len(imagenes):
                print(
                    f"Procesadas: {i}/{len(imagenes)}"
                )

    # ======================================
    # 4. GUARDAR RESULTADOS
    # ======================================

    CARPETA_DESTINO.mkdir(
        parents=True,
        exist_ok=True
    )

    reporte = pd.DataFrame(registros)

    reporte.to_csv(
        CARPETA_DESTINO / "reporte_redimensionamiento.csv",
        index=False
    )

    if errores:
        pd.DataFrame(errores).to_csv(
            CARPETA_DESTINO / "errores.csv",
            index=False
        )

    print("\nPROCESAMIENTO FINALIZADO")
    print("Imágenes procesadas:", len(registros))
    print("Errores:", len(errores))
    print("Destino:", CARPETA_DESTINO)


if __name__ == "__main__":
    procesar_dataset()
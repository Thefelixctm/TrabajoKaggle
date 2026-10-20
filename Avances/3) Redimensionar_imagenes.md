### Redimensionamiento de imágenes del dataset

Se desarrolló e implementó un script en Python utilizando la biblioteca Pillow para reducir la resolución de las fotografías del conjunto de datos, estableciendo un máximo de 1024 píxeles en su dimensión mayor y conservando la relación de aspecto original.

Se procesaron exitosamente **162 imágenes, correspondientes a 127 fotografías de entrenamiento y 35 de prueba**, sin registrar errores durante la ejecución.

La validación del archivo `reporte_redimensionamiento.csv` permitió comprobar que todas las imágenes cumplen con el límite de resolución establecido, mantienen sus proporciones originales dentro de las diferencias de redondeo y no presentan ampliaciones innecesarias. Asimismo, no se identificaron registros incompletos ni rutas duplicadas.

Las imágenes procesadas fueron almacenadas en una carpeta independiente, preservando los archivos originales. Este procedimiento permite disponer de un conjunto de fotografías de menor resolución para las posteriores etapas de procesamiento y entrenamiento de modelos de visión por computadora.
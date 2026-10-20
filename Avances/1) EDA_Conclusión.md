### Análisis exploratorio de las distribuciones granulométricas

Se realizó un análisis exploratorio de las 24 muestras de suelo disponibles en el conjunto de entrenamiento de la competición *Predicting Soil Grain Size Distributions from Images*. Cada muestra contiene once porcentajes acumulados correspondientes a diámetros granulométricos entre 0,002 y 200 mm.

Inicialmente, se verificó la integridad de los datos, sin identificar valores faltantes ni registros duplicados. Asimismo, el análisis de las fracciones por intervalo confirmó la coherencia de las distribuciones granulométricas, cuyos porcentajes suman el 100 % para cada muestra.

Los resultados evidenciaron una alta heterogeneidad entre las distribuciones granulométricas. Las mayores desviaciones estándar se observaron en los diámetros intermedios, especialmente en 0,63 mm, donde se registró una desviación de 38,18 puntos porcentuales. Esto demuestra que las muestras presentan diferencias considerables en sus proporciones de partículas finas y gruesas.

Por otra parte, el análisis de las fracciones de masa permitió identificar que los intervalos de 0,02–0,063 mm, 0,063–0,2 mm, 2–6,3 mm y 6,3–20 mm presentan las mayores proporciones medias de material. El análisis de correlaciones también evidenció relaciones positivas entre los porcentajes acumulados de diámetros cercanos, comportamiento consistente con la naturaleza acumulativa de las variables.

En conclusión, el análisis exploratorio demuestra que el conjunto de datos presenta una diversidad granulométrica considerable, pese a su reducido número de muestras. Esta característica supone un desafío para el entrenamiento de modelos de visión por computadora, particularmente por el riesgo de sobreajuste y la necesidad de generalizar a suelos no observados. Por ello, será fundamental utilizar técnicas de validación cruzada y evaluar cuidadosamente el comportamiento predictivo de los modelos propuestos.
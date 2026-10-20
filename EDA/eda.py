
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. CONFIGURACIÓN
# ==========================================

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "datos" / "Training_labels_updated.csv"
OUTPUT = Path(__file__).resolve().parent / "graficos"
OUTPUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA)

columnas = [
    "0.002", "0.0063", "0.02", "0.063",
    "0.2", "0.63", "2", "6.3",
    "20", "63", "200"
]

diametros = np.array([float(c) for c in columnas])
valores = df[columnas].to_numpy(dtype=float)

# ==========================================
# 2. INSPECCIÓN GENERAL
# ==========================================

print("\n===== INFORMACIÓN GENERAL =====")
print("Dimensiones:", df.shape)
print("Muestras únicas:", df["sample_id"].nunique())
print("\nTipos de datos:")
print(df.dtypes)
print("\nPrimeras cinco muestras:")
print(df.head())

# ==========================================
# 3. CALIDAD DE LOS DATOS
# ==========================================

print("\n===== CALIDAD DE DATOS =====")
print("\nValores faltantes:")
print(df.isnull().sum())

print("\nFilas duplicadas:", df.duplicated().sum())
print("IDs duplicados:", df["sample_id"].duplicated().sum())

rango = np.isfinite(valores).all(axis=1) & (
    (valores >= 0) & (valores <= 100)
).all(axis=1)

monotonia = (np.diff(valores, axis=1) >= -1e-8).all(axis=1)
final_100 = np.isclose(valores[:, -1], 100)

validas = rango & monotonia & final_100

print("\nCurvas válidas:", validas.sum(), "/", len(df))
print("Curvas inválidas:")
print(df.loc[~validas, "sample_id"].tolist())

# ==========================================
# 4. ESTADÍSTICAS DESCRIPTIVAS
# ==========================================

print("\n===== ESTADÍSTICAS =====")

estadisticas = df[columnas].describe().T
print(estadisticas.round(2))

estadisticas.to_csv(
    OUTPUT / "estadisticas_granulometricas.csv"
)

# ==========================================
# 5. CURVAS GRANULOMÉTRICAS
# ==========================================

plt.figure(figsize=(11, 6))

for _, fila in df.iterrows():
    plt.semilogx(
        diametros,
        fila[columnas].to_numpy(dtype=float),
        alpha=0.55,
        linewidth=1.4
    )

plt.xlabel("Diámetro de partícula (mm)")
plt.ylabel("Porcentaje acumulado (%)")
plt.title("Curvas granulométricas de las 24 muestras")
plt.ylim(0, 105)
plt.grid(True, alpha=0.3, which="both")
plt.tight_layout()

plt.savefig(OUTPUT / "01_curvas_granulometricas.png", dpi=300)
plt.show()

# ==========================================
# 6. CURVA MEDIA Y MEDIANA
# ==========================================

media = np.mean(valores, axis=0)
mediana = np.median(valores, axis=0)
p25 = np.percentile(valores, 25, axis=0)
p75 = np.percentile(valores, 75, axis=0)

plt.figure(figsize=(11, 6))

plt.semilogx(diametros, media, marker="o", label="Media")
plt.semilogx(diametros, mediana, marker="s", label="Mediana")
plt.fill_between(
    diametros, p25, p75,
    alpha=0.2, label="Percentiles 25–75"
)

plt.xlabel("Diámetro (mm)")
plt.ylabel("Porcentaje acumulado (%)")
plt.title("Distribución granulométrica representativa")
plt.ylim(0, 105)
plt.grid(True, alpha=0.3, which="both")
plt.legend()
plt.tight_layout()

plt.savefig(OUTPUT / "02_media_mediana.png", dpi=300)
plt.show()

# ==========================================
# 7. DISPERSIÓN POR DIÁMETRO
# ==========================================

plt.figure(figsize=(12, 6))

plt.boxplot(
    [df[c].values for c in columnas],
    tick_labels=columnas,
    showfliers=True
)

plt.xlabel("Diámetro (mm)")
plt.ylabel("Porcentaje acumulado (%)")
plt.title("Variabilidad granulométrica por diámetro")
plt.xticks(rotation=45)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(OUTPUT / "03_boxplot.png", dpi=300)
plt.show()

# ==========================================
# 8. PROPORCIONES POR INTERVALO
# ==========================================

# Primera fracción: material <= 0.002 mm.
# Las siguientes son diferencias entre acumulados.
fracciones = np.diff(
    valores,
    axis=1,
    prepend=np.zeros((len(df), 1))
)

fracciones_df = pd.DataFrame(
    fracciones,
    columns=columnas,
    index=df["sample_id"]
)

print("\n===== FRACCIONES POR INTERVALO =====")
print(fracciones_df.describe().round(2))

fracciones_df.to_csv(OUTPUT / "fracciones_intervalos.csv")

promedio_fracciones = fracciones_df.mean()

plt.figure(figsize=(12, 6))
plt.bar(columnas, promedio_fracciones)

plt.xlabel("Límite superior del intervalo (mm)")
plt.ylabel("Fracción media de masa (%)")
plt.title("Proporción media de masa por intervalo")
plt.xticks(rotation=45)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(OUTPUT / "04_fracciones.png", dpi=300)
plt.show()

# ==========================================
# 9. CORRELACIONES
# ==========================================

# La última columna es constante (100 %),
# por lo que no tiene correlación de Pearson.
corr = df[columnas[:-1]].corr()

fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(corr, vmin=-1, vmax=1, cmap="coolwarm")

ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns, rotation=45)
ax.set_yticklabels(corr.columns)

fig.colorbar(im, ax=ax, label="Correlación de Pearson")
ax.set_title("Correlación entre porcentajes acumulados")
plt.tight_layout()

plt.savefig(OUTPUT / "05_correlaciones.png", dpi=300)
plt.show()

print("\nEDA FINALIZADO")
print("Gráficos guardados en:", OUTPUT)
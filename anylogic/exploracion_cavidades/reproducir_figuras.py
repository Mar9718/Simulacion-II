"""Reproduce las figuras y tablas del avance a partir de los CSV incluidos.

Ejecución: python reproducir_figuras.py
Se verifican los conteos registrados; no se recalculan encuentros geométricos.
Las medias de errores se limitan a estimaciones finitas e indican su denominador.
"""
from pathlib import Path
from collections import Counter, defaultdict
import csv
import math
import statistics

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.ticker import PercentFormatter, NullFormatter

BASE = Path(__file__).resolve().parent
DATA = BASE / "datos"
FIGURES = BASE / "figuras"
TABLES = BASE / "tablas"
REGIMES = ("interior_1000", "entrada_5000")
SPLITS = ("25/75", "50/50")
CAVITIES = ("pequena", "grande")
LABELS = {"interior_1000": "Inicio interior · D = 1000 mm",
          "entrada_5000": "Inicio en entrada · D = 5000 mm"}
SHORT = {"interior_1000": "Interior · 1000 mm", "entrada_5000": "Entrada · 5000 mm"}
CAVITY_LABELS = {"pequena": "Pequeña", "grande": "Grande"}
BLUE, ORANGE, GREEN, GRAY = "#2367A6", "#D2782D", "#28845A", "#ADB8C8"
STYLE = {"font.family": "DejaVu Sans", "font.size": 11,
         "axes.titlesize": 12, "axes.labelsize": 11,
         "axes.spines.top": False, "axes.spines.right": False,
         "axes.titleweight": "bold", "figure.facecolor": "white",
         "axes.facecolor": "white", "savefig.facecolor": "white",
         "svg.fonttype": "none", "axes.unicode_minus": True}


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(name, rows):
    if not rows:
        raise ValueError(f"Tabla vacía: {name}")
    with (TABLES / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def close(a, b):
    return math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-7)


def cavity_key(row):
    return row["reparto"], int(row["par"]), row["cavidad"]


def estimate(row):
    return float(row["A_estimada_mm2"]) if row["A_estimada_mm2"] else None


def validate_and_derive():
    studies, classification_rows, finite_rows, error_summaries = {}, [], [], []
    for regime in REGIMES:
        folder = DATA / regime
        cavities, pairs = read_csv(folder / "cavidades.csv"), read_csv(folder / "pares.csv")
        summaries, seeds = read_csv(folder / "resumen_repartos.csv"), read_csv(folder / "semillas.csv")
        require(len(cavities) == 20 and len(pairs) == 10, f"Tamaño inesperado: {regime}")
        lookup = {cavity_key(row): row for row in cavities}
        require(len(lookup) == len(cavities), f"Cavidades duplicadas: {regime}")
        seed_lookup = {(r["reparto"], int(r["par"]), r["cavidad"], int(r["visita"])): r["semilla"] for r in seeds}
        require(len(seed_lookup) == 40, f"Flujos incompletos o repetidos: {regime}")
        for row in cavities:
            require(row["estado"] == "completada", f"Ejecución incompleta: {regime}/{cavity_key(row)}")
            n, area = int(row["N_encuentros"]), float(row["area_real_mm2"])
            expected_area = 875 if row["cavidad"] == "pequena" else 1750
            require(n >= 0 and close(area, expected_area), "Conteo o área conocidos inválidos")
            require(close(float(row["ancho_mm"]) * float(row["alto_mm"]), area), "Dimensiones y área no coinciden")
            target = 1000 if regime == "interior_1000" else 5000
            require(close(float(row["L_real_mm"]) + float(row["S_real_mm"]), target), "Distancia total distinta del régimen")
            for visit in (1, 2):
                require(seed_lookup[cavity_key(row) + (visit,)] == row[f"semilla_v{visit}"], "Semilla y cavidad no coinciden")
            if n == 0:
                require(estimate(row) is None and row["estado_estimacion"] == "sin_estimacion_finita_N0", "N=0 requiere estimación ausente")
            else:
                calculated = 2 * float(row["L_real_mm"]) * float(row["S_real_mm"]) / (math.pi * n)
                require(estimate(row) is not None and close(calculated, estimate(row)), "Estimador y CSV no coinciden")
                error = calculated - area
                require(close(error, row["error_mm2"]) and close(error / area, row["error_relativo"]), "Errores y CSV no coinciden")
                finite_rows.append({"regimen": regime, "reparto": row["reparto"], "par": int(row["par"]),
                    "cavidad": row["cavidad"], "N_encuentros": n, "area_real_mm2": area,
                    "A_estimada_mm2": calculated, "error_mm2": error,
                    "error_relativo": error / area, "error_absoluto_relativo": abs(error / area)})
        for split in SPLITS:
            complete = [r for r in pairs if r["reparto"] == split and r["estado"] == "completo"]
            require(len(complete) == 5, f"R debe ser 5: {regime}/{split}")
            classes = Counter()
            for pair in complete:
                small, large = [lookup[(split, int(pair["par"]), c)] for c in CAVITIES]
                ns, nl = int(small["N_encuentros"]), int(large["N_encuentros"])
                require(ns == int(pair["N_pequena"]) and nl == int(pair["N_grande"]), "Conteos entre archivos no coinciden")
                category = "acierto" if ns > nl else "inversion" if ns < nl else "empate"
                require(pair["clasificacion"] == category, "Clasificación incompatible con N")
                classes[category] += 1
            native = next(r for r in summaries if r["reparto"] == split)
            derived = {"regimen": regime, "reparto": split, "pares_completos": len(complete),
                       "aciertos": classes["acierto"], "inversiones": classes["inversion"], "empates": classes["empate"]}
            require(int(native["pares_completos"]) == len(complete), "Denominador no coincide")
            for category in ("aciertos", "inversiones", "empates"):
                require(int(native[category]) == derived[category], "Resumen nativo no coincide con los pares")
                derived[f"proporcion_{category}"] = derived[category] / len(complete)
                require(close(native[f"proporcion_{category}"], derived[f"proporcion_{category}"]), "Proporción nativa incompatible")
            classification_rows.append(derived)
            for cavity in CAVITIES:
                group = [r for r in cavities if r["reparto"] == split and r["cavidad"] == cavity]
                finite = [r for r in finite_rows if r["regimen"] == regime and r["reparto"] == split and r["cavidad"] == cavity]
                zeros = sum(int(r["N_encuentros"]) == 0 for r in group)
                require(int(native[f"N0_{cavity}"]) == zeros and int(native[f"estimaciones_finitas_{cavity}"]) == len(finite), "Denominadores de estimaciones incompatibles")
                errors = [r["error_absoluto_relativo"] for r in finite]
                error_summaries.append({"regimen": regime, "reparto": split, "cavidad": cavity,
                    "ejecuciones_completas": len(group), "estimaciones_finitas": len(finite), "N0_sin_estimacion_finita": zeros,
                    "denominador_estadisticas": len(finite),
                    "media_error_absoluto_relativo_solo_finitas": statistics.mean(errors) if errors else "",
                    "mediana_error_absoluto_relativo_solo_finitas": statistics.median(errors) if errors else ""})
        studies[regime] = {"cavities": cavities, "lookup": lookup}
    comparisons = []
    for key, initial in studies["interior_1000"]["lookup"].items():
        later = studies["entrada_5000"]["lookup"][key]
        require(all(initial[f"semilla_v{v}"] == later[f"semilla_v{v}"] for v in (1, 2)), "Identificadores emparejados con semillas diferentes")
        if estimate(initial) is None or estimate(later) is None:
            continue
        area = float(initial["area_real_mm2"])
        first, second = abs(estimate(initial) / area - 1), abs(estimate(later) / area - 1)
        change = second - first
        comparisons.append({"reparto": key[0], "par": key[1], "cavidad": key[2],
            "error_absoluto_relativo_interior_1000": first,
            "error_absoluto_relativo_entrada_5000": second,
            "diferencia_entrada_menos_interior": change,
            "cambio": "disminuye" if change < -1e-12 else "aumenta" if change > 1e-12 else "igual"})
    counts = Counter(r["cambio"] for r in comparisons)
    write_csv("resumen_clasificacion.csv", classification_rows)
    write_csv("errores_finitos.csv", finite_rows)
    write_csv("resumen_errores_finitos.csv", error_summaries)
    write_csv("comparacion_emparejada_regimenes.csv", comparisons)
    write_csv("resumen_comparacion_emparejada.csv", [{"casos_posibles": 20, "finitos_en_ambos_regimenes": len(comparisons),
        "excluidos_por_estimacion_no_finita": 20 - len(comparisons), "error_disminuye": counts["disminuye"],
        "error_aumenta": counts["aumenta"], "error_igual": counts["igual"],
        "alcance": "comparacion_descriptiva_cambian_distancia_y_arranque"}])
    return studies, classification_rows


def save(fig, stem):
    for suffix in ("png", "svg"):
        fig.savefig(FIGURES / f"{stem}.{suffix}", dpi=180, bbox_inches="tight")
    plt.close(fig)


def classification_figure(rows):
    fig, ax = plt.subplots(figsize=(11, 6.5))
    bottom = [0.0] * len(rows)
    for key, label, color in (("aciertos", "Aciertos", BLUE), ("inversiones", "Inversiones", ORANGE), ("empates", "Empates", GRAY)):
        heights = [100 * r[key] / r["pares_completos"] for r in rows]
        ax.bar(range(len(rows)), heights, bottom=bottom, color=color, label=label, width=.64, edgecolor="white")
        for i, (row, height) in enumerate(zip(rows, heights)):
            if height:
                ax.text(i, bottom[i] + height / 2, f"{row[key]}/{row['pares_completos']}\n{height:.0f}%", ha="center", va="center", color="white" if key != "empates" else "#243244", fontweight="bold")
            bottom[i] += height
    ax.set_xticks(range(len(rows)), [f"{SHORT[r['regimen']]}\nReparto {r['reparto']} · R = {r['pares_completos']}" for r in rows])
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(PercentFormatter(100))
    ax.set_ylabel("Proporción de todos los pares completos")
    ax.set_title("Clasificación por conteos de encuentros", pad=32, fontsize=16)
    ax.legend(loc="lower center", bbox_to_anchor=(.5, 1.005), ncol=3, frameon=False)
    ax.grid(axis="y", alpha=.17)
    ax.set_axisbelow(True)
    fig.subplots_adjust(bottom=.20, top=.83)
    fig.text(.5, .025, "Se conservan los pares con N = 0. Cada barra usa cinco pares completos; los regímenes difieren en distancia y arranque.", ha="center", fontsize=10, color="#435267")
    save(fig, "01_clasificacion_pares")


def estimates_figure(studies):
    finite = [estimate(r) for s in studies.values() for r in s["cavities"] if estimate(r) is not None]
    limits = (min(min(finite), 875) / 1.7, max(max(finite), 1750) * 1.9)
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharey=True)
    for row_index, regime in enumerate(REGIMES):
        for col_index, split in enumerate(SPLITS):
            ax = axes[row_index, col_index]
            ticks = []
            for x, cavity in enumerate(CAVITIES):
                group = sorted((r for r in studies[regime]["cavities"] if r["reparto"] == split and r["cavidad"] == cavity), key=lambda r: int(r["par"]))
                color, marker, area = (BLUE, "o", 875) if cavity == "pequena" else (ORANGE, "s", 1750)
                ax.axhline(area, color=color, linestyle="--", linewidth=1.1, alpha=.85)
                finite_count = 0
                for r in group:
                    value = estimate(r)
                    if value is None:
                        continue
                    finite_count += 1
                    jitter = (int(r["par"]) - 3) * .10
                    ax.scatter(x + jitter, value, color=color, marker=marker, s=47, edgecolor="white", linewidth=.5, zorder=3)
                    ax.annotate(f"p{r['par']}", (x + jitter, value), xytext=(5, 3), textcoords="offset points", fontsize=8, color=color)
                ticks.append(f"{CAVITY_LABELS[cavity]}\nFinitas: {finite_count}/5 · N = 0: {5-finite_count}")
            ax.set_yscale("log")
            ax.set_ylim(limits)
            ax.set_xlim(-.45, 1.5)
            ax.set_xticks([0, 1], ticks)
            ax.set_title(f"{LABELS[regime]}\nReparto {split}", pad=12)
            ax.grid(axis="y", which="major", alpha=.2)
            ax.yaxis.set_minor_formatter(NullFormatter())
            if col_index == 0:
                ax.set_ylabel("Área estimada finita (mm²; escala logarítmica)")
    handles = [Line2D([0], [0], color=BLUE, ls="--", label="Área pequeña: 875 mm²"),
               Line2D([0], [0], color=ORANGE, ls="--", label="Área grande: 1750 mm²")]
    fig.suptitle("Estimaciones individuales y áreas conocidas", y=.98, fontsize=17)
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(.5, .945), ncol=2, frameon=False)
    fig.subplots_adjust(top=.85, bottom=.13, hspace=.62, wspace=.16)
    fig.text(.5, .035, "Escala vertical común. p identifica el par. N = 0 implica ausencia de estimación finita; no se representa como área cero.", ha="center", fontsize=10, color="#435267")
    save(fig, "02_estimaciones_individuales")


def trajectories_figure(studies):
    trajectories = read_csv(DATA / "trayectorias_referencia.csv")
    grouped = defaultdict(list)
    for r in trajectories:
        require(int(r["par"]) == 1, "Las trayectorias de referencia deben pertenecer al par 1")
        grouped[(r["reparto"], r["cavidad"], int(r["visita"]))].append(r)
    require(len(grouped) == 8, "Se requieren ocho visitas de referencia")
    max_width = max(float(r["ancho_mm"]) for r in studies["entrada_5000"]["cavities"])
    max_height = max(float(r["alto_mm"]) for r in studies["entrada_5000"]["cavities"])
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 12.5), sharex=True, sharey=True)
    for row_index, split in enumerate(SPLITS):
        for col_index, cavity in enumerate(CAVITIES):
            ax = axes[row_index, col_index]
            data = studies["entrada_5000"]["lookup"][(split, 1, cavity)]
            width, height = float(data["ancho_mm"]), float(data["alto_mm"])
            ax.add_patch(Rectangle((0, 0), width, height, fill=False, edgecolor="#48586A", linewidth=1.2, zorder=4))
            for visit, color in ((1, BLUE), (2, ORANGE)):
                points = sorted(grouped[(split, cavity, visit)], key=lambda r: int(r["indice_punto"]))
                require(len({int(r["indice_punto"]) for r in points}) == len(points), "Índice de trayectoria repetido")
                x, y = [float(r["x_mm"]) for r in points], [float(r["y_mm"]) for r in points]
                require(all(-1e-8 <= a <= width + 1e-8 and -1e-8 <= b <= height + 1e-8 for a, b in zip(x, y)), "Trayectoria fuera de cavidad")
                require(close(sum(float(r["tramo_mm"]) for r in points), data["L_real_mm" if visit == 1 else "S_real_mm"]), "Distancia de referencia incompatible")
                ax.plot(x, y, color=color, linewidth=.48, alpha=.65)
                ax.plot(x[0], y[0], marker="o", color=color, markeredgecolor="white", markersize=5, zorder=6)
            entry_width = 1 if cavity == "pequena" else math.sqrt(2)
            ax.plot([(width-entry_width)/2, (width+entry_width)/2], [height, height], color=GREEN, linewidth=5, solid_capstyle="butt", zorder=7)
            ax.set_xlim(-1, max_width + 1)
            ax.set_ylim(max_height + 2, -1)
            ax.set_aspect("equal", adjustable="box")
            ax.set_xlabel("X (mm)")
            ax.set_ylabel("Y (mm)")
            ax.set_title(f"Reparto {split} · {CAVITY_LABELS[cavity].lower()}\nN = {data['N_encuentros']} · Área estimada = {estimate(data):.0f} mm²", pad=10)
            ax.grid(alpha=.12)
    handles = [Line2D([0], [0], color=BLUE, label="Visita 1"), Line2D([0], [0], color=ORANGE, label="Visita 2"),
               Line2D([0], [0], color=GREEN, linewidth=5, label="Entrada: 1 mm / √2 mm")]
    fig.suptitle("Recorridos registrados · D = 5000 mm · primer par", y=.98, fontsize=16)
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(.5, .945), ncol=3, frameon=False)
    fig.subplots_adjust(top=.87, bottom=.10, hspace=.28, wspace=.28)
    fig.text(.5, .025, "La escala física es común a los cuatro paneles. Se conserva la coordenada de la plataforma: Y crece hacia abajo.\nSe muestran todas las posiciones exportadas del par 1; la selección es la misma para ambos repartos.", ha="center", fontsize=10, color="#435267", linespacing=1.6)
    save(fig, "03_recorridos_referencia")


def cumulative_figure():
    rows = sorted(read_csv(DATA / "actualizacion_interactiva.csv"), key=lambda r: int(r["revision"]))
    require([int(r["pares_completos"]) for r in rows] == [5, 6, 7], "La actualización debe conservar los cortes R=5,6,7")
    for r in rows:
        require(r["reparto"] == "25/75", "La secuencia corresponde al reparto 25/75")
        require(sum(int(r[k]) for k in ("aciertos", "inversiones", "empates")) == int(r["pares_completos"]), "Clasificaciones acumuladas incompatibles")
        require(close(r["proporcion_aciertos"], int(r["aciertos"]) / int(r["pares_completos"])), "Proporción acumulada incompatible")
    x = [int(r["pares_completos"]) for r in rows]
    y = [100 * float(r["proporcion_aciertos"]) for r in rows]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, color=BLUE, linewidth=2, marker="o", markersize=9)
    for a, b, r in zip(x, y, rows):
        ax.annotate(f"{b:.1f}%", (a, b), xytext=(0, 13), textcoords="offset points", ha="center", color=BLUE, fontweight="bold", fontsize=13)
        ax.annotate(f"Aciertos: {r['aciertos']}\nInversiones: {r['inversiones']}\nEmpates: {r['empates']}", (a, b), xytext=(0, -23), textcoords="offset points", ha="center", va="top", fontsize=10, color="#34465D")
    ax.set_ylim(0, 100)
    ax.set_xlim(4.6, 7.4)
    ax.set_xticks(x, [f"R = {a}\nCorte {r['revision']}" for a, r in zip(x, rows)])
    ax.yaxis.set_major_formatter(PercentFormatter(100))
    ax.set_xlabel("Pares completos acumulados", labelpad=10)
    ax.set_ylabel("Aciertos / todos los pares completos")
    ax.set_title("Actualización del contador · reparto 25/75", fontsize=16, pad=20)
    ax.grid(axis="y", alpha=.2)
    fig.subplots_adjust(bottom=.23, top=.85)
    fig.text(.5, .035, "Serie acumulada: cada corte conserva los pares anteriores. Los tres puntos no son muestras independientes.\nInicio desde entrada · D = 5000 mm por cavidad.", ha="center", fontsize=10, color="#435267", linespacing=1.6)
    save(fig, "04_actualizacion_acumulada")


def main():
    FIGURES.mkdir(exist_ok=True)
    TABLES.mkdir(exist_ok=True)
    with plt.rc_context(STYLE):
        studies, rows = validate_and_derive()
        classification_figure(rows)
        estimates_figure(studies)
        trajectories_figure(studies)
        cumulative_figure()
    print("Verificados los CSV: 20 pares completos, 40 ejecuciones de cavidad y tres cortes acumulados.")
    print("Exportadas cuatro figuras PNG/SVG y cinco tablas derivadas en figuras/ y tablas/.")


if __name__ == "__main__":
    main()

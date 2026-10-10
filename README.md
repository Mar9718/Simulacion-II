# Simulación II

En este repositorio reúno mis cuadernos y ejercicios de Simulación II. Explico los procedimientos paso a paso e incluyo el código, las gráficas y los resultados de cada trabajo.

## Cuadernos disponibles

### Metropolis-Hastings en dos dimensiones

En este cuaderno genero una cadena de puntos con dos coordenadas, explico la regla de aceptación y represento la muestra con una nube de puntos y dos histogramas marginales.

- [Ver el notebook en GitHub](notebooks/M-H_tutorial_histogramas.ipynb).
- [Abrir el notebook en Google Colab](https://colab.research.google.com/github/Mar9718/Simulacion-II/blob/main/notebooks/M-H_tutorial_histogramas.ipynb).

Uso **10 000 estados**, el punto inicial **(0, 0)** y la **semilla 42**. Conservo los estados repetidos cuando rechazo una propuesta, porque también forman parte de la cadena.

### Caminata aleatoria sobre un grafo

En este cuaderno simulo una caminata entre cadenas de ceros y unos que no tienen dos unos consecutivos. Estimo el número medio de unos y comparo el resultado con la esperanza teórica. También represento la media acumulada y comparo la distribución simulada con la teórica mediante gráficas de barras.

- [Ver el notebook en GitHub](notebooks/Caminata_sobre_el_grafo_tutorial.ipynb).
- [Abrir el notebook en Google Colab](https://colab.research.google.com/github/Mar9718/Simulacion-II/blob/main/notebooks/Caminata_sobre_el_grafo_tutorial.ipynb).

Uso cadenas de **100 posiciones**, descarto **20 000 pasos iniciales** y guardo **100 000 observaciones**, con la **semilla 42**. Conservo los estados repetidos por rechazo y explico el conteo combinatorio que uso para obtener los valores teóricos.

## Ejecución

Trabajo con **Python y NumPy**. Para las gráficas de Metropolis-Hastings uso **Pillow**; en la caminata sobre el grafo uso **Matplotlib** y calculo las combinaciones con **SciPy**.

Para ejecutar cada cuaderno, lo abro mediante su enlace de **Google Colab** y ejecuto las celdas de arriba hacia abajo. Las gráficas y los resultados están integrados en los notebooks.

## Alcance de los resultados

Las gráficas y los conteos describen las simulaciones obtenidas. La tasa de aceptación, el descarte de pasos iniciales y la apariencia de las gráficas, por sí solos, no demuestran convergencia ni independencia entre los estados.

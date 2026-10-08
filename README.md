# Simulación II

En este repositorio reúno mis cuadernos y ejercicios de Simulación II. Explico los procedimientos paso a paso e incluyo el código, las gráficas y los resultados de cada trabajo.

## Notebook disponible

### Metropolis-Hastings en dos dimensiones

En este cuaderno genero una cadena de puntos con dos coordenadas, explico la regla de aceptación y represento la muestra con una nube de puntos y dos histogramas marginales.

- [Ver el notebook en GitHub](notebooks/M-H_tutorial_histogramas.ipynb).
- [Abrir el notebook en Google Colab](https://colab.research.google.com/github/Mar9718/Simulacion-II/blob/main/notebooks/M-H_tutorial_histogramas.ipynb).

Uso **10 000 estados**, el punto inicial **(0, 0)** y la **semilla 42**. Conservo los estados repetidos cuando rechazo una propuesta, porque también forman parte de la cadena.

## Ejecución

Trabajo con Python, NumPy y Pillow. En mi entorno local uso Jupyter con el kernel **Python (cientifico)**.

Para ejecutar el cuaderno, lo abro en Jupyter o mediante el enlace de Colab y ejecuto las celdas de arriba hacia abajo. Las gráficas están integradas en el notebook; al ejecutarlo también se guardan como archivos PNG en la carpeta de trabajo.

## Alcance de los resultados

Las gráficas y los conteos describen la simulación obtenida. La tasa de aceptación y la apariencia de las gráficas, por sí solas, no demuestran convergencia ni independencia entre los estados.

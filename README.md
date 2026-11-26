# Simulación II

En este repositorio reúno mis cuadernos y ejercicios de Simulación II. Explico los procedimientos paso a paso e incluyo el código, las gráficas y los resultados de cada trabajo.

## Cuadernos disponibles

Organizo los cuadernos del más antiguo al más reciente.

### 1. Metropolis-Hastings en dos dimensiones

En este cuaderno genero una cadena de puntos con dos coordenadas, explico la regla de aceptación y represento la muestra con una nube de puntos y dos histogramas marginales.

- [Ver el notebook en GitHub](notebooks/M-H_tutorial_histogramas.ipynb).
- [Abrir el notebook en Google Colab](https://colab.research.google.com/github/Mar9718/Simulacion-II/blob/main/notebooks/M-H_tutorial_histogramas.ipynb).

Uso **10 000 estados**, el punto inicial **(0, 0)** y la **semilla 42**. Conservo los estados repetidos cuando rechazo una propuesta, porque también forman parte de la cadena.

### 2. Caminata aleatoria sobre un grafo

En este cuaderno simulo una caminata entre cadenas de ceros y unos que no tienen dos unos consecutivos. Estimo el número medio de unos y comparo el resultado con la esperanza teórica. También represento la media acumulada y comparo la distribución simulada con la teórica mediante gráficas de barras.

- [Ver el notebook en GitHub](notebooks/Caminata_sobre_el_grafo_tutorial.ipynb).
- [Abrir el notebook en Google Colab](https://colab.research.google.com/github/Mar9718/Simulacion-II/blob/main/notebooks/Caminata_sobre_el_grafo_tutorial.ipynb).

Uso cadenas de **100 posiciones**, descarto **20 000 pasos iniciales** y guardo **100 000 observaciones**, con la **semilla 42**. Conservo los estados repetidos por rechazo y explico el conteo combinatorio que uso para obtener los valores teóricos.

### 3. Modelo SIR con Metropolis-Hastings

En este cuaderno programo Metropolis-Hastings para ajustar un modelo SIR a los datos de un brote de influenza. Explico cómo genero las propuestas, cómo decido si las acepto y cómo resumo los parámetros. Comparo las curvas del modelo con los datos y reviso sus diferencias mediante residuos y observaciones simuladas.

- [Ver el notebook en GitHub](notebooks/Modelo_SIR_MCMC.ipynb).
- [Abrir el notebook en Google Colab](https://colab.research.google.com/github/Mar9718/Simulacion-II/blob/main/notebooks/Modelo_SIR_MCMC.ipynb).

Uso **4 cadenas**, realizo **20 000 propuestas por cadena** y conservo **10 000 estados por cadena** después del calentamiento. Fijo las semillas **101, 202, 303 y 404**. Identifico las fuentes de los datos y del código adaptado, y explico las limitaciones del ajuste.

### 4. Ajuste bayesiano del modelo SIR con PyMC

En este cuaderno ajusto las tasas de transmisión y remoción del SIR y la dispersión de las observaciones. Defino los priors y la verosimilitud, obtengo muestras con Metropolis y reviso las cadenas con ArviZ. Interpreto la distribución posterior, los intervalos creíbles, las curvas del ajuste y las réplicas predictivas.

- [Ver el notebook en GitHub](notebooks/Modelo_SIR_PyMC.ipynb).
- [Abrir el notebook en Google Colab](https://colab.research.google.com/github/Mar9718/Simulacion-II/blob/main/notebooks/Modelo_SIR_PyMC.ipynb).

Uso **12 cadenas**, con **10 000 pasos de calentamiento** y **100 000 estados conservados por cadena**, y fijo la **semilla 101**. Los datos están incluidos en el cuaderno y sus fuentes se identifican al final. El ajuste describe la evolución general del brote; también señalo la sobreestimación de los últimos días y los conteos negativos que puede generar el supuesto de observación normal.

### 5. Movimiento browniano con deriva

En este cuaderno calculo la probabilidad de que un movimiento browniano con deriva tome valores entre **1 y 3 al tiempo 4**. Desarrollo la solución con la distribución normal y la comparo con una estimación por simulación. Represento 30 trayectorias con la franja del intervalo y la media teórica, y comparo el histograma de los valores finales con su densidad normal.

- [Ver el notebook en GitHub](notebooks/Browniano_deriva_probabilidad_t4.ipynb).
- [Abrir el notebook en Google Colab](https://colab.research.google.com/github/Mar9718/Simulacion-II/blob/main/notebooks/Browniano_deriva_probabilidad_t4.ipynb).

Uso **deriva 0.6**, **parámetro de varianza 0.25** y **100 000 trayectorias**, con **10 000 pasos por trayectoria** y **semilla 42**. Obtengo una probabilidad analítica de **0.6449902230** y una estimación de **0.64377**. Los gráficos reutilizan la misma simulación; la probabilidad corresponde al valor final del proceso.

### 6. Integral estocástica

En este cuaderno desarrollo la media y la varianza de $\int_0^t W_s^2\,ds$ y comparo los resultados con una simulación para $t=1$. Incluyo el ejemplo de una trayectoria, el histograma de las integrales y la comparación de los momentos con sus valores teóricos.

- [Ver el notebook en GitHub](notebooks/S2_Actividad_2_Ejercicio_2_Integral_estocastica.ipynb).
- [Abrir el notebook en Google Colab](https://colab.research.google.com/github/Mar9718/Simulacion-II/blob/main/notebooks/S2_Actividad_2_Ejercicio_2_Integral_estocastica.ipynb).

Uso **100 000 trayectorias**, **1000 subintervalos** y **semilla 42**.

## Modelos en AnyLogic

### Exploración y estimación de cavidades

Se presenta una exploradora que realiza dos visitas a cada cavidad, registra los encuentros con su primer recorrido y estima el área mediante sus longitudes y ese conteo. El modelo incluye vistas en planta y en 3D, entradas designadas, generación de nuevos pares y exportación de resultados.

- [Reporte de avance, método, gráficas y datos](anylogic/exploracion_cavidades/README.md).
- [Carpeta del modelo para abrir en AnyLogic](anylogic/exploracion_cavidades/modelo_anylogic/).
- [Descargar el proyecto de AnyLogic para revisión](anylogic/exploracion_cavidades/entrega/Proyecto_AnyLogic.zip).
- [Informe de avance en PDF](anylogic/exploracion_cavidades/documentos/Avance_2026-11-26.pdf).

La versión actual utiliza **AnyLogic 8.9.10 PLE**, cavidades de **875 y 1750 mm²** y **5000 mm por cavidad**, con repartos **25/75** y **50/50**. El conjunto inicial conserva **cinco pares por reparto**: se obtuvieron **4/5** y **3/5 aciertos**, respectivamente. El reporte separa ese conjunto de los pares añadidos después y del antecedente con 1000 mm e inicio interior. Son resultados exploratorios: el cambio de distancia también cambia el lugar de inicio y no demuestra la superioridad general de un reparto.

Para revisar el proyecto se descarga la carpeta o el archivo ZIP, se abre `Exploradora3D_Interactivo.alp` y se ejecuta `Simulation`. Las instrucciones y las condiciones de uso de AnyLogic acompañan al modelo. La entrega corresponde a una actividad docente de Simulación II.

## Ejecución

Trabajo con **Python y NumPy**. Para las gráficas de Metropolis-Hastings en dos dimensiones uso **Pillow**; en la caminata sobre el grafo uso **Matplotlib** y calculo las combinaciones con **SciPy**.

Para la actividad de integral estocástica uso **NumPy**, **Matplotlib**, **Numba** e **IPython**.

En el SIR con Metropolis-Hastings uso **SciPy** para resolver las ecuaciones, **pandas** para las tablas y **Matplotlib** para las gráficas.

Ejecuto las celdas de arriba hacia abajo, empezando con un kernel limpio. Las gráficas y los resultados están integrados en los notebooks; también incluyo sus enlaces de **Google Colab**.

Para el movimiento browniano utilicé **Python 3.12**, **NumPy 2.5.3**, **SciPy 1.18.1**, **Matplotlib 3.11.2** y **Numba 0.68.0**. En un entorno virtual activo con Python 3.12, instalo las bibliotecas y abro JupyterLab:

```bash
python -m pip install numpy==2.5.3 scipy==1.18.1 matplotlib==3.11.2 numba==0.68.0 jupyterlab
python -m jupyterlab
```

Abro `notebooks/Browniano_deriva_probabilidad_t4.ipynb`. Defino los parámetros una sola vez y uso `numero_a_graficar` para elegir cuántas trayectorias muestro. Comprobé la ejecución completa desde un kernel limpio en Jupyter. La ejecución en Colab no se ha verificado.

Para el SIR con PyMC utilicé **Python 3.12 y PyMC 5.25.1**. Registro las versiones de las dependencias directas en [requirements-sir.txt](requirements-sir.txt). En un entorno virtual activo con Python 3.12, instalo esas bibliotecas y abro JupyterLab desde la carpeta del repositorio:

```bash
python -m pip install -r requirements-sir.txt
python -m jupyterlab
```

Abro `notebooks/Modelo_SIR_PyMC.ipynb` y selecciono el kernel del entorno donde instalé las bibliotecas. El cuaderno genera sus archivos de muestras y figuras en `outputs/sir_pymc_sencillo/suave/`; no necesito descargar datos adicionales. La ejecución completa se comprobó en Jupyter con las versiones indicadas. En Colab debo preparar las bibliotecas compatibles; esa ejecución no se ha verificado.

Durante el muestreo aparece una barra por cadena. En **Visual Studio Code** abro el archivo `.ipynb` con la extensión Jupyter y selecciono el entorno de Python correspondiente. Las dependencias incluyen `ipywidgets` para mostrar el avance. La preparación de la primera ejecución puede tardar; el mensaje de inicio se muestra antes de esa preparación. El archivo HTML permite consultar una ejecución terminada y no muestra progreso en vivo.

## Alcance de los resultados

Las gráficas y los conteos describen las simulaciones obtenidas. La tasa de aceptación, el descarte de pasos iniciales y la apariencia de las gráficas, por sí solos, no demuestran convergencia ni independencia entre los estados.

En el SIR con PyMC, los diagnósticos de las cadenas respaldan los resúmenes de la posterior bajo los supuestos elegidos. Los residuos y las réplicas permiten examinar el ajuste a esos mismos datos; no constituyen una evaluación con observaciones nuevas. El notebook identifica el código adaptado.

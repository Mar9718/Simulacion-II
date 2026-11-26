# Modelo de exploración de cavidades en AnyLogic

Este proyecto contiene una simulación docente en dos dimensiones, con presentación en planta y en 3D, para comparar dos cavidades y dos repartos de una distancia total entre visitas.

> Si la exploradora recorre la misma distancia total en dos visitas, ¿cambia la frecuencia con la que el conteo de cruces le permite distinguir la cavidad pequeña de la grande según cómo reparta esa distancia?

## Requisito y condiciones de uso

Se requiere **AnyLogic 8.9.10**, con edición Personal Learning Edition (PLE) para este uso docente. Las bibliotecas necesarias forman parte de la instalación de AnyLogic. No se requieren recursos 3D externos, paquetes de Python ni archivos Java adicionales.

Antes de utilizar el modelo, se debe leer y aceptar el [AnyLogic Model End User Agreement](ANYLOGIC_MODEL_END_USER_AGREEMENT.txt), incluido íntegramente junto con sus usos permitidos y no permitidos. También puede consultarse el [portal de información legal de AnyLogic](https://www.anylogic.com/downloads/legal-info/). La distribución del archivo del proyecto no sustituye la instalación ni las condiciones de licencia de AnyLogic.

## Apertura y ejecución

1. Extraer esta carpeta completa en una ubicación con permiso de escritura. El modelo debe ejecutarse desde los archivos extraídos.
2. Abrir AnyLogic y seleccionar **File → Open**; elegir [Exploradora3D_Interactivo.alp](Exploradora3D_Interactivo.alp).
3. En el árbol del proyecto, seleccionar el experimento **Simulation** y pulsar **Run**.
4. Esperar el cálculo de la serie inicial. Se muestran cinco pares por reparto, las cavidades pequeña y grande y sus recorridos en planta y en 3D.

El cálculo de las trayectorias y de sus resultados se realiza antes de mostrarlos. La reproducción posterior permite seguir las visitas y conserva los resultados calculados.

## Controles de la presentación

| Control | Función |
| --- | --- |
| Mostrar 25/75 / Mostrar 50/50 | Seleccionar el reparto y el último par mostrado en él. |
| Reproducir visitas | Representar de nuevo las dos visitas del par seleccionado. |
| Ver final | Mostrar completas las trayectorias del par. |
| Nueva simulación | Añadir un par de caminatas para cada cavidad al reparto seleccionado y actualizar sus contadores. |
| Velocidad ×1 / ×5 / ×10 | Cambiar la velocidad de reproducción, sin modificar las trayectorias ni los resultados. |

Cada par contiene una ejecución en la cavidad pequeña y una en la grande; cada ejecución consta de dos visitas. La primera visita se representa en azul, la segunda en naranja y la entrada en verde. Los contadores de aciertos, inversiones, empates y pares completos se mantienen por reparto. Los nuevos pares utilizan flujos aleatorios predefinidos por sus identificadores.

## Configuración del modelo

| Parámetro | Valor |
| --- | --- |
| Cavidad pequeña | 25 × 35 mm; área de 875 mm². |
| Cavidad grande | 25√2 × 35√2 mm; área de 1750 mm². |
| Entradas | Centradas en el borde inferior; anchuras de 1 mm y √2 mm. |
| Inicio de cada visita | Punto sorteado de manera independiente dentro de su entrada. |
| Distancia total por ejecución de cavidad | 5000 mm. |
| Reparto 25/75 | Primera visita de 1250 mm; segunda de 3750 mm. |
| Reparto 50/50 | Dos visitas de 2500 mm. |
| Paso de dirección | 1 mm; ángulo uniforme nuevo entre 0 y 2π por paso. |
| Paredes | Reflexión especular, incluidos los subtramos de rebote; la entrada permanece reflectante durante la visita. |
| Serie inicial | Cinco pares por reparto; diez pares y veinte ejecuciones de cavidad en total. |

El movimiento es plano, con Z = 0. La vista 3D presenta ese mismo modelo. La caminata es una idealización geométrica; la velocidad de reproducción no representa una rapidez biológica.

El observable **N** cuenta encuentros puntuales únicos con el rastro de la primera visita, agrupados por episodio y avance en la segunda visita. La clasificación regional **C** se registra por separado y puede quedar sin definir cuando no existen las condiciones geométricas necesarias. Los solapamientos de longitud positiva se registran como fallas explícitas.

Para N > 0, el área se estima mediante **Â = 2LS/(πN)**, usando las longitudes efectivamente recorridas. N = 0 conserva un resultado válido para clasificar el par y deja el área sin estimación finita. El par se clasifica como acierto cuando N de la cavidad pequeña supera al de la grande; inversión cuando es menor; empate cuando son iguales. El área verdadera se utiliza para evaluar el error de la estimación.

## Archivos de resultados

Cada inicio crea una carpeta nueva:

```text
resultados/
└── interactivo_<identificador>/
    ├── configuracion.txt
    ├── semillas.csv
    ├── flujos_efectivos.csv
    ├── trayectorias.csv
    ├── eventos.csv
    ├── cavidades.csv
    ├── pares.csv
    ├── resumen_repartos.csv
    ├── estado_ejecucion.txt
    └── cortes/
        ├── corte_0000/
        ├── corte_0001/
        └── …
```

La base `resultados` se resuelve respecto del **directorio de trabajo del proceso de AnyLogic** (`user.dir`), que debe permitir la escritura. Cuando este directorio es la carpeta del modelo, `resultados` queda junto a este LEEME. Si la instalación utiliza otro directorio de trabajo, los resultados se guardan allí. `estado_ejecucion.txt` registra la ubicación relativa de la sesión.

`corte_0000` conserva la serie inicial. Cada uso de **Nueva simulación** crea una revisión posterior con los archivos de ese momento. Los cortes anteriores se conservan sin sobrescritura, mientras los archivos de la raíz de la sesión reflejan la revisión más reciente. Los valores sin estimación o clasificación definida se guardan como campos vacíos; no equivalen a cero.

## Alcance de esta entrega

Se entrega el proyecto editable con sus instrucciones y el acuerdo de uso de AnyLogic. La copia conserva las reglas, parámetros, semillas, detector y controles del modelo de trabajo; únicamente adapta el destino de resultados a una ruta portable y el registro de su ubicación a una ruta relativa.

El código de esta copia se comprobó por compilación con el JDK y las bibliotecas de AnyLogic 8.9.10. Se comprobó la creación y escritura de los archivos y cortes desde una carpeta con espacios, sin ejecutar nuevas simulaciones científicas. La apertura y la ejecución mediante la interfaz de esta copia portable quedan pendientes de comprobación en el equipo receptor.

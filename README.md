# Aplicación de Simulación de Modelos Epidemiológicos

Esta es una aplicación web interactiva desarrollada en Python con Streamlit para simular y visualizar modelos epidemiológicos clásicos. La herramienta fue creada como un complemento práctico al proyecto de investigación sobre modelos matemáticos para la predicción de enfermedades de Maria Victoria Criado Carretero.

## Modelos Incluidos

- **SIR**: Susceptible - Infectado - Recuperado
- **SEIR**: Susceptible - Expuesto - Infectado - Recuperado
- **SIS**: Susceptible - Infectado - Susceptible
- **SI**: Susceptible - Infectado

## Características

- **Interfaz Interactiva**: Ajusta los parámetros de cada modelo y observa los resultados en tiempo real.
- **Visualización Clara**: Gráficos interactivos que muestran la evolución de cada compartimento de la población a lo largo del tiempo.
- **Educativo**: Incluye breves descripciones de cada modelo directamente en la aplicación.

## Tecnologías Utilizadas

Este proyecto se ha construido utilizando las siguientes bibliotecas de Python:

- **Streamlit**: Es el framework principal sobre el que corre la aplicación. Permite crear y compartir aplicaciones web interactivas para proyectos de ciencia de datos de forma rápida y sencilla.
- **NumPy**: Se utiliza para realizar cálculos numéricos eficientes, especialmente en la preparación de los arrays de tiempo para las simulaciones.
- **SciPy**: Fundamental para el núcleo de la simulación. Específicamente, se usa la función `odeint` para resolver las ecuaciones diferenciales ordinarias (EDOs) que gobiernan cada modelo epidemiológico.
- **Pandas**: Se emplea para organizar los datos resultantes de las simulaciones en `DataFrames`, lo que facilita su manipulación y posterior visualización.
- **Plotly Express**: Es la biblioteca encargada de generar los gráficos interactivos. Permite crear visualizaciones ricas y dinámicas que ayudan a interpretar los resultados de los modelos.

## Instalación

Para ejecutar esta aplicación en tu máquina local, sigue estos pasos:

1.  **Clona el repositorio (o descarga los archivos)**

2.  **Crea y activa un entorno virtual**

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
    *En Windows, el comando de activación es `\.venv\Scripts\activate`*

3.  **Instala las dependencias**

    Asegúrate de tener el archivo `requirements.txt` en el mismo directorio.

    ```bash
    pip install -r requirements.txt
    ```

## Uso

Una vez instaladas las dependencias, puedes ejecutar la aplicación con el siguiente comando:

```bash
streamlit run main.py
```

Esto abrirá una nueva pestaña en tu navegador con la aplicación en funcionamiento.

## Contribuciones

Este proyecto fue creado con un propósito educativo y está abierto a contribuciones. Si tienes alguna idea para mejorarlo, no dudes en abrir un *issue* o enviar un *pull request*.
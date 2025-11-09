
# -*- coding: utf-8 -*-
"""
Aplicación principal de simulación de modelos epidemiológicos.
"""

import streamlit as st
import plotly.express as px
import pandas as pd

from models import modelo_sir, modelo_seir, modelo_sis, modelo_si
from ui import sidebar

def main():
    """
    Función principal de la aplicación.
    """
    st.title("Simulación de Modelos Epidemiológicos")
    st.markdown("""
    Esta aplicación permite simular diferentes modelos epidemiológicos 
    y visualizar los resultados de forma interactiva. 
    Creada como complemento al proyecto de investigación de **María Victoria Criado**.
    """)

    modelo, parametros = sidebar()

    if modelo == "SIR":
        df = modelo_sir(
            poblacion=parametros["poblacion"],
            infectados_iniciales=parametros["infectados_iniciales"],
            recuperados_iniciales=parametros["recuperados_iniciales"],
            beta=parametros["beta"],
            gamma=parametros["gamma"],
            dias=parametros["dias"]
        )
        st.header("Modelo SIR")
        st.markdown("""
        El modelo SIR divide la población en tres compartimentos: 
        Susceptibles (S), Infectados (I) y Recuperados (R).
        """)
        with st.expander("Parámetros Utilizados"):
            st.write(parametros)
        fig = px.line(df, x="Día", y=["Susceptibles", "Infectados", "Recuperados"], 
                      title="Simulación del Modelo SIR")
        st.plotly_chart(fig)
        with st.expander("Datos de la Simulación"):
            st.dataframe(df)

    elif modelo == "SEIR":
        df = modelo_seir(
            poblacion=parametros["poblacion"],
            infectados_iniciales=parametros["infectados_iniciales"],
            recuperados_iniciales=parametros["recuperados_iniciales"],
            expuestos_iniciales=parametros["expuestos_iniciales"],
            beta=parametros["beta"],
            gamma=parametros["gamma"],
            sigma=parametros["sigma"],
            dias=parametros["dias"]
        )
        st.header("Modelo SEIR")
        st.markdown("""
        El modelo SEIR añade un compartimento de Expuestos (E) al modelo SIR. 
        Las personas en este compartimento han sido infectadas pero aún no son infecciosas.
        """)
        with st.expander("Parámetros Utilizados"):
            st.write(parametros)
        fig = px.line(df, x="Día", y=["Susceptibles", "Expuestos", "Infectados", "Recuperados"],
                        title="Simulación del Modelo SEIR")
        st.plotly_chart(fig)
        with st.expander("Datos de la Simulación"):
            st.dataframe(df)

    elif modelo == "SIS":
        df = modelo_sis(
            poblacion=parametros["poblacion"],
            infectados_iniciales=parametros["infectados_iniciales"],
            beta=parametros["beta"],
            gamma=parametros["gamma"],
            dias=parametros["dias"]
        )
        st.header("Modelo SIS")
        st.markdown("""
        En el modelo SIS (Susceptible-Infectado-Susceptible), los individuos 
        recuperados no adquieren inmunidad y vuelven a ser susceptibles.
        """)
        with st.expander("Parámetros Utilizados"):
            st.write(parametros)
        fig = px.line(df, x="Día", y=["Susceptibles", "Infectados"],
                        title="Simulación del Modelo SIS")
        st.plotly_chart(fig)
        with st.expander("Datos de la Simulación"):
            st.dataframe(df)

    elif modelo == "SI":
        df = modelo_si(
            poblacion=parametros["poblacion"],
            infectados_iniciales=parametros["infectados_iniciales"],
            beta=parametros["beta"],
            dias=parametros["dias"]
        )
        st.header("Modelo SI")
        st.markdown("""
        El modelo SI (Susceptible-Infectado) es el más simple. 
        Los individuos infectados permanecen así de por vida.
        """)
        with st.expander("Parámetros Utilizados"):
            st.write(parametros)
        fig = px.line(df, x="Día", y=["Susceptibles", "Infectados"],
                        title="Simulación del Modelo SI")
        st.plotly_chart(fig)
        with st.expander("Datos de la Simulación"):
            st.dataframe(df)

if __name__ == "__main__":
    main()

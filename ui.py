
# -*- coding: utf-8 -*-
"""
Módulo para la interfaz de usuario de la aplicación.
"""

import streamlit as st

def sidebar():
    """
    Crea la barra lateral con los controles de la aplicación.

    Returns:
        tuple: Tupla con el modelo seleccionado y un diccionario de parámetros.
    """
    st.sidebar.title("Parámetros de Simulación")
    
    modelo = st.sidebar.selectbox(
        "Seleccione el Modelo",
        ("SIR", "SI", "SIS", "SEIR")
    )

    poblacion = st.sidebar.number_input("Población Total", min_value=1, value=1000)
    infectados_iniciales = st.sidebar.number_input("Infectados Iniciales", min_value=1, value=10)
    dias = st.sidebar.number_input("Días de Simulación", min_value=1, value=100)

    parametros = {
        "poblacion": poblacion,
        "infectados_iniciales": infectados_iniciales,
        "dias": dias
    }

    if modelo == "SIR":
        beta = st.sidebar.slider("Beta (Tasa de transmisión)", 0.0, 1.0, 0.2)
        gamma = st.sidebar.slider("Gamma (Tasa de recuperación)", 0.0, 1.0, 0.1)
        parametros["beta"] = beta
        parametros["gamma"] = gamma
        parametros["recuperados_iniciales"] = st.sidebar.number_input("Recuperados Iniciales", min_value=0, value=0)

    elif modelo == "SEIR":
        beta = st.sidebar.slider("Beta (Tasa de transmisión)", 0.0, 1.0, 0.2)
        gamma = st.sidebar.slider("Gamma (Tasa de recuperación)", 0.0, 1.0, 0.1)
        sigma = st.sidebar.slider("Sigma (Tasa de incubación)", 0.0, 1.0, 0.1)
        parametros["beta"] = beta
        parametros["gamma"] = gamma
        parametros["sigma"] = sigma
        parametros["expuestos_iniciales"] = st.sidebar.number_input("Expuestos Iniciales", min_value=0, value=0)
        parametros["recuperados_iniciales"] = st.sidebar.number_input("Recuperados Iniciales", min_value=0, value=0)

    elif modelo == "SIS":
        beta = st.sidebar.slider("Beta (Tasa de transmisión)", 0.0, 1.0, 0.2)
        gamma = st.sidebar.slider("Gamma (Tasa de recuperación)", 0.0, 1.0, 0.1)
        parametros["beta"] = beta
        parametros["gamma"] = gamma

    elif modelo == "SI":
        beta = st.sidebar.slider("Beta (Tasa de transmisión)", 0.0, 1.0, 0.2)
        parametros["beta"] = beta

    return modelo, parametros

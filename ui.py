
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
        ("SIR", "SI", "SIS", "SEIR", "Modelo Ross-Macdonald")
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

    elif modelo == "Modelo Ross-Macdonald":
        modo_sim = st.sidebar.selectbox(
            "Modo de Simulación",
            ("Simulación Simple", "Comparar por Temperatura", "Comparar por Humedad")
        )
        parametros["modo_sim"] = modo_sim

        st.sidebar.markdown("### Condiciones Climáticas")
        
        if modo_sim == "Simulación Simple":
            temp = st.sidebar.slider("Temperatura (°C)", 10.0, 40.0, 28.0)
            humedad = st.sidebar.slider("Humedad Relativa (%)", 0.0, 100.0, 70.0)
            parametros["temp"] = temp
            parametros["humedad"] = humedad
            
        elif modo_sim == "Comparar por Temperatura":
            humedad = st.sidebar.slider("Humedad Fija (%)", 0.0, 100.0, 70.0)
            st.sidebar.markdown("#### Configuración de Temperatura")
            temp_base = st.sidebar.number_input("Temp. Base (°C)", value=24.0, step=1.0)
            temp_step = st.sidebar.number_input("Incremento (°C)", value=2.0, step=1.0)
            num_escenarios = st.sidebar.slider("Nº Escenarios", 2, 5, 3)
            
            parametros["humedad"] = humedad
            parametros["temp_base"] = temp_base
            parametros["temp_step"] = temp_step
            parametros["num_escenarios"] = num_escenarios
            
        elif modo_sim == "Comparar por Humedad":
            temp = st.sidebar.slider("Temperatura Fija (°C)", 10.0, 40.0, 28.0)
            st.sidebar.markdown("#### Configuración de Humedad")
            hum_base = st.sidebar.number_input("Humedad Base (%)", value=50.0, step=5.0)
            hum_step = st.sidebar.number_input("Aymento (%)", value=10.0, step=5.0)
            num_escenarios = st.sidebar.slider("Nº Escenarios", 2, 5, 3)
            
            parametros["temp"] = temp
            parametros["hum_base"] = hum_base
            parametros["hum_step"] = hum_step
            parametros["num_escenarios"] = num_escenarios

        st.sidebar.markdown("### Parámetros Biológicos")
        prob_h_v = st.sidebar.slider("Prob. Transmisión H->V (b)", 0.0, 1.0, 0.5)
        prob_v_h = st.sidebar.slider("Prob. Transmisión V->H (c)", 0.0, 1.0, 0.5)
        gamma = st.sidebar.slider("Tasa de Recuperación H (gamma)", 0.0, 1.0, 0.14)
        
        parametros["b"] = prob_h_v
        parametros["c"] = prob_v_h
        parametros["gamma"] = gamma
        parametros["infectados_v_iniciales"] = st.sidebar.number_input("Mosquitos Infectados Iniciales", min_value=0, value=100)

    return modelo, parametros


# -*- coding: utf-8 -*-
"""
Aplicación principal de simulación de modelos epidemiológicos.
"""

import streamlit as st
import plotly.express as px
import pandas as pd

from models import modelo_sir, modelo_seir, modelo_sis, modelo_si, modelo_ross_macdonald
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

    elif modelo == "Impacto Climático":
        st.header("Análisis de Impacto Climático (Cambio de Temperatura)")
        st.markdown(f"""
        Este análisis simula cómo el aumento de la temperatura afecta la propagación de una epidemia. 
        Se asume que la **Tasa de Transmisión (Beta)** aumenta un **{parametros['sensibilidad']*100}%** por cada grado Celsius adicional, 
        simulando una mayor actividad de vectores (como mosquitos) o una incubación más rápida.
        
        **Modelo Base**: SEIR (Susceptible - Expuesto - Infectado - Recuperado)
        """)

        dfs = []
        temp_base = parametros["temp_base"]
        temp_step = parametros["temp_step"]
        beta_base = parametros["beta"]
        sensibilidad = parametros["sensibilidad"]

        for i in range(parametros["num_escenarios"]):
            temp_actual = temp_base + (i * temp_step)
            # Factor de aumento: 1 + (sensibilidad * diferencia_temp)
            # Si diferencia es 0 (temp base), factor es 1.
            factor = 1 + (sensibilidad * (temp_actual - temp_base))
            beta_actual = beta_base * factor
            
            # Ejecutar simulación SEIR
            df_temp = modelo_seir(
                poblacion=parametros["poblacion"],
                infectados_iniciales=parametros["infectados_iniciales"],
                recuperados_iniciales=parametros["recuperados_iniciales"],
                expuestos_iniciales=parametros["expuestos_iniciales"],
                beta=beta_actual,
                gamma=parametros["gamma"],
                sigma=parametros["sigma"],
                dias=parametros["dias"]
            )
            
            # Marcar el escenario en el DataFrame
            df_temp["Escenario"] = f"{temp_actual}°C (Beta: {beta_actual:.2f})"
            df_temp["Temp"] = temp_actual
            
            dfs.append(df_temp)

        # Concatenar todos los resultados
        df_final = pd.concat(dfs)

        with st.expander("Parámetros Utilizados"):
            st.write(parametros)

        # Gráfico Comparativo
        fig = px.line(df_final, x="Día", y="Infectados", color="Escenario",
                      title=f"Comparativa de Infectados según Temperatura (Sensibilidad: {sensibilidad:.2f}/°C)",
                      labels={"Infectados": "Número de Personas Infectadas"})
        
        st.plotly_chart(fig)
        
        with st.expander("Datos de la Simulación"):
            st.dataframe(df_final)

    elif modelo == "Modelo Ross-Macdonald":
        # Documentación del Modelo
        st.header("Modelo Ross-Macdonald (Enfermedades por Vectores)")
        with st.expander("📘 Explicación del Modelo y Factores Climáticos", expanded=True):
            st.markdown("""
            El modelo **Ross-Macdonald** es el estándar para simular enfermedades transmitidas por vectores (como mosquitos). 
            A diferencia de los modelos SIR directos, este modelo acopla dos poblaciones:
            
            1.  **Humanos**: Susceptibles ($S_h$), Infectados ($I_h$), Recuperados ($R_h$).
            2.  **Vectores (Mosquitos)**: Susceptibles ($S_v$), Infectados ($I_v$).
            
            ### Impacto del Clima
            La Temperatura y la Humedad modifican el comportamiento biológico del vector:
            *   **Temperatura ($T$)**: Afecta la **Tasa de Picaduras ($a$)**. Los mosquitos pican más frecuentemente a mayor temperatura (hasta cierto límite).
                *   *Fórmula*: $a = 0.2 + 0.02 \\times (T - 20)$
            *   **Humedad ($H$)**: Afecta la **Densidad de Mosquitos ($m$)**. Mayor humedad favorece los criaderos y la supervivencia.
                *   *Fórmula*: $m = 1 + 0.05 \\times (H - 30)$
            """)

        modo_sim = parametros.get("modo_sim", "Simulación Simple")
        
        # Función auxiliar para calcular parámetros dependientes
        def calc_params_bio(temp, hum):
            # Tasa de picaduras (a)
            a_val = max(0.05, 0.2 + 0.02 * (temp - 20))
            # Densidad (m)
            if hum < 30:
                m_val = max(0.1, hum / 100)
            else:
                m_val = 1 + 0.05 * (hum - 30)
            return a_val, m_val

        mu_mosq = 0.1 # Mortalidad base

        if modo_sim == "Simulación Simple":
            temp = parametros["temp"]
            hum = parametros["humedad"]
            a_calc, m_calc = calc_params_bio(temp, hum)
            
            # Ejecutar Simulación
            df = modelo_ross_macdonald(
                poblacion_h=parametros["poblacion"],
                infectados_h=parametros["infectados_iniciales"],
                infectados_v_iniciales=parametros["infectados_v_iniciales"],
                m=m_calc,
                a=a_calc,
                b=parametros["b"],
                c=parametros["c"],
                gamma=parametros["gamma"],
                mu=mu_mosq,
                dias=parametros["dias"]
            )
            
            with st.expander("Parámetros Utilizados", expanded=True):
                col1, col2, col3 = st.columns(3)
                col1.metric("Temperatura", f"{temp}°C", f"Picaduras (a): {a_calc:.2f}/día")
                col2.metric("Humedad", f"{hum}%", f"Densidad (m): {m_calc:.2f}")
                col3.metric("R0 Estimado", f"{(m_calc * a_calc**2 * parametros['b'] * parametros['c']) / (parametros['gamma'] * mu_mosq):.2f}")
                st.write(parametros)

            # Gráficos Individuales
            st.subheader("Dinámica de la Infección")
            fig_h = px.line(df, x="Día", y=["Humanos Susceptibles", "Humanos Infectados", "Humanos Recuperados"],
                            title="Población Humana", color_discrete_sequence=["blue", "red", "green"])
            st.plotly_chart(fig_h)
            
            fig_v = px.line(df, x="Día", y=["Mosquitos Susceptibles", "Mosquitos Infectados"],
                            title="Población de Mosquitos (Vectores)", color_discrete_sequence=["orange", "purple"])
            st.plotly_chart(fig_v)
            
            with st.expander("Datos Detallados"):
                st.dataframe(df)

        else:
            # Lógica Comparativa (Temp o Humedad)
            dfs = []
            param_list = []
            
            hum_fija = parametros.get("humedad")
            temp_fija = parametros.get("temp")
            
            is_temp_mode = (modo_sim == "Comparar por Temperatura")
            
            num_escenarios = parametros["num_escenarios"]
            
            base_val = parametros["temp_base"] if is_temp_mode else parametros["hum_base"]
            step_val = parametros["temp_step"] if is_temp_mode else parametros["hum_step"]

            st.subheader(f"Comparativa: Variando {'Temperatura' if is_temp_mode else 'Humedad'}")
            
            for i in range(num_escenarios):
                current_val = base_val + (i * step_val)
                
                if is_temp_mode:
                    t_iter = current_val
                    h_iter = hum_fija
                    label = f"{t_iter}°C (Hum: {h_iter}%)"
                else:
                    t_iter = temp_fija
                    h_iter = current_val
                    label = f"{h_iter}% Hum (Temp: {t_iter}°C)"
                
                a_iter, m_iter = calc_params_bio(t_iter, h_iter)
                
                df_iter = modelo_ross_macdonald(
                    poblacion_h=parametros["poblacion"],
                    infectados_h=parametros["infectados_iniciales"],
                    infectados_v_iniciales=parametros["infectados_v_iniciales"],
                    m=m_iter,
                    a=a_iter,
                    b=parametros["b"],
                    c=parametros["c"],
                    gamma=parametros["gamma"],
                    mu=mu_mosq,
                    dias=parametros["dias"]
                )
                
                df_iter["Escenario"] = label
                # Guardamos solo lo necesario para comparar humanos infectados
                df_clean = df_iter[["Día", "Humanos Infectados", "Escenario"]]
                dfs.append(df_clean)
                
                param_list.append({
                    "Escenario": label,
                    "Temp": t_iter,
                    "Humedad": h_iter,
                    "Picaduras (a)": round(a_iter, 3),
                    "Densidad (m)": round(m_iter, 3)
                })

            df_final = pd.concat(dfs)

            with st.expander("Parámetros de los Escenarios", expanded=True):
                st.table(pd.DataFrame(param_list))

            # Gráfico Comparativo
            fig = px.line(df_final, x="Día", y="Humanos Infectados", color="Escenario",
                          title=f"Comparativa de Infecciones Humanas - {modo_sim}",
                          labels={"Humanos Infectados": "Personas Infectadas"})
            st.plotly_chart(fig)
            
            with st.expander("Datos Completos de la Simulación"):
                st.dataframe(df_final)

if __name__ == "__main__":
    main()

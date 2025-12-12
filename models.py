
# -*- coding: utf-8 -*-
"""
Módulo para implementar los modelos epidemiológicos.
"""

import numpy as np
from scipy.integrate import odeint
import pandas as pd

# Modelo SIR
def modelo_sir(poblacion, infectados_iniciales, recuperados_iniciales, beta, gamma, dias):
    """
    Simula el modelo SIR.

    Args:
        poblacion (int): Población total.
        infectados_iniciales (int): Número inicial de infectados.
        recuperados_iniciales (int): Número inicial de recuperados.
        beta (float): Tasa de transmisión.
        gamma (float): Tasa de recuperación.
        dias (int): Número de días para simular.

    Returns:
        pandas.DataFrame: DataFrame con los resultados de la simulación.
    """
    # Población susceptible inicial
    susceptibles_iniciales = poblacion - infectados_iniciales - recuperados_iniciales
    
    # Vector de condiciones iniciales
    y0 = susceptibles_iniciales, infectados_iniciales, recuperados_iniciales
    
    # Puntos de tiempo
    t = np.linspace(0, dias, dias)

    # Ecuaciones diferenciales del modelo SIR
    def deriv(y, t, N, beta, gamma):
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

    # Integrar las ecuaciones SIR a lo largo del tiempo
    ret = odeint(deriv, y0, t, args=(poblacion, beta, gamma))
    S, I, R = ret.T

    # Crear DataFrame con los resultados
    df = pd.DataFrame({
        'Día': t,
        'Susceptibles': S,
        'Infectados': I,
        'Recuperados': R
    })
    return df

# Modelo SEIR
def modelo_seir(poblacion, infectados_iniciales, recuperados_iniciales, expuestos_iniciales, beta, gamma, sigma, dias):
    """
    Simula el modelo SEIR.

    Args:
        poblacion (int): Población total.
        infectados_iniciales (int): Número inicial de infectados.
        recuperados_iniciales (int): Número inicial de recuperados.
        expuestos_iniciales (int): Número inicial de expuestos.
        beta (float): Tasa de transmisión.
        gamma (float): Tasa de recuperación.
        sigma (float): Tasa de incubación.
        dias (int): Número de días para simular.

    Returns:
        pandas.DataFrame: DataFrame con los resultados de la simulación.
    """
    susceptibles_iniciales = poblacion - infectados_iniciales - recuperados_iniciales - expuestos_iniciales
    y0 = susceptibles_iniciales, expuestos_iniciales, infectados_iniciales, recuperados_iniciales
    t = np.linspace(0, dias, dias)

    def deriv(y, t, N, beta, gamma, sigma):
        S, E, I, R = y
        dSdt = -beta * S * I / N
        dEdt = beta * S * I / N - sigma * E
        dIdt = sigma * E - gamma * I
        dRdt = gamma * I
        return dSdt, dEdt, dIdt, dRdt

    ret = odeint(deriv, y0, t, args=(poblacion, beta, gamma, sigma))
    S, E, I, R = ret.T

    df = pd.DataFrame({
        'Día': t,
        'Susceptibles': S,
        'Expuestos': E,
        'Infectados': I,
        'Recuperados': R
    })
    return df

# Modelo SIS
def modelo_sis(poblacion, infectados_iniciales, beta, gamma, dias):
    """
    Simula el modelo SIS.

    Args:
        poblacion (int): Población total.
        infectados_iniciales (int): Número inicial de infectados.
        beta (float): Tasa de transmisión.
        gamma (float): Tasa de recuperación.
        dias (int): Número de días para simular.

    Returns:
        pandas.DataFrame: DataFrame con los resultados de la simulación.
    """
    susceptibles_iniciales = poblacion - infectados_iniciales
    y0 = susceptibles_iniciales, infectados_iniciales
    t = np.linspace(0, dias, dias)

    def deriv(y, t, N, beta, gamma):
        S, I = y
        dSdt = -beta * S * I / N + gamma * I
        dIdt = beta * S * I / N - gamma * I
        return dSdt, dIdt

    ret = odeint(deriv, y0, t, args=(poblacion, beta, gamma))
    S, I = ret.T

    df = pd.DataFrame({
        'Día': t,
        'Susceptibles': S,
        'Infectados': I
    })
    return df

# Modelo SI
def modelo_si(poblacion, infectados_iniciales, beta, dias):
    """
    Simula el modelo SI.

    Args:
        poblacion (int): Población total.
        infectados_iniciales (int): Número inicial de infectados.
        beta (float): Tasa de transmisión.
        dias (int): Número de días para simular.

    Returns:
        pandas.DataFrame: DataFrame con los resultados de la simulación.
    """
    susceptibles_iniciales = poblacion - infectados_iniciales
    y0 = susceptibles_iniciales, infectados_iniciales
    t = np.linspace(0, dias, dias)

    def deriv(y, t, N, beta):
        S, I = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N
        return dSdt, dIdt

    ret = odeint(deriv, y0, t, args=(poblacion, beta))
    S, I = ret.T

    df = pd.DataFrame({
        'Día': t,
        'Susceptibles': S,
        'Infectados': I
    })
    df = pd.DataFrame({
        'Día': t,
        'Susceptibles': S,
        'Infectados': I
    })
    return df

# Modelo Ross-Macdonald (Hospedador-Vector)
def modelo_ross_macdonald(poblacion_h, infectados_h, infectados_v_iniciales, m, a, b, c, gamma, mu, dias):
    """
    Simula el modelo Ross-Macdonald (Humanos y Mosquitos).
    
    Args:
        poblacion_h (int): Población humana total.
        infectados_h (int): Humanos infectados iniciales.
        infectados_v_iniciales (int): Mosquitos infectados iniciales.
        m (float): Densidad de mosquitos por humano (V/H).
        a (float): Tasa de picaduras por mosquito y día.
        b (float): Probabilidad de transmisión Mosquito -> Humano.
        c (float): Probabilidad de transmisión Humano -> Mosquito.
        gamma (float): Tasa de recuperación en humanos.
        mu (float): Tasa de mortalidad de mosquitos.
        dias (int): Días de simulación.
    """
    # Humanos
    Sh = poblacion_h - infectados_h
    Ih = infectados_h
    Rh = 0
    
    # Mosquitos
    # Asumimos que la población de mosquitos es constante y proporcional a los humanos: V = m * H
    # V se divide en Susceptibles (Sv) e Infectados (Iv) (ignoramos expuestos en este modelo simple)
    Itv = infectados_v_iniciales
    Stv = (m * poblacion_h) - Itv

    # Estado inicial: [Sh, Ih, Rh, Sv, Iv]
    y0 = Sh, Ih, Rh, Stv, Itv
    t = np.linspace(0, dias, dias)

    def deriv(y, t, N_h, m, a, b, c, gamma, mu):
        Sh, Ih, Rh, Sv, Iv = y
        
        # Dinámica Humanos
        # dSh/dt = -a * b * (Iv/Nh) * Sh
        dShdt = -a * b * (Iv / N_h) * Sh
        dIhdt = a * b * (Iv / N_h) * Sh - gamma * Ih
        dRhdt = gamma * Ih
        
        # Dinámica Mosquitos (V = Sv + Iv)
        # dSv/dt = mu * V - a * c * (Ih/Nh) * Sv - mu * Sv
        # dIv/dt = a * c * (Ih/Nh) * Sv - mu * Iv
        # Nota: Asumimos nacimiento = muerte (mu*V) para mantener población constante
        V = Sv + Iv
        dSvdt = (mu * V) - a * c * (Ih / N_h) * Sv - mu * Sv
        dIvdt = a * c * (Ih / N_h) * Sv - mu * Iv
        
        return dShdt, dIhdt, dRhdt, dSvdt, dIvdt

    ret = odeint(deriv, y0, t, args=(poblacion_h, m, a, b, c, gamma, mu))
    Sh, Ih, Rh, Sv, Iv = ret.T

    df = pd.DataFrame({
        'Día': t,
        'Humanos Susceptibles': Sh,
        'Humanos Infectados': Ih,
        'Humanos Recuperados': Rh,
        'Mosquitos Susceptibles': Sv,
        'Mosquitos Infectados': Iv
    })
    return df
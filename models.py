
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
    return df
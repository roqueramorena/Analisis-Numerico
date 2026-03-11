import streamlit as st
import numpy as np
import utils as ec
import pandas as pd
import plotly.graph_objects as go

def biseccion(f,a,b,err):
    cuadro = {
    'a[i]':[],
    'b[i]':[],
    'x[i]':[],
    'f(x[i])':[],
    'Dx[i]':[]
    }
    fa = ec.evaluar_f(f,a)
    fb = ec.evaluar_f(f,b)

    # Casos base
    if fa * fb > 0:
        return None, []
    if a  > b:
        a, b = b, a
        fa, fb = fb, fa
    
    # Calculo de la raíz
    valor_anterior = a
    while True:
        x = (a+b)/2
        fx = ec.evaluar_f(f,x)

        cuadro['a[i]'].append(a)
        cuadro['b[i]'].append(b)
        cuadro['x[i]'].append(x)
        cuadro['f(x[i])'].append(fx)
        cuadro['Dx[i]'].append(x-a)

        if abs(fx) < err: 
            return x, cuadro
        if round(x,6) == round(valor_anterior,6):
            break
        
        valor_anterior = x
        
        # Opciones
        if fx * fa < 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx

    return x, cuadro

def mostrar_info():
    st.header('Metodo Bisección')
    
    formula = st.text_input('Escribe tu función $f(x)$:', value='x**2 + 11*x - 6')
    
    st.latex(ec.mostrar_formula(formula))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        inf = st.number_input('Ingresar intervalo inferior',value=-10.0,step=2.0)
    with col2:
        sup = st.number_input('Ingresar intervalo superior',value=10.0,step=2.0)
    with col3:
        err = st.number_input('Tolerancia de error $E = 10^{-n}$',value=2,min_value=1, max_value=10)
        err = 10**(-err)
    try:
        x = np.linspace(inf, sup, 300)
        y = ec.evaluar_f(formula,x)
        
        fig = go.Figure()
        p_x, datos = biseccion(formula,inf,sup,err)
        
        if p_x is not None:
            st.success(f'Raíz encontrada en: $$x ≈ {round(p_x,6)}$$')
            
            # calculamos límites para cuadrícula manual
            xmin, xmax = inf, sup
            ymin, ymax = float(np.min(y)), float(np.max(y))
            x_grids = np.linspace(xmin, xmax, 11)
            y_grids = np.linspace(ymin, ymax, 11)
            
            fig.update_layout(
                xaxis=dict(
                    title='Eje X',
                    showgrid=False,
                    zeroline=False,
                    layer='below traces',
                ),
                yaxis=dict(
                    title='Eje Y',
                    showgrid=False,
                    zeroline=False,
                    layer='below traces'
                ),
                plot_bgcolor='white',
                height=600
            )
            # líneas de cuadrícula como shapes en el nivel más bajo
            for xi in x_grids:
                fig.add_shape(dict(
                    type='line', x0=xi, x1=xi, y0=ymin, y1=ymax,
                    line=dict(color='lightgray', width=1, dash='dot'),
                    layer='below'
                ))
            for yi in y_grids:
                fig.add_shape(dict(
                    type='line', x0=xmin, x1=xmax, y0=yi, y1=yi,
                    line=dict(color='lightgray', width=1, dash='dot'),
                    layer='below'
                ))
            
            # La función se dibuja encima de ejes y cuadrícula
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='f(x)', line=dict(color='blue', width=2)))
            
            fig.add_vline(x=0, line_color="red", line_width=1, line_dash="solid", opacity=1, layer='below')
            
            fig.add_hline(y=0, line_color="red", line_width=1, line_dash="solid", opacity=1, layer='below')
            
            fig.add_trace(go.Scatter(
                x=[p_x], 
                y=[0],
                mode='markers',
                name='Raíz',
                marker=dict(
                    size=10,
                    color='green',
                    symbol='circle',
                    line=dict(color='black', width=1)
                )
            ))
            
            st.plotly_chart(fig, use_container_width=True)
            
            mostrar_datos = st.checkbox("Mostrar datos de iteraciones")
            if mostrar_datos:
                st.dataframe(pd.DataFrame(datos))
        else:
            st.error('No se ha encontrado la raíz.')

    except Exception as e:
        st.error(f'Error en la fórmula: {e}')
        st.info('Escribe la fórmula correctamente. Ejemplo: `x**2 + 11*x - 6`')

    st.divider()
    st.header('Código hecho en Python')
    st.code('''
def biseccion(f,a,b,err,max_i):
    fa = f(a)
    fb = f(b)
    # Casos base
    if f(a) * f(b) > 0:
        return None
    if a  > b:
        a, b = b, a
    # Calculo de la raíz
    for i in range(1, max_i+1):
        x = (a+b)/2
        fx = f(x)
        if abs(fx) < err or max_i<=0: 
            return x
        # Opciones
        if fx * fa < 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx
    return x''',
            "python")
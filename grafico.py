import plotly.graph_objects as go
import streamlit as st
import numpy as np
import utils as ec

@st.cache_data(show_spinner="Cargando trazado de la curva...")
def generar_base_fig(f, raiz, inf, sup):
    # Calculamos la distancia más larga desde la raíz a los extremos
    # para que al usarla en ambos lados, la raíz quede en el centro exacto.
    radio_vista = max(abs(raiz - inf), abs(raiz - sup))
    radio_con_margen = radio_vista * 1.1

    # Generamos los puntos basados en ese radio para que la curva no se corte
    x = np.linspace(raiz - radio_con_margen, raiz + radio_con_margen, 1000)
    y = ec.evaluar_f(f, x)
    
    fig = go.Figure()

    # Función f(x)
    fig.add_trace(go.Scatter(
        x=x, y=y, 
        mode='lines', 
        name='f(x)', 
        line=dict(color='#1E88E5', width=3)
    ))
    
    # Línea punteada para el límite inferior 'a'
    fig.add_vline(
        x=inf, 
        line_width=2, 
        line_dash="dash",
        line_color="rgba(30, 136, 229, 0.5)"
    )

    # Línea punteada para el límite superior 'b'
    fig.add_vline(
        x=sup, 
        line_width=2, 
        line_dash="dash", 
        line_color="rgba(30, 136, 229, 0.5)"
    )

    fig.update_layout(
        template='plotly_white',
        dragmode=False, 
        hovermode='x unified',
        margin=dict(l=40, r=40, t=100, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5),
        
        xaxis=dict(
            # Aplicamos el rango simétrico respecto a la raíz
            range=[raiz - radio_con_margen, raiz + radio_con_margen],
            # fixedrange=True,
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.2)',
            zeroline=True,
            zerolinecolor='rgba(176, 196, 222, 0.8)', 
            zerolinewidth=2.5
        ),
        yaxis=dict(
            range = [-max(abs(y))*1.2, max(abs(y))*1.2],
            # fixedrange=True,
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.2)',
            zeroline=True,
            zerolinecolor='rgba(176, 196, 222, 0.8)',
            zerolinewidth=2.5
        )
    )
    return fig

def dibujar(f, raiz, inf, sup, key=None, iteraciones=None):
    # Traemos la base del caché (instantáneo si no cambió f o el intervalo)
    fig = generar_base_fig(f, raiz, inf, sup)
    
    # Creamos una COPIA para no ensuciar el objeto original en el caché
    fig_final = go.Figure(fig)

    # Agregamos la "Telemetría" (las x rojas) solo si es necesario
    if iteraciones is not None and 'x[i]' in iteraciones:
        x_puntos = iteraciones['x[i]'][:-1]
        etiquetas = [f"x_{i}" for i in range(len(x_puntos))]
        fig_final.add_trace(go.Scatter(
            x=x_puntos,
            y=[0] * len(x_puntos),
            mode='markers',
            text=etiquetas,
            textposition="top center",
            name='Rastro x_i',
            marker=dict(symbol='x', size=10, color='#EF4444'),
            hovertemplate="Iteración %{text}: %{x:.6f}<extra></extra>"
        ))
    
    # Agregamos la Raíz final
    fig_final.add_trace(go.Scatter(
        x=[raiz], y=[0],
        mode='markers',
        name='Raíz',
        marker=dict(
            size=12, 
            color='#00E676', 
            line=dict(
                color='white', 
                width=2
                )
            )
    ))
    # Finalmente, mostramos el gráfico unificado
    st.plotly_chart(
        fig_final,
        use_container_width=True,
        key=key,
        config={
            'scrollZoom': False,
            'doubleClick': False, # <--- ESTO DESACTIVA EL RESET AL TOCAR
            'displayModeBar': True,
            'displaylogo': False,
            'showTips': False,
            'modeBarButtons': [[
                'zoomIn2d', 
                'zoomOut2d', 
                'resetViews'
                ]]
            }
        )
    
@st.cache_data(show_spinner="Cargando trazado de la curva...")
def generar_base_fig_abierto(f, raiz, x0, es_punto_fijo=False):
    # En métodos abiertos, la distancia clave es entre el punto inicial y la raíz
    radio_vista = abs(raiz - x0)
    
    # Control de seguridad: si x0 y la raíz están muy cerca, forzamos un radio mínimo
    if radio_vista < 0.5:
        radio_vista = 1.0
        
    radio_con_margen = radio_vista * 1.5

    # Generamos los puntos
    x = np.linspace(raiz - radio_con_margen, raiz + radio_con_margen, 1000)
    y = ec.evaluar_f(f, x)
    
    fig = go.Figure()

    # Trazamos la función principal (f(x) o g(x))
    nombre_curva = 'g(x)' if es_punto_fijo else 'f(x)'
    fig.add_trace(go.Scatter(
        x=x, y=y, 
        mode='lines', 
        name=nombre_curva, 
        line=dict(color='#1E88E5', width=3)
    ))

    # 
    # AGREGADO ESPECIAL PARA PUNTO FIJO: La recta y = x
    if es_punto_fijo:
        fig.add_trace(go.Scatter(
            x=x, y=x, # y = x
            mode='lines',
            name='y = x',
            line=dict(color='#FFCA28', width=2, dash='dash')
        ))

    # Línea punteada para marcar dónde arrancó el método (x0)
    fig.add_vline(
        x=x0, 
        line_width=2, 
        line_dash="dot",
        line_color="rgba(255, 111, 0, 0.6)", # Naranja para diferenciar de la raíz
        annotation_text="x₀", 
        annotation_position="top right"
    )

    fig.update_layout(
        template='plotly_white',
        dragmode=False, 
        hovermode='x unified',
        margin=dict(l=40, r=40, t=100, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5),
        
        xaxis=dict(
            range=[raiz - radio_con_margen, raiz + radio_con_margen],
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.2)',
            zeroline=True,
            zerolinecolor='rgba(176, 196, 222, 0.8)', 
            zerolinewidth=2.5
        ),
        yaxis=dict(
            range=[-max(abs(y))*1.2, max(abs(y))*1.2],
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.2)',
            zeroline=True,
            zerolinecolor='rgba(176, 196, 222, 0.8)',
            zerolinewidth=2.5
        )
    )
    return fig

def dibujar_abierto(f, raiz, x0, key=None, iteraciones=None, es_punto_fijo=False):
    # Usamos x0 en lugar de inf y sup
    fig = generar_base_fig_abierto(f, raiz, x0, es_punto_fijo)
    
    fig_final = go.Figure(fig)

    # Telemetría: Las iteraciones
    if iteraciones is not None and 'x[i]' in iteraciones:
        # Convertimos a float por si vienen como strings desde tu tabla
        x_puntos = [float(val) for val in iteraciones['x[i]'][:-1]] 
        
        # En punto fijo, los puntos van sobre la curva g(x), en Newton sobre el eje X
        y_puntos = ec.evaluar_f(f, np.array(x_puntos)) if es_punto_fijo else [0] * len(x_puntos)

        etiquetas = [f"x_{i}" for i in range(len(x_puntos))]
        fig_final.add_trace(go.Scatter(
            x=x_puntos,
            y=y_puntos,
            mode='markers',
            text=etiquetas,
            textposition="top center",
            name='Iteraciones x_i',
            marker=dict(symbol='x', size=10, color='#EF4444'),
            hovertemplate="Iteración %{text}: %{x:.6f}<extra></extra>"
        ))
    
    # Agregamos el punto final (La Raíz)
    # En Punto Fijo la intersección visual es en (raiz, raiz). En Newton es (raiz, 0).
    y_raiz = raiz if es_punto_fijo else 0
    fig_final.add_trace(go.Scatter(
        x=[raiz], y=[y_raiz],
        mode='markers',
        name='Punto de Convergencia',
        marker=dict(
            size=12, 
            color='#00E676', 
            line=dict(color='white', width=2)
        )
    ))

    st.plotly_chart(
        fig_final,
        use_container_width=True,
        key=key,
        config={
            'scrollZoom': False,
            'doubleClick': False, 
            'displayModeBar': True,
            'displaylogo': False,
            'showTips': False,
            'modeBarButtons': [['zoomIn2d', 'zoomOut2d', 'resetViews']]
        }
    )

@st.cache_data(show_spinner="Cargando trazado de la curva...")
def generar_base_fig_abierto(f, raiz, x0, es_punto_fijo=False):
    # En métodos abiertos, la distancia clave es entre el punto inicial y la raíz
    radio_vista = abs(raiz - x0)
    
    # Control de seguridad: si x0 y la raíz están muy cerca, forzamos un radio mínimo
    if radio_vista < 0.5:
        radio_vista = 1.0
        
    radio_con_margen = radio_vista * 1.5

    # Generamos los puntos
    x = np.linspace(raiz - radio_con_margen, raiz + radio_con_margen, 1000)
    y = ec.evaluar_f(f, x)
    
    fig = go.Figure()

    # Trazamos la función principal (f(x) o g(x))
    nombre_curva = 'g(x)' if es_punto_fijo else 'f(x)'
    fig.add_trace(go.Scatter(
        x=x, y=y, 
        mode='lines', 
        name=nombre_curva, 
        line=dict(color='#1E88E5', width=3)
    ))

    # 
    # AGREGADO ESPECIAL PARA PUNTO FIJO: La recta y = x
    if es_punto_fijo:
        fig.add_trace(go.Scatter(
            x=x, y=x, # y = x
            mode='lines',
            name='y = x',
            line=dict(color='#FFCA28', width=2, dash='dash')
        ))

    # Línea punteada para marcar dónde arrancó el método (x0)
    fig.add_vline(
        x=x0, 
        line_width=2, 
        line_dash="dot",
        line_color="rgba(255, 111, 0, 0.6)", # Naranja para diferenciar de la raíz
        annotation_text="x₀", 
        annotation_position="top right"
    )

    fig.update_layout(
        template='plotly_white',
        dragmode=False, 
        hovermode='x unified',
        margin=dict(l=40, r=40, t=100, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5),
        
        xaxis=dict(
            range=[raiz - radio_con_margen, raiz + radio_con_margen],
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.2)',
            zeroline=True,
            zerolinecolor='rgba(176, 196, 222, 0.8)', 
            zerolinewidth=2.5
        ),
        yaxis=dict(
            range=[-max(abs(y))*1.2, max(abs(y))*1.2],
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.2)',
            zeroline=True,
            zerolinecolor='rgba(176, 196, 222, 0.8)',
            zerolinewidth=2.5
        )
    )
    return fig

def dibujar_abierto(f, raiz, x0, key=None, iteraciones=None, es_punto_fijo=False):
    # Usamos x0 en lugar de inf y sup
    fig = generar_base_fig_abierto(f, raiz, x0, es_punto_fijo)
    
    fig_final = go.Figure(fig)

    # Telemetría: Las iteraciones
    if iteraciones is not None and 'x[i]' in iteraciones:
        # Convertimos a float por si vienen como strings desde tu tabla
        x_puntos = [float(val) for val in iteraciones['x[i]'][:-1]] 
        
        # En punto fijo, los puntos van sobre la curva g(x), en Newton sobre el eje X
        y_puntos = ec.evaluar_f(f, np.array(x_puntos)) if es_punto_fijo else [0] * len(x_puntos)

        etiquetas = [f"x_{i}" for i in range(len(x_puntos))]
        fig_final.add_trace(go.Scatter(
            x=x_puntos,
            y=y_puntos,
            mode='markers',
            text=etiquetas,
            textposition="top center",
            name='Iteraciones x_i',
            marker=dict(symbol='x', size=10, color='#EF4444'),
            hovertemplate="Iteración %{text}: %{x:.6f}<extra></extra>"
        ))
    
    # Agregamos el punto final (La Raíz)
    # En Punto Fijo la intersección visual es en (raiz, raiz). En Newton es (raiz, 0).
    y_raiz = raiz if es_punto_fijo else 0
    fig_final.add_trace(go.Scatter(
        x=[raiz], y=[y_raiz],
        mode='markers',
        name='Punto de Convergencia',
        marker=dict(
            size=12, 
            color='#00E676', 
            line=dict(color='white', width=2)
        )
    ))

    st.plotly_chart(
        fig_final,
        use_container_width=True,
        key=key,
        config={
            'scrollZoom': False,
            'doubleClick': False, 
            'displayModeBar': True,
            'displaylogo': False,
            'showTips': False,
            'modeBarButtons': [['zoomIn2d', 'zoomOut2d', 'resetViews']]
        }
    )
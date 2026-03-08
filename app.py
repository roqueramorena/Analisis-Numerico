import streamlit as st
import inicio, biseccion

st.set_page_config(
    page_title='App Análisis Numerico',
    page_icon='📊',
    )



def main():

    st.title('App Análisis Numérico 📊')

    choice = st.segmented_control(
        "Selecciona el módulo:",
        options=["Inicio", "Bisección"],
        default="Inicio"
    )
    
    mostrar_tp = st.checkbox("Mostrar Consigna del TP")
    if mostrar_tp:
        st.pdf("archivos/Consigna Tp 1 inf tele.pdf")
    
    # st.divider()

    if choice == 'Inicio':
        inicio.inicio()
    elif choice == 'Bisección':
        biseccion.mostrar_info()

if __name__ == '__main__':
    main()

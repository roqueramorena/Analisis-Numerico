# 📊 Software de Métodos Numéricos
Aplicación interactiva desarrollada en **Python + Streamlit** para la resolución de problemas de **Análisis Numérico**.

## 📦 Instalación
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/BautistaGenovese/Analisis-Numerico.git
   cd Analisis-Numerico
   ```
3. Crear entorno de ejecución

    Se recomienda ejecutar el proyecto dentro de un entorno virtual de Python para evitar conflictos entre dependencias. Crear y activar el entorno virtual:
      - En Windows:
   
         ```bash
         python -m venv env
         .\env\Scripts\activate
         ```
      
      - En Linux o Mac:
      
         ```bash
         python3 -m venv env
         source env/bin/activate
         ```

4. Instalar dependencias:

    ```bash
    pip install -r requirements.txt
    ```

5. Ejecutar la aplicación
    ```bash
    streamlit run app.py
    ```


## 📂 Estructura del Proyecto

```
Analisis-Numerico
│
├── archivos/
├── app.py            # Archivo principal de la aplicación
├── inicio.py         # Página de introducción
├── biseccion.py      # Implementación del método de bisección
├── ecuacion.py       # Evaluación y formateo de funciones
└── requirements.txt  # Dependencias del proyecto
```

## 🛠️ Tecnologías utilizadas
- Python
- Streamlit
- NumPy
- Matplotlib
- Pandas
- SymPy

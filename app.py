import gradio as gr
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Función para procesar el archivo cargado y realizar limpieza y normalización
def process_file(file, separator, method, normalize):
    codificaciones = ['utf-8', 'latin1', 'iso-8859-1']  # Lista de codificaciones comunes
    df = None
    for encoding in codificaciones:
        try:
            # Intentar leer el archivo con la codificación actual
            df = pd.read_csv(file.name, sep=separator, encoding=encoding, on_bad_lines='skip')
            break  # Salir del bucle si se carga con éxito
        except Exception as e:
            continue
    
    # Si no se pudo cargar el archivo
    if df is None:
        return f"No se pudo procesar el archivo con las codificaciones comunes.", None
    
    # Realizar limpieza de datos según el método seleccionado
    if method == "Poner ceros":
        df.fillna(0, inplace=True)
    elif method == "Borrar filas completas":
        df.dropna(inplace=True)
    elif method == "Promedio":
        df.fillna(df.mean(), inplace=True)
    elif method == "Máximo":
        df.fillna(df.max(), inplace=True)
    elif method == "Mínimo":
        df.fillna(df.min(), inplace=True)
    elif method == "Eliminar duplicados":
        df.drop_duplicates(inplace=True)
    elif method == "Eliminar valores atípicos":
        # Asumimos que valores atípicos son aquellos fuera de 3 desviaciones estándar
        for col in df.select_dtypes(include=['float64', 'int64']):
            df = df[(df[col] >= (df[col].mean() - 3 * df[col].std())) &
                    (df[col] <= (df[col].mean() + 3 * df[col].std()))]
    
    # Realizar normalización si está seleccionada
    if normalize == "Min-Max":
        scaler = MinMaxScaler()
        df[df.columns] = scaler.fit_transform(df)
    elif normalize == "Z-Score":
        scaler = StandardScaler()
        df[df.columns] = scaler.fit_transform(df)
    
    return f"Archivo procesado con éxito. Limpieza: {method}. Normalización: {normalize}.", df

# Interfaz en Gradio
with gr.Blocks() as demo:
    gr.Markdown("## Seleccionador de Separador, Limpieza y Normalización de Archivos CSV")
    
    # Seleccionador de separador
    separator = gr.Radio(
        choices=[",", ";"],
        label="Selecciona el separador",
        value=","
    )
    
    # Subidor de archivos
    file_input = gr.File(label="Sube tu archivo (CSV)")
    
    # Selección de método de limpieza
    method = gr.Radio(
        choices=[
            "Poner ceros",
            "Borrar filas completas",
            "Promedio",
            "Máximo",
            "Mínimo",
            "Eliminar duplicados",
            "Eliminar valores atípicos"
        ],
        label="Selecciona el método de limpieza",
        value="Poner ceros"
    )
    
    # Selección de normalización
    normalize = gr.Radio(
        choices=["Ninguna", "Min-Max", "Z-Score"],
        label="Selecciona el método de normalización",
        value="Ninguna"
    )
    
    # Salida de resultados
    output_text = gr.Textbox(label="Resultado")
    output_dataframe = gr.Dataframe(label="Datos procesados")
    
    # Botón para procesar
    process_button = gr.Button("Procesar archivo")
    
    # Conexión entre los componentes
    process_button.click(
        fn=process_file, 
        inputs=[file_input, separator, method, normalize], 
        outputs=[output_text, output_dataframe]
    )

# Ejecutar la aplicación
demo.launch()

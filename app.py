import gradio as gr
import pandas as pd

# Función para procesar el archivo cargado
def process_file(file, separator):
    try:
        # Cargar el archivo con el separador seleccionado
        df = pd.read_csv(file.name, sep=separator)
        return f"Archivo cargado con éxito. Aquí tienes las primeras filas:", df.head()
    except Exception as e:
        return f"Error al procesar el archivo: {str(e)}", None

# Interfaz en Gradio
with gr.Blocks() as demo:
    gr.Markdown("## Seleccionador de Separador y Cargador de Archivos")
    
    # Seleccionador de separador
    separator = gr.Dropdown(
        choices=[",", ";"],
        label="Selecciona el separador",
        value=","
    )
    
    # Subidor de archivos
    file_input = gr.File(label="Sube tu archivo (CSV)")
    
    # Salida de resultados
    output_text = gr.Textbox(label="Resultado")
    output_dataframe = gr.Dataframe(label="Datos procesados")
    
    # Botón para procesar
    process_button = gr.Button("Procesar archivo")
    
    # Conexión entre los componentes
    process_button.click(
        fn=process_file, 
        inputs=[file_input, separator], 
        outputs=[output_text, output_dataframe]
    )

# Ejecutar la aplicación
demo.launch()

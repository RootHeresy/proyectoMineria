import gradio as gr
import pandas as pd

# Función para procesar el archivo cargado
def process_file(file, separator):
    codificaciones = ['utf-8', 'latin1', 'iso-8859-1']  # Lista de codificaciones comunes
    for encoding in codificaciones:
        try:
            # Intentar leer el archivo con la codificación actual
            df = pd.read_csv(file.name, sep=separator, encoding=encoding, on_bad_lines='skip')
            return f"Archivo cargado con éxito usando codificación: {encoding}", df
        except Exception as e:
            # Intentar con la siguiente codificación si ocurre un error
            continue
    # Si todas las codificaciones fallan
    return f"No se pudo procesar el archivo con las codificaciones comunes.", None

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


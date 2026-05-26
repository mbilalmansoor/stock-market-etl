import gradio as gr
from datetime import datetime, timedelta
import pipeline as pipe

def ui_mediator(ticker, start_date, end_date):
    """Bridges the interactive web widgets with the backend orchestration workflow."""
    status_msg, df_result = pipe.execute_etl_flow(ticker, start_date, end_date)
    
    if df_result.is_empty():
        return status_msg, None
    
    # Convert Polars to standard Pandas right at the border for Gradio's graphing engine
    return status_msg, df_result.to_pandas()

# --- DESIGNING THE GRADIO INTERFACE ---
default_start = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")
default_end = datetime.today().strftime("%Y-%m-%d")

with gr.Blocks(theme=gr.themes.Default(primary_hue="emerald")) as demo:
    gr.Markdown("# 🧊 Decoupled Data Engineering App (Polars + DuckDB)")
    gr.Markdown("Fully modular architecture. Storage rules, ETL transformations, and presentation layouts are completely separated.")
    
    with gr.Row():
        with gr.Column(scale=1):
            ticker_field = gr.Textbox(label="Ticker Identifier", value="AAPL", placeholder="e.g. NVDA, GOOG")
            start_field = gr.Textbox(label="Start Window (YYYY-MM-DD)", value=default_start)
            end_field = gr.Textbox(label="End Window (YYYY-MM-DD)", value=default_end)
            submit_action = gr.Button("Trigger Pipeline Execution", variant="primary")
            
        with gr.Column(scale=2):
            log_field = gr.Textbox(label="Engine Process Log", interactive=False)
            chart_field = gr.LinePlot(
                x="date", 
                y="close_price", 
                title="Historical Timeline Evaluation", 
                tooltip=["date", "close_price"]
            )
            
    # Map execution click straight to our mediator bridge function
    submit_action.click(
        fn=ui_mediator, 
        inputs=[ticker_field, start_field, end_field], 
        outputs=[log_field, chart_field]
    )

if __name__ == "__main__":
    demo.launch()
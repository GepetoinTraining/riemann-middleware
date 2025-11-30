# app.py
import matplotlib
matplotlib.use('Agg') # <--- ADD THIS LINE TO PREVENT SERVER CRASHES
import matplotlib.pyplot as plt
import gradio as gr
import sys
import io
from src.WorldGen import WorldAlchemist, WorldConfig

# --- THE GRADIO WRAPPER ---
def generate_world_view(seed):
    # 1. Capture Stdout (to show the alchemy report)
    # We redirect the print statements to a string buffer
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    
    try:
        # 2. Run the Simulation
        # Ensure seed is an integer
        seed = int(seed)
        sim = WorldAlchemist(seed)
        
        # 3. Generate the terrain
        # Note: We need to modify render_slice slightly to return the figure 
        # instead of saving it, or we just read the saved file.
        # For this demo, we'll let it save to 'world_gen.png' and read it back.
        sim.render_slice()
        
        # 4. Get the text report
        output_text = new_stdout.getvalue()
        
        return "world_gen.png", output_text
        
    except Exception as e:
        return None, f"Error: {str(e)}"
    finally:
        # Reset stdout
        sys.stdout = old_stdout

# --- THE INTERFACE ---
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# 🌍 Riemann World Alchemist")
    gr.Markdown("> *\"The code executes the proof. The proof compiles reality.\"*")
    
    with gr.Row():
        with gr.Column():
            seed_input = gr.Number(label="Knowledge Seed (Integer)", value=29160000, precision=0)
            run_btn = gr.Button("Generate World", variant="primary")
            
            gr.Markdown("### Known Resonant Frequencies:")
            gr.Examples(
                examples=[
                    [29160000], # The Garden
                    [1080],     # Balanced Mud
                    [118098],   # The Logic Peaks
                    [58]        # The Cliffhanger
                ],
                inputs=seed_input
            )
            
        with gr.Column():
            output_img = gr.Image(label="Terrain Slice (Flux vs Form)")
            output_log = gr.Code(label="Alchemy Report", language="markdown")

    run_btn.click(fn=generate_world_view, inputs=seed_input, outputs=[output_img, output_log])

# Launch the substrate
demo.launch()
# main.py
from fastapi import FastAPI
import gradio as gr

# 1. Import your existing FastAPI app and Gradio interface
# Assuming app.api.api contains your FastAPI instance named 'app'
# Assuming app.gradio.app_ui contains your Gradio interface named 'demo'
from app.api.api import app as api_app
from app.gradio.app_ui import demo as gradio_ui

# 2. Create a new, master FastAPI application
master_app = FastAPI()

# 3. Mount your existing API to a specific path (e.g., /api)
master_app.mount("/api", api_app)

# 4. Mount the Gradio UI to the root path (/)
# This takes the master_app and the Gradio UI, and combines them.
app = gr.mount_gradio_app(master_app, gradio_ui, path="/")
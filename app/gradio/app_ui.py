import gradio as gr
import requests

FASTAPI_URL = "http://localhost:8000"


def upload_pdf(files):
    if not files:
        return "Please select one or more PDFs."

    multipart_files = []

    for file in files:
        multipart_files.append(
            (
                "files",  # Must match FastAPI parameter name
                (
                    file.name,
                    open(file.name, "rb"),
                    "application/pdf",
                ),
            )
        )

    try:
        response = requests.post(
            f"{FASTAPI_URL}/upload",
            files=multipart_files
        )
    finally:
        # Close all opened file handles
        for _, (_, f, _) in multipart_files:
            f.close()

    if response.ok:
        return "✅ PDF uploaded successfully."
    return f"❌ Upload failed: {response.text}"


def chat(message, history):
    if history is None:
        history = []
    payload = {
        "user_input": message
    }

    response = requests.post(
        f"{FASTAPI_URL}/chat",
        json=payload
    )

    if response.ok:
        answer = response.json().get("response", "No response.")
    else:
        answer = f"Error: {response.text}"

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": answer})

    return history, ""


with gr.Blocks(title="PDF Chat") as demo:
    with gr.Row():
        # Left panel
        with gr.Column(scale=1):
            pdf = gr.File(
                label="Upload PDF",
                file_types=[".pdf"],
                file_count = "multiple"
            )
            upload_btn = gr.Button("Upload")
            status = gr.Markdown()

        # Right panel
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="Chat",
                height=600,
                # type="messages"
            )

            msg = gr.Textbox(
                placeholder="Ask a question about the uploaded PDF...",
                show_label=False
            )

            send = gr.Button("Send")

    upload_btn.click(
        upload_pdf,
        inputs=pdf,
        outputs=status
    )

    send.click(
        chat,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    )

    msg.submit(
        chat,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    )

demo.launch()
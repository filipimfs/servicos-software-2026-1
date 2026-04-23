import gradio as gr
import requests


# =========================
# FUNÇÃO: TRANSCRIÇÃO + ANÁLISE
# =========================
def processa_audio(audio_path):
    if audio_path is None:
        return "Nenhum áudio recebido."

    with open(audio_path, "rb") as f:
        files = {"file": ("audio.wav", f, "audio/wav")}

        try:
            response = requests.post(
                "http://backend-json:8080/transcrever-e-analisar",
                files=files
            )

            if response.status_code == 200:
                data = response.json()

                return (
                    f"📝 Texto:\n{data['texto']}\n\n"
                    f"🧠 Sentimento: {data['sentimento']}\n"
                    f"📊 Score: {data['score']}"
                )
            else:
                return f"Erro no servidor: {response.status_code}"

        except Exception as e:
            return f"Erro de conexão com o backend: {str(e)}"


# =========================
# INTERFACE
# =========================
demo = gr.Interface(
    fn=processa_audio,
    inputs=gr.Audio(type="filepath", label="Grave ou envie um áudio"),
    outputs=gr.Textbox(label="Resultado da IA"),
    title="🎙️ Transcrição + Análise de Sentimento",
    description="Envie um áudio. O sistema transcreve usando IA (Whisper) e analisa automaticamente o sentimento.",
)


# =========================
# RUN
# =========================
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)

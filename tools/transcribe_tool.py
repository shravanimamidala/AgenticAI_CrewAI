from crewai_tools import BaseTool
from whisper import load_model

model = load_model("base")

class TranscribeTool(BaseTool):
    name = "Transcriber"
    description = "Transcribes mp3 audio file to text using Whisper"

    def _run(self, file_path: str) -> str:
        result = model.transcribe(file_path)
        return result["text"]

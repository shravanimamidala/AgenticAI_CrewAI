# tools/huggingface_tool.py
from crewai_tools import AIMindTool
from transformers import pipeline
from pydantic import Field

generator = pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-beta")

class HuggingFaceTextGenerationTool(AIMindTool):
    name: str = Field(default="HuggingFaceTextGenerationTool", description="Generates text using Hugging Face model")

    def _run(self, text_input: str):
        # Initialize the Hugging Face pipeline with your API key
        model = pipeline("text-generation", model="huggingface/HuggingFaceH4/zephyr-7b-beta", use_auth_token="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")
        result = model(text_input)
        return result



class HuggingFaceSummaryTool(BaseTool):
    name = "Summarizer"
    description = "Summarizes transcripts using HuggingFace LLM"

    def _run(self, input_text: str) -> str:
        return generator(input_text[:500], max_new_tokens=150, truncation=True)[0]['generated_text']
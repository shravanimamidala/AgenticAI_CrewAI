import requests
import os
import sys
import json
from transformers import pipeline
import whisper

print("MAIN.PY Python Executable:", sys.executable)

# Environment setup
os.environ["HUGGINGFACE_API_KEY"] = "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"
os.environ["CREWAI_LLM_MODEL"] = "HuggingFaceH4/zephyr-7b-beta"
os.environ.pop("OPENAI_API_KEY", None)

summarizer = pipeline("text-generation", model=os.environ["CREWAI_LLM_MODEL"])
transcriber = whisper.load_model("base")

# Create directories
os.makedirs("input", exist_ok=True)
os.makedirs("transcripts", exist_ok=True)

def process_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json().get("data", {}).get("results", [])
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return

    metadata = []

    for entry in results:
        for idx, rec in enumerate(entry.get("recording", [])):
            src = rec.get("src")
            if not src:
                continue

            file_id = f"{entry.get('id')}_{idx}"
            mp3_path = f"input/{file_id}.mp3"
            transcript_path = f"transcripts/{file_id}.txt"

            # Download if not already
            if not os.path.exists(mp3_path):
                try:
                    r = requests.get(src)
                    with open(mp3_path, "wb") as f:
                        f.write(r.content)
                    print(f"Downloaded: {mp3_path}")
                except Exception as e:
                    print(f"Failed to download {mp3_path}: {e}")
                    continue
            else:
                print(f"File exists, skipping download: {mp3_path}")

            # Transcription
            try:
                result = transcriber.transcribe(mp3_path)
                transcript = result["text"]
                with open(transcript_path, "w", encoding="utf-8") as f:
                    f.write(transcript)
            except Exception as e:
                print(f"Transcription failed for {mp3_path}: {e}")
                transcript = ""

            # Summarization
            try:
                summary = summarizer(transcript[:500], max_new_tokens=150, truncation=True)[0]['generated_text']
            except Exception as e:
                print(f"Summarization failed: {e}")
                summary = ""

            metadata.append({
                "id": entry.get("id"),
                "user": entry.get("user"),
                "user_id": entry.get("user_id"),
                "phone_number": entry.get("phone_number"),
                "call_length": entry.get("call_length"),
                "call_date": entry.get("call_date"),
                "recording_id": rec.get("recording_id"),
                "filename": rec.get("filename"),
                "call_type": entry.get("call_type"),
                "src": src,
                "input_file": mp3_path,
                "transcript_file": transcript_path,
                "transcript": transcript,
                "summary": summary
            })

    with open("metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print("Processing completed and metadata.json written.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_url(sys.argv[1])
    else:
        print("No URL provided.")

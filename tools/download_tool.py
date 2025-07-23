from crewai_tools import AIMindTool
import requests, os
from pydantic import Field


class DownloadRecordingTool(AIMindTool):
    name: str = Field(default="DownloadRecordingTool", description="Tool for downloading recordings")

    def _run(self, metadata: dict):
        os.makedirs("input", exist_ok=True)
        results = metadata.get("data", {}).get("results", [])
        for entry in results:
            for i, r in enumerate(entry.get("recording", [])):
                src_url = r.get("src")
                filename = f"{entry.get('id', 'unknown')}_{i}.mp3"
                try:
                    response = requests.get(src_url)
                    with open(f"input/{filename}", "wb") as f:
                        f.write(response.content)
                except Exception as e:
                    print(f"Failed to download {src_url}: {e}")
        return "Downloaded all available recordings to /input"

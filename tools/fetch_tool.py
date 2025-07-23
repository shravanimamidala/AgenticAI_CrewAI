from crewai_tools import AIMindTool
from typing import Annotated
from pydantic import Field
import requests

class FetchJSONTool(AIMindTool):
    name: str = Field(default="fetch_json_tool")
    description: str = Field(default="Fetches JSON metadata from a given URL")

    def _run(self, url: Annotated[str, "The API URL to fetch JSON from"]) -> dict:
        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

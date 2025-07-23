import sys
print("AGENT CONFIG PATH:", __file__)
from tools.fetch_tool import FetchJSONTool
from tools.download_tool import DownloadRecordingTool
from crewai.project import CrewBase, agent, task, crew
from crewai import Agent, Task, Crew

@CrewBase
class DashboardCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    tools_config = "config/tools.yaml"

    @agent
    def url_agent(self):
        return Agent(config=self.agents_config["url_agent"], tools=[FetchJSONTool()])
    
    @agent
    def metadata_agent(self):
        return Agent(config=self.agents_config["metadata_agent"])
    
    @agent
    def dashboard_agent(self):
        return Agent(config=self.agents_config["dashboard_agent"])
    
    @agent
    def downloader_agent(self):
        return Agent(config=self.agents_config["downloader_agent"], tools=[DownloadRecordingTool()])
    

    @task
    def parse_url_task(self) -> Task:
        return Task(config=self.tasks_config["parse_url_task"], agent=self.url_agent())

    @task
    def process_metadata_task(self) -> Task:
        return Task(config=self.tasks_config["process_metadata_task"], agent=self.metadata_agent())

    @task
    def download_recordings_task(self) -> Task:
        return Task(config=self.tasks_config["download_recordings_task"], agent=self.downloader_agent())

    @task
    def display_task(self) -> Task:
        return Task(config=self.tasks_config["display_task"], agent=self.dashboard_agent())

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.url_agent(),
                self.metadata_agent(),
                self.dashboard_agent(),
                self.downloader_agent(),
            ],
            tasks=[
                self.parse_url_task(),
                self.process_metadata_task(),
                self.download_recordings_task(),
                self.display_task(),
            ],
            verbose=True
        )

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ExaSearchTool

from daily_ai_news_email_digest.tools.gmail_tool import GmailSendTool


@CrewBase
class DailyAiNewsEmailDigestCrew:
    """DailyAiNewsEmailDigest crew"""

    @agent
    def ai_news_hunter(self) -> Agent:
        return Agent(
            config=self.agents_config["ai_news_hunter"],  # type: ignore[index]
            tools=[ExaSearchTool()],
            inject_date=True,
            allow_delegation=False,
            max_iter=30,
            llm=LLM(model="gemini/gemini-2.5-flash"),
        )

    @agent
    def ai_news_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["ai_news_analyst"],  # type: ignore[index]
            tools=[],
            inject_date=True,
            allow_delegation=False,
            max_iter=10,
            llm=LLM(model="gemini/gemini-2.5-flash"),
        )

    @agent
    def newsletter_copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config["newsletter_copywriter"],  # type: ignore[index]
            tools=[],
            inject_date=True,
            allow_delegation=False,
            max_iter=10,
            llm=LLM(model="gemini/gemini-2.5-flash"),
        )

    @agent
    def html_email_designer(self) -> Agent:
        return Agent(
            config=self.agents_config["html_email_designer"],  # type: ignore[index]
            tools=[],
            inject_date=True,
            allow_delegation=False,
            max_iter=10,
            llm=LLM(model="gemini/gemini-2.5-flash"),
        )

    @agent
    def email_delivery_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["email_delivery_agent"],  # type: ignore[index]
            tools=[GmailSendTool()],
            inject_date=True,
            allow_delegation=False,
            max_iter=5,
            llm=LLM(model="gemini/gemini-2.5-flash"),
        )

    @task
    def hunt_ai_news(self) -> Task:
        return Task(
            config=self.tasks_config["hunt_ai_news"],  # type: ignore[index]
            markdown=False,
        )

    @task
    def curate_ai_news(self) -> Task:
        return Task(
            config=self.tasks_config["curate_ai_news"],  # type: ignore[index]
            markdown=False,
        )

    @task
    def write_newsletter_copy(self) -> Task:
        return Task(
            config=self.tasks_config["write_newsletter_copy"],  # type: ignore[index]
            markdown=False,
        )

    @task
    def design_html_email(self) -> Task:
        return Task(
            config=self.tasks_config["design_html_email"],  # type: ignore[index]
            markdown=False,
        )

    @task
    def send_email_newsletter(self) -> Task:
        return Task(
            config=self.tasks_config["send_email_newsletter"],  # type: ignore[index]
            markdown=False,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the DailyAiNewsEmailDigest crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ExaSearchTool

from daily_ai_news_email_digest.tools.gmail_tool import GmailSendTool

GEMINI_FLASH = LLM(model="gemini/gemini-2.5-flash")


@CrewBase
class DailyAiNewsEmailDigestCrew:

    @agent
    def ai_news_hunter(self) -> Agent:
        return Agent(
            config=self.agents_config["ai_news_hunter"],  # type: ignore[index]
            tools=[ExaSearchTool()],
            inject_date=True,
            allow_delegation=False,
            max_iter=30,
            llm=GEMINI_FLASH,
        )

    @agent
    def ai_news_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["ai_news_analyst"],  # type: ignore[index]
            inject_date=True,
            allow_delegation=False,
            max_iter=10,
            llm=GEMINI_FLASH,
        )

    @agent
    def newsletter_copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config["newsletter_copywriter"],  # type: ignore[index]
            inject_date=True,
            allow_delegation=False,
            max_iter=10,
            llm=GEMINI_FLASH,
        )

    @agent
    def html_email_designer(self) -> Agent:
        return Agent(
            config=self.agents_config["html_email_designer"],  # type: ignore[index]
            inject_date=True,
            allow_delegation=False,
            max_iter=10,
            llm=GEMINI_FLASH,
        )

    @agent
    def email_delivery_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["email_delivery_agent"],  # type: ignore[index]
            tools=[GmailSendTool()],
            inject_date=True,
            allow_delegation=False,
            max_iter=5,
            llm=GEMINI_FLASH,
        )

    @task
    def hunt_ai_news(self) -> Task:
        return Task(config=self.tasks_config["hunt_ai_news"])  # type: ignore[index]

    @task
    def curate_ai_news(self) -> Task:
        return Task(config=self.tasks_config["curate_ai_news"])  # type: ignore[index]

    @task
    def write_newsletter_copy(self) -> Task:
        return Task(config=self.tasks_config["write_newsletter_copy"])  # type: ignore[index]

    @task
    def design_html_email(self) -> Task:
        return Task(config=self.tasks_config["design_html_email"])  # type: ignore[index]

    @task
    def send_email_newsletter(self) -> Task:
        return Task(config=self.tasks_config["send_email_newsletter"])  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

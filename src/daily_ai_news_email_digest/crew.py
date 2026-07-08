import time
import litellm
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

litellm.cache = None

# CrewAI 1.15.0 injects Anthropic cache_breakpoint into messages regardless of provider.
# Groq rejects it. Strip it before every call. Also retry on rate limits.
_orig_completion = litellm.completion


def _completion_stripped(**kwargs):
    for msg in kwargs.get("messages", []):
        if isinstance(msg, dict):
            msg.pop("cache_breakpoint", None)
    for attempt in range(5):
        try:
            return _orig_completion(**kwargs)
        except litellm.RateLimitError:
            if attempt < 4:
                time.sleep(65)
            else:
                raise


litellm.completion = _completion_stripped

GROQ_LLM = LLM(
    model="groq/llama-3.3-70b-versatile",
    max_tokens=3000,
)


@CrewBase
class DailyAiNewsEmailDigestCrew:

    @agent
    def ai_news_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["ai_news_analyst"],
            inject_date=True,
            allow_delegation=False,
            max_iter=5,
            llm=GROQ_LLM,
        )

    @agent
    def newsletter_copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config["newsletter_copywriter"],
            inject_date=True,
            allow_delegation=False,
            max_iter=5,
            llm=GROQ_LLM,
        )

    @agent
    def html_email_designer(self) -> Agent:
        return Agent(
            config=self.agents_config["html_email_designer"],
            inject_date=True,
            allow_delegation=False,
            max_iter=5,
            llm=GROQ_LLM,
        )

    @task
    def curate_ai_news(self) -> Task:
        return Task(config=self.tasks_config["curate_ai_news"])

    @task
    def write_newsletter_copy(self) -> Task:
        return Task(config=self.tasks_config["write_newsletter_copy"])

    @task
    def design_html_email(self) -> Task:
        return Task(config=self.tasks_config["design_html_email"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

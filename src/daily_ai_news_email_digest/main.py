#!/usr/bin/env python
import sys
from daily_ai_news_email_digest.crew import DailyAiNewsEmailDigestCrew


def run():
    DailyAiNewsEmailDigestCrew().crew().kickoff(inputs={})


def train():
    DailyAiNewsEmailDigestCrew().crew().train(
        n_iterations=int(sys.argv[1]),
        filename=sys.argv[2],
        inputs={},
    )


def replay():
    DailyAiNewsEmailDigestCrew().crew().replay(task_id=sys.argv[1])


def test():
    DailyAiNewsEmailDigestCrew().crew().test(
        n_iterations=int(sys.argv[1]),
        eval_llm=sys.argv[2],
        inputs={},
    )

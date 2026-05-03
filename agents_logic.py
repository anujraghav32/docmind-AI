import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()

LLM_MODEL = "groq/llama-3.3-70b-versatile"

writer = Agent(
    role='Writer',
    goal='Summarize PDF',
    backstory='Expert writer',
    llm=LLM_MODEL,
    verbose=True,
    allow_delegation=False
)

critic = Agent(
    role='Critic',
    goal='Review summary',
    backstory='Expert critic',
    llm=LLM_MODEL,
    verbose=True,
    allow_delegation=False
)

def run_agentic_process(pdf_text):
    t1 = Task(
        description=f"Summarize: {pdf_text[:5000]}",
        expected_output="Summary",
        agent=writer
    )
    t2 = Task(
        description="Review this summary and improve it",
        expected_output="Final Summary",
        agent=critic
    )

    crew = Crew(
        agents=[writer, critic],
        tasks=[t1, t2],
        process=Process.sequential,
        verbose=True
    )
    return crew.kickoff()

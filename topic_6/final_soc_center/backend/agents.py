from typing import NotRequired
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph_supervisor import create_supervisor
from langchain_openai import ChatOpenAI
from langgraph.managed import RemainingSteps
from langgraph.graph import MessagesState

from backend.tools import get_virustotal_safe_tools
from backend.schemas import IncidentConclusion

load_dotenv()

class SupervisorState(MessagesState):
    remaining_steps: RemainingSteps
    structured_response: NotRequired[IncidentConclusion]

power_llm = ChatOpenAI(model="gpt-6.1-sol", use_responses_api=True, reasoning_effort="low")
llm = ChatOpenAI(model="gpt-5.5")

async def create_agents():
    """Creates the agents involved in the SOC. One supervisor, two researchers and one analyzer"""

    safe_tools = await get_virustotal_safe_tools()

    research_agent = create_agent(
        name="researcher",
        model=llm,
        tools=safe_tools,
        system_prompt="""You are a SOC threat-intelligence researcher specialized on using VirusTotal for investigating and that
            excels on using your reasoning and also critical thinking. 
            malicious threats. You will be given pieces of information from incidents and your goal is to make a
            research to see if they belong to a malicious actor or not, because there might be some false positives.
            Once you finish, you have to present the raw data of your findings""",
        debug=True
    )

    analyst_agent = create_agent(
        name="analyst",
        model=llm,
        tools=safe_tools,
        system_prompt="""
            You are a SOC threat-intelligence analyst specialized on analyzing threat research data and generate conclusions.
            You will be given some information about an incident and the results of a research done. Your goal is to generate
            evidence to declare if that incident is a false positive or not, based on the data provided.
        """,
        debug=True
    )


    supervisor_agent = create_supervisor(
        model=power_llm,
        agents=[
            research_agent,
            analyst_agent
        ],
        prompt="""
            You are SOC manager that handles a team of specialist to diagnose and solve threat incidents. You will be
            given incidents and your goal is deleate tasks to your team and return the conclusion.

            Your team of specialists are:
            1. researcher: makes a deep research on the internet for the given incident data
            2. analyst: given results of an investigation, analyzes all the information and generates conclusions
        """,
        response_format=IncidentConclusion,
        state_schema=SupervisorState,
        debug=True
        
    )

    return supervisor_agent.compile()
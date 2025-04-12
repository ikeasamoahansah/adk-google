import os
import asyncio
import datetime

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.agents import Agent
from google.genai import types

openai_key = os.environ['OPENAI_API_KEY']
google_key = os.environ['GOOGLE_API_KEY']
model_list = ['gemini-2.0-flash-exp', 'openai/gpt-4o']


def get_and_parse_document(input: int, text: str) -> str:
    """Parses a financial document sent by the user.

    Args:
        input (file): The financial document sent by the user
        text (str): Additional instructions given by the user
    
    Returns:
        str: A structured data in the csv file format with comma separated values
            Includes the total column with for the amount of values in the '$' currency
    """
    print("Document!")


financial_agent = Agent(
    name="finai_agent_v1",
    model=model_list[0],
    description="Provides financial reports",
    instruction="You are a helpful financial assistant. Your primary goal is to provide financial reports. "
                "When the user sends a document or a text, "
                "you MUST use the `get_and_parse_document` tool to generate the file in a csv format. "
                "Only use the tool when the user's prompt is related to finance. ",
    tools=[get_and_parse_document],
)

session_service = InMemorySessionService()

APP_NAME = "finai_app"
USER_ID = "user_1"
SESSION_ID = "session_001"

# specific session where conversation wiil happen
session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)

# Runner orchestrates the agent execution loop
runner = Runner(
    agent=financial_agent,
    app_name=APP_NAME,
    session_service=session_service
)

# Agent Interaction with async calls and executions
async def call_agent_async(query: str):
    """Sends a query to the agent and print the final response."""

    content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response." #Default

    # run_async executes the agent logic and yields Events
    # iterate through events to find final answer
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
        # is_final_response() marks the concluding message for the turn
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate: # Handle errors
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message'}"
            # Add more checks if needed
            break

    print(f"<<< Agent Response: {final_response_text}")


async def run_conversation() -> asyncio.coroutines:
    await call_agent_async("Make a price list for apples, bananas and oranges")
    await call_agent_async("Make a price list for some household utensils")

"""
Simple script to run the agent-as-tool example.

Usage:
    python main.py

Or use ADK CLI:
    adk run adk-agent-as-tool-example
    adk web adk-agent-as-tool-example
"""

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent


def main():
    session_service = InMemorySessionService()

    session = session_service.create_session(
        app_name=root_agent.name,
        user_id="user-1",
        session_id="session-1"
    )

    runner = Runner(
        agent=root_agent,
        app_name=root_agent.name,
        session_service=session_service
    )

    user_message = "What is 125 * 37 + 89?"

    print(f"User: {user_message}\n")

    content = types.Content(
        role="user",
        parts=[types.Part(text=user_message)]
    )

    for event in runner.run(
        user_id=session.user_id,
        session_id=session.session_id,
        new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print(f"Assistant: {event.content.parts[0].text}")


if __name__ == "__main__":
    main()

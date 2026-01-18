import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from agent import create_workflow_agent

load_dotenv()


def main():
    # Create the workflow agent
    app = create_workflow_agent()

    # Run the workflow
    result = app.invoke({
        "messages": [HumanMessage(content="Process this data and validate the result")],
        "current_step": "initialize",
        "retries": 0,
        "data": None,
        "error": None
    })

    # Print the result
    print("=== Workflow Result ===")
    print(f"Final step: {result.get('current_step')}")
    for message in result["messages"]:
        print(f"{message.type}: {message.content}")


if __name__ == "__main__":
    main()

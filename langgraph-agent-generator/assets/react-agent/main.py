import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from agent import create_agent

load_dotenv()


def main():
    # Create the agent
    app = create_agent()

    # Run the agent
    result = app.invoke({
        "messages": [HumanMessage(content="What is 2 + 2?")]
    })

    # Print the result
    for message in result["messages"]:
        print(f"{message.type}: {message.content}")


if __name__ == "__main__":
    main()

import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from agent import create_multi_agent

load_dotenv()


def main():
    # Create the multi-agent system
    app = create_multi_agent()

    # Run the agent
    result = app.invoke({
        "messages": [HumanMessage(content="Write a blog post about AI agents")],
        "next_agent": "supervisor",
        "task_complete": False
    })

    # Print the result
    print("=== Multi-Agent Result ===")
    for message in result["messages"]:
        print(f"\n{message.type}: {message.content[:200]}...")


if __name__ == "__main__":
    main()

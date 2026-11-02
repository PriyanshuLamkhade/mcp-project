
import asyncio
from uuid import uuid4

from langchain.messages import HumanMessage
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain.mcp import MCPAdapter
from langgraph.checkpoint.memory import InMemorySaver


async def main():

    async with MCPAdapter("http://127.0.0.1:8000/mcp") as adapter:

        # Discover MCP tools
        tools = await adapter.list_tools()

        print("\nAvailable MCP Tools:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")

        # Initialize Ollama
        model = ChatOllama(
            model="qwen3.5:9b",
            temperature=0,
            thinking=False,
        )

        # Create an actual agent
        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt="""
            You are a helpful task management assistant.

            Instructions:
            - Use the available tools whenever the user's request
              requires an action supported by those tools.
            - Do not invent tool results.
            - If the user's request is unclear, ask one short
              clarification question.
            - Keep responses short and direct.
            - Do not claim an action was completed unless the
              corresponding tool call succeeded.
            """,
            checkpointer=InMemorySaver(),
        )

        config = {
            "configurable": {
                "thread_id": str(uuid4())
            }
        }

        while True:

            human_question = input("\nHuman: ")

            if human_question.lower() == "q":
                break

            result = await agent.ainvoke(
                {
                    "messages": [
                        HumanMessage(content=human_question)
                    ]
                },
                config=config
            )

            print("\nAI:", result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())

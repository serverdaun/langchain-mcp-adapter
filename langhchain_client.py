import asyncio
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": [
                    "/Users/noty/Desktop/ML/projects/mcp-adapters/servers/math_server.py"
                ],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    )

    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    result = await agent.ainvoke(
        {
            # "messages": [HumanMessage(content="What is 2 + 2?")]
            "messages": [HumanMessage(content="What is the weather in Tokyo?")]
        }
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

stdio_server_params = StdioServerParameters(
    command="python",
    args=["/Users/noty/Desktop/ML/projects/mcp-adapters/servers/math_server.py"],
)

async def main():
    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("session initialized")

            tools = await load_mcp_tools(session)

            agent = create_react_agent(llm, tools)
            result = await agent.ainvoke({
                "messages": [HumanMessage(content="What is 2 + 2 * 3?")]
            })
            print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())

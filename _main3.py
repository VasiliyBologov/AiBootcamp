import asyncio
import os
import shutil
import subprocess
import time
from typing import Any

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerSse, MCPServerStdio
from agents.model_settings import ModelSettings

from get_env import load_env, get_env_value

load_env()
key = get_env_value('OPENAI_API_KEY')
print(key)
print(get_env_value('MDB_MCP_CONNECTION_STRING'))
os.environ["OPENAI_API_KEY"] = key


async def run_agent(mcp_server: MCPServer):
    agent = Agent(
        name="Assistant",
        instructions=(
            "You are a helpful and knowledgeable assistant."
            "Use available MCP tools to answer user questions accurately and efficiently."
            "For questions about delivery, returns, warranties, discounts, partnerships, or the franchise — use the support/FAQ tools."
            "Do not guess. Always rely on tools to ensure correctness and completeness of your response."
        ),
        model="gpt-4.1-nano",
        mcp_servers=[mcp_server]
    )

    # Use the `add` tool to add two numbers
    message = "расскажи мне про скидки"
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)



async def main():
    mcp1 = MCPServerStdio(
            name="support-bot",
            params={
                "command": "uv",
                "args": [
                    "run",
                    "--with",
                    "mcp[cli]",
                    "mcp",
                    "run",
                    "mcps/mcp-rules/main.py"
                ]
            }
        )
    # ) as server:
    #     trace_id = gen_trace_id()
    #     with trace(workflow_name="MCP ES", trace_id=trace_id):
    #         # print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
    #         pass

    await mcp1.connect()
    trace_id = gen_trace_id()
    with trace(workflow_name="Assistant", trace_id=trace_id):
        await run_agent(mcp1)
    mcp1.exit_stack.pop_all()



if __name__ == "__main__":
    import datetime
    start = datetime.datetime.now()
    try:
        asyncio.run(main())
    finally:
        end = datetime.datetime.now()
        r =end - start
        print(f"Time taken: {r.seconds} seconds")
        print("Done")
        # raise Exception("Exit")








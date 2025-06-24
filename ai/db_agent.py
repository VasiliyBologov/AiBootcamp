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
os.environ["OPENAI_API_KEY"] = key

class DBAgent:
    def __init__(self):
        self.agent = None
        self.mcp = None

    async def run(self):
        self.mcp = MCPServerStdio(
            name="mongodb-mcp",
            params={
                "command": "docker",
                "args": [
                    "run",
                    "--rm",
                    "-i",
                    "-e",
                    f"MDB_MCP_CONNECTION_STRING={get_env_value('MDB_MCP_CONNECTION_STRING')}",
                    "mongodb_mcp_server:latest"
                ]
            }
        )

        await self.mcp.connect()

        self.agent = Agent(
            name="Assistant",
            instructions="Use the tools to find information in mongodb",
            model="gpt-4.1-nano",
            mcp_servers=[self.mcp],
            # model_settings=ModelSettings(tool_choice="required"),
        )

    async def ask(self, message) -> str:
        trace_id = gen_trace_id()
        r = "No result"
        with trace(workflow_name="MCP ES", trace_id=trace_id):
            result = await Runner.run(starting_agent=self.agent, input=message)
            print(result.final_output)
            r = result.final_output
        return r

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mcp.exit_stack.pop_all()

# async def run_agent(mcp_server: MCPServer):
#
#
#     # Use the `add` tool to add two numbers
#     message = "расскажи мне о 'Parfum Code Collection Women W01' из giter_products.product"
#     print(f"Running: {message}")
#
#     print()



# async def main():
#
#     # ) as server:
#     #     trace_id = gen_trace_id()
#     #     with trace(workflow_name="MCP ES", trace_id=trace_id):
#     #         # print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
#     #         pass
#
#
#
#     with trace(workflow_name="MCP ES", trace_id=trace_id):
#         await run_agent(mcp1)




# if __name__ == "__main__":
#     import datetime
#     start = datetime.datetime.now()
#     try:
#         asyncio.run(main())
#     finally:
#         end = datetime.datetime.now()
#         r =end - start
#         print(f"Time taken: {r.seconds} seconds")
#         print("Done")
#         # raise Exception("Exit")


import logging
import os

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerSse, MCPServerStdio

from get_env import load_env, get_env_value


load_env()
key = get_env_value('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = key

logging.basicConfig(level=logging.INFO)

class ConsultantAgent:
    def __init__(self):
        self.agent = None
        self.mcp = None

    async def run(self):
        logging.info(f"Run Agent: {self.__class__.__name__}")
        self.mcp = MCPServerStdio(
            name="Giter Fragrance API MCP Server",
            params={
                "command": "uv",
                "args": [
                    "run",
                    "--with",
                    "mcp[cli]",
                    "mcp",
                    "run",
                    "mcps/mcp-products/main.py"
                ]
            }
        )

        await self.mcp.connect()

        self.agent = Agent(
            name="Assistant",
            instructions="You are an online perfume consultant. Use the tools to find information about product from api. Use link mask 'https://main.giter.world/catalog/fragrance/product/{productId} for presentations info. '  ",
            model="gpt-4.1-nano",
            mcp_servers=[self.mcp],
            # model_settings=ModelSettings(tool_choice="required"),
        )

        logging.info(f"Agent: {self.__class__.__name__} - is ready.")

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

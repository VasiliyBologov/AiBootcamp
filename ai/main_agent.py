import os

from agents import Agent, Runner, gen_trace_id, trace, handoff
from agents.mcp import MCPServer, MCPServerSse, MCPServerStdio
from agents.model_settings import ModelSettings

from get_env import load_env, get_env_value

if not os.environ.get("OPENAI_API_KEY", None):
    load_env()
    key = get_env_value('OPENAI_API_KEY')
    os.environ["OPENAI_API_KEY"] = key

class MainAgent:
    def __init__(self):
        self.agent = None

    async def run(self, api_agent, support_agent):
        self.agent = Agent(
            name="Assistant",
            instructions = ("You are an online assistant. To answer questions use Handoffs consultant and assistant agents. consultant - can tell about products and goods, select the right one by description. Assistant can tell about discounts, affiliate program or support questions"),
            model="gpt-4.1-mini",
            handoffs=[api_agent, support_agent],
        )

    async def ask(self, message) -> str:
        trace_id = gen_trace_id()
        r = "No result"
        with trace(workflow_name="Online assistant", trace_id=trace_id):
            result = await Runner.run(starting_agent=self.agent, input=message, max_turns=10)
            print(result.final_output)
            r = result.final_output
        return r

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mcp.exit_stack.pop_all()
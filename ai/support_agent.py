import os

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerSse, MCPServerStdio
from agents.model_settings import ModelSettings

from get_env import load_env, get_env_value

if not os.environ.get("OPENAI_API_KEY", None):
    load_env()
    key = get_env_value('OPENAI_API_KEY')
    os.environ["OPENAI_API_KEY"] = key

class SupportAgent:
    def __init__(self):
        self.agent = None
        self.mcp = None

    async def run(self):
        self.mcp = MCPServerStdio(
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
        await self.mcp.connect()
        self.agent = Agent(
            name="SupportAssistant",
            instructions = (
                "You are a helpful and knowledgeable assistant."
                "Use available MCP tools to answer user questions accurately and efficiently."
                "For questions about delivery, returns, warranties, discounts, partnerships, or the franchise — use the support/FAQ tools."
                "Do not guess. Always rely on tools to ensure correctness and completeness of your response."
                ),
            model="gpt-4.1-nano",
            mcp_servers=[self.mcp]
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
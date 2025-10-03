import os

import duckdb
import logfire
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai import RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

# setup logging
load_dotenv()
logfire.configure(token=os.getenv("LOGFIRE_TOKEN"))
logfire.instrument_pydantic_ai()

#setup the LLM
BASE_URL="http://127.0.0.1:1234/v1"
LM_STUDIO_MODEL="openai/gpt-oss-20b"

# define the output model
class Capital(BaseModel):
    name: str = Field(..., description="The name of the capital")
    country: str = Field(..., description="The country of the capital, as it was asked by the user.")
    num_inhabitants: float = Field(..., description="The number of inhabitants of the capital")
    size_of_capital: float = Field(..., description="The size of the capital in square kilometers")


def get_capital_agent() -> Agent:
    model = OpenAIChatModel(LM_STUDIO_MODEL, provider=OpenAIProvider(BASE_URL))
    agent = Agent(model, output_type=Capital)

    # Be aware that this is a decorator that uses the real instance, so agent, not Agent
    # define this outside and get dependencies in a different way
    @agent.tool
    def query_numbers(ctx: RunContext[None], capital_name: str) -> {}:
        """query the number of inhabitants and size for a capital"""
        row = duckdb.sql(
            f"Select inhabitants, size from 'data/capitals_wikipedia.csv' where name = '{capital_name}'").fetchone()
        return {'inhabitants': row[0], 'size': row[1]}

    return agent


if __name__ == "__main__":
    agent = get_capital_agent()
    result = agent.run_sync("What is the size of the capital of Germany?")
    print(result.output)


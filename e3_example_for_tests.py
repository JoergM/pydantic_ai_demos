import os
from dataclasses import dataclass

import duckdb
import logfire
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider


# define the output model
class Capital(BaseModel):
    name: str = Field(..., description="The name of the capital")
    country: str = Field(..., description="The country of the capital, as it was asked by the user.")
    num_inhabitants: float = Field(..., description="The number of inhabitants of the capital")
    size_of_capital: float = Field(..., description="The size of the capital in square kilometers")

# the Type defining runtime dependencies for the agent
@dataclass
class CapitalDeps:
    db: duckdb.DuckDBPyConnection

def init_db():
    """initialize the database based on the csv file"""
    db = duckdb.connect(':memory:')
    db.execute('CREATE TABLE capitals_wikipedia '
               'AS SELECT * from "data/capitals_wikipedia.csv"')
    return db

#this time not decorator
def query_numbers(ctx: RunContext[CapitalDeps], capital_name: str) -> {}:
    """query the number of inhabitants and size for a capital"""
    row = ctx.deps.db.execute(f"SELECT inhabitants, size "
                              f"FROM capitals_wikipedia "
                              f"WHERE name = '{capital_name}'").fetchone()
    if row:
        return {'inhabitants': row[0], 'size': row[1]}
    else:
        return {}

def get_capital_agent() -> Agent:
    BASE_URL = "http://127.0.0.1:1234/v1"
    LM_STUDIO_MODEL = "openai/gpt-oss-20b"
    model = OpenAIChatModel(LM_STUDIO_MODEL, provider=OpenAIProvider(BASE_URL))
    agent = Agent(model,
                  output_type=Capital,
                  deps_type=CapitalDeps, # Here we define the type of deps used in all tool calls
                  tools=[query_numbers]) # This is an alternative way to provide tools
    return agent

if __name__ == "__main__":
    agent = get_capital_agent()
    deps = CapitalDeps(db=init_db()) #We need to initialize the runtime dependencies
    result = agent.run_sync("What is the size of the capital of Germany?", deps=deps)
    print(result.output)


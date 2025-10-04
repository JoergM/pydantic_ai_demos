import duckdb
import pytest
from pydantic_ai import models
from pydantic_ai.messages import ModelMessage, ModelResponse, ToolCallPart
from pydantic_ai.models.function import FunctionModel, AgentInfo

from e3_example_for_tests import get_capital_agent, CapitalDeps


@pytest.fixture
def fake_db():
    """This creates a database only for the test"""
    db = duckdb.connect(':memory:')
    db.execute('CREATE TABLE capitals_wikipedia (name VARCHAR, inhabitants NUMERIC, size NUMERIC)')
    db.execute("INSERT INTO capitals_wikipedia VALUES ('Berlin', 4000000, 900)")  # lets round berlin numbers up
    return CapitalDeps(db=db)

#This example should demonstrate the way a function model works. It would probably not make a good test.
def simulate_model(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
    #messages contains the full history so we can analyse it in detail
    if len(messages) == 1:  # We only count the messages here. In reality it would probably be parsed
        return ModelResponse(parts=[
            ToolCallPart( #Could als be other types like TextPart of course
                tool_name="query_numbers",
                args={'capital_name': 'Berlin'}
            )])
    if len(messages) > 1:
        tool_return = messages[-1].parts[0]
        assert tool_return.part_kind == "tool-return"
        return ModelResponse(parts=[
            ToolCallPart( # this is the final answer because structured data is expected
                tool_name="final_result",
                args={
                    'country': 'Germany',
                    'name': 'Berlin',
                    'num_inhabitants': tool_return.content['inhabitants'],
                    'size_of_capital': tool_return.content['size']
                }
            )
        ])
    else:
        raise ValueError("No messages received")


# Demonstrate the use of TestModel
@pytest.mark.asyncio
async def test_alternative_model(fake_db: CapitalDeps):
    models.ALLOW_MODEL_REQUESTS = False  # block any requests to real models form happening
    agent = get_capital_agent()
    with agent.override(model=FunctionModel(simulate_model)):
        result = await agent.run("What is the size of the capital of Germany?", deps=fake_db)
        print(result.output)

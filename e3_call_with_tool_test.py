import pytest
from pydantic_ai.models.test import TestModel

from e3_call_with_tool import get_capital_agent

@pytest.mark.asyncio
async def test_call_with_tool():
    agent = get_capital_agent()
    agent.override(model=TestModel())
    result = await agent.run("What is the size of the capital of Germany?")
    print(result.output)


# Demonstrate the use of test_model
# To replace the model we need to be able to get the agent


# demonstrate the use of dependencies

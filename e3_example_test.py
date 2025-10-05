import duckdb
import pytest
from pydantic_ai import models
from pydantic_ai.models.test import TestModel

from e3_example_for_tests import get_capital_agent, CapitalDeps

@pytest.fixture
def fake_db():
    """This creates a database only for the test"""
    db = duckdb.connect(':memory:')
    db.execute('CREATE TABLE capitals_wikipedia (name VARCHAR, inhabitants NUMERIC, size NUMERIC)')
    db.execute("INSERT INTO capitals_wikipedia VALUES ('Berlin', 4000000, 900)") #lets round berlin numbers up
    return CapitalDeps(db=db)

@pytest.mark.asyncio
async def test_database_values_returned(fake_db: CapitalDeps):
    """This is some kind of integration test to demonstrate that the tool is called and the
    database values are returned.
    It demonstrates the use of Dependencies to guarantee results.
    """
    agent = get_capital_agent()
    result = await agent.run("What is the size of the capital of Germany?", deps=fake_db)
    print(f"\n")
    print(f"Test 1 result: {result.output}")
    assert result.output.country == "Germany"
    assert result.output.name == "Berlin"
    assert result.output.num_inhabitants == 4000000
    assert result.output.size_of_capital == 900

# Demonstrate the use of TestModel
@pytest.mark.asyncio
async def test_alternative_model(fake_db: CapitalDeps):
    models.ALLOW_MODEL_REQUESTS = False #block any requests to real models form happening
    agent = get_capital_agent()
    with agent.override(model=TestModel()):
        result = await agent.run("What is the size of the capital of Germany?", deps=fake_db)
        print(f"\n")
        print(f"Test 2 result: {result.output}")




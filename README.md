# Struktur vor Zufall: Verlässlichere KI Systeme bauen mit Pydantic AI

This repository contains example code for the presentation "Struktur vor Zufall: Verlässlichere KI Systeme bauen mit Pydantic AI" (Structure over Randomness: Building More Reliable AI Systems with Pydantic AI).

The examples demonstrate how to use Pydantic AI to create structured, testable, and reliable AI systems by leveraging type safety, validation, and evaluation frameworks.

## Examples Overview

The repository contains four examples that should be explored in sequence:

### e1_structure.ipynb - Structured Outputs
Demonstrates the basics of Pydantic AI:
- Basic LLM calls returning strings
- Structured outputs using Pydantic models
- Integration with Logfire for observability
- Using validators to ensure output quality with automatic retries

### e2_tool call.ipynb - Tool Integration
Shows how to extend LLM capabilities with tools:
- Giving the LLM access to external data sources (DuckDB)
- Tool calling to retrieve accurate information
- Reducing hallucinations through grounded data access
- Working with runtime dependencies

### e3_example_for_tests.py - Testing Strategies
Demonstrates how to write testable AI agents:
- Structuring agents for unit testing
- Using dependency injection for test isolation
- Example test cases (e3_example_test.py, e3_example_function_model_test.py)

### e4_using_evals.ipynb - Evaluation Framework
Shows how to evaluate non-deterministic AI outputs:
- Creating evaluation datasets
- Deterministic evaluators for measurable criteria
- Using LLM-as-a-Judge for semantic evaluation
- Comparing different models and prompts

## Setup Instructions

### Prerequisites

1. **Python 3.12 or higher** - Check your version with `python --version`
2. **uv** - Modern Python package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))
3. **LM Studio** - Local LLM runtime (see setup below)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pydantic-demos
```

2. Install dependencies using uv:
```bash
uv sync
```

This will:
- Create a virtual environment
- Install all required dependencies from `pyproject.toml`
- Lock versions in `uv.lock`

3. Set up environment variables:
```bash
cp .env_example .env
```

Edit `.env` and add your Logfire token (see Environment Variables section below).

### LM Studio Setup

The examples use a local LLM via LM Studio for privacy and cost-efficiency.

1. **Download LM Studio**:
   - Visit [https://lmstudio.ai/](https://lmstudio.ai/)
   - Download the version for your operating system
   - Install the application

2. **Download a Model**:
   - Open LM Studio
   - Go to the "Discover" tab
   - Search for "gpt-oss-20b" or another compatible model
   - Click download and wait for completion

3. **Start the Local Server**:
   - Go to the "Local Server" tab in LM Studio
   - Select the downloaded model (e.g., `openai/gpt-oss-20b`)
   - Click "Start Server"
   - Ensure the server is running on `http://127.0.0.1:1234/v1` (default)

**Alternative Models**: You can use any OpenAI-compatible model. Update the `LM_STUDIO_MODEL` variable in the examples to match your chosen model.

**Using Cloud Providers**: To use OpenAI, Anthropic, or other cloud providers instead, modify the agent initialization:
```python
# Instead of local model
agent = Agent('openai:gpt-4', output_type=YourModel)
```

## Environment Variables

The project uses environment variables for configuration. Copy `.env_example` to `.env` and configure:

- **LOGFIRE_TOKEN**: Your Logfire API token for observability and logging
  - Sign up at [https://logfire.pydantic.dev/](https://logfire.pydantic.dev/)
  - Free tier available with generous limits
  - Get your token from the Logfire dashboard
  - Optional: Remove logfire configuration from examples if you don't want to use it

## Running the Examples

### Jupyter Notebooks (e1, e2, e4)

1. Start Jupyter:
```bash
uv run jupyter notebook
```

2. Open the notebooks in sequence:
   - `e1_structure.ipynb`
   - `e2_tool call.ipynb`
   - `e4_using_evals.ipynb`

3. Run cells sequentially to see the examples in action

### Python Tests (e3)

Run the test examples:
```bash
uv run pytest e3_example_test.py -v -s
uv run pytest e3_example_function_model_test.py -v -s
```

Or run the main script:
```bash
uv run python e3_example_for_tests.py
```

## Project Structure

```
pydantic-demos/
├── e1_structure.ipynb              # Example 1: Structured outputs
├── e2_tool call.ipynb              # Example 2: Tool integration
├── e3_example_for_tests.py         # Example 3: Main code
├── e3_example_test.py              # Example 3: Basic tests
├── e3_example_function_model_test.py  # Example 3: Function model tests
├── e4_using_evals.ipynb            # Example 4: Evaluation framework
├── data/
│   ├── capitals_wikipedia.csv      # Test data for examples
│   └── capitals_dataset.yaml       # Evaluation dataset
├── pyproject.toml                  # Project dependencies
├── uv.lock                         # Locked dependency versions
├── .env                            # Environment variables (not in git)
├── .env_example                    # Environment template
├── README.md                       # This file
└── LICENSE.md                      # License information
```

## Key Dependencies

- **pydantic-ai**: Framework for building structured AI agents
- **pydantic-evals**: Evaluation framework for AI systems
- **duckdb**: In-memory database for examples
- **logfire**: Observability platform by Pydantic
- **pytest**: Testing framework

## Troubleshooting

### LM Studio Connection Issues
- Ensure LM Studio server is running on port 1234
- Check the server URL in examples matches your LM Studio configuration
- Verify the model name matches the loaded model in LM Studio

### Logfire Errors
- Ensure your LOGFIRE_TOKEN is set in `.env`
- Check token validity at [https://logfire.pydantic.dev/](https://logfire.pydantic.dev/)
- You can comment out logfire configuration if not needed

### Package Installation Issues
- Ensure uv is up to date: `uv self update`
- Try removing `.venv` and running `uv sync` again
- Check Python version: `python --version` (needs 3.12+)

## License

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/). See [LICENSE.md](LICENSE.md) for details.

## Author

Jörg Müller
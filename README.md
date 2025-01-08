# EvaEngine SDK
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/evaengine.svg)](https://badge.fury.io/py/evaengine)

A Python SDK for evaluating and generating tweet responses using EvaEngine's AI-powered API. This SDK provides easy access to tweet evaluation metrics, virtual scoring, and AI-generated response suggestions.

## Features

- 🔍 Comprehensive tweet evaluation
- 🎯 Virtual scoring system
- 💡 AI-powered response suggestions
- 📊 Detailed scoring metrics
- ⚡ Async/await support
- 🔒 Type-safe with Pydantic models

## Installation

```bash
pip install evaengine
```

## Quick Start

```python
import asyncio
from evaengine import EvaEngine

async def main():
    # Initialize with your API key
    engine = EvaEngine(api_key="your-api-key")
    
    async with engine:
        # Evaluate a tweet response
        result = await engine.evaluate_tweet(
            input_tweet="What's your favorite programming language?",
            output_tweet="Python is amazing for its simplicity and readability!"
        )
        
        print(f"Final Score: {result.final_score}")
        print(f"Truth Score: {result.truth.score}")
        print(f"Truth Rationale: {result.truth.rationale}")

if __name__ == "__main__":
    asyncio.run(main())
```

## API Reference

### Initialize Client

```python
from evaengine import EvaEngine

# Using API key directly
engine = EvaEngine(api_key="your-api-key")

# Using environment variable
from dotenv import load_dotenv
import os

load_dotenv()
engine = EvaEngine(api_key=os.getenv("X_API_KEY"))
```

### Evaluate Tweet

Evaluate a tweet response against an original tweet:

```python
result = await engine.evaluate_tweet(
    input_tweet="What's your favorite programming language?",
    output_tweet="Python is amazing for its simplicity and readability!"
)

print(f"Final Score: {result.final_score}")
print(f"Truth Score: {result.truth.score}")
print(f"Accuracy Score: {result.accuracy.score}")
print(f"Creativity Score: {result.creativity.score}")
print(f"Engagement Score: {result.engagement.score}")
```

### Get Historical Scores

Retrieve historical evaluation scores:

```python
scores = await engine.get_scores()
```

### Get AI-Suggested Response

Generate an AI-powered response suggestion:

```python
suggestion = await engine.get_suggested_tweet(
    input_tweet="Just launched my new AI project!"
)
print(f"Suggested Response: {suggestion}")
```


## Environment Variables

You can set your API key using an environment variable:

```bash
# .env file
X_API_KEY=your-api-key
```


## Requirements

- Python 3.7+
- aiohttp>=3.8.0
- pydantic>=2.0.0
- python-dotenv>=0.19.0

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Documentation

For more detailed documentation, visit [https://api.evaengine.ai/docs](https://api.evaengine.ai/docs)

## License

MIT License - see LICENSE file for details.
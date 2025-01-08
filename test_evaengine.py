import asyncio
from evaengine import EvaEngine
from dotenv import load_dotenv
import os
load_dotenv()

async def test_evaluation():
    engine = EvaEngine(api_key=os.getenv("X_API_KEY"))
    
    async with engine:
        # Test tweet evaluation
        result = await engine.evaluate_tweet(
            input_tweet="What's your favorite programming language?",
            output_tweet="Python is amazing for its simplicity and readability!"
        )
        print("Evaluation Result:", result)
        
        # Test virtual evaluation
        virtual_result = await engine.evaluate_tweet_virtual(
            input_tweet="What's your favorite programming language?",
            output_tweet="Python is amazing for its simplicity and readability!"
        )
        print("Virtual Evaluation:", virtual_result)
        
        # Test scores
        scores = await engine.get_scores()
        print("Available Scores:", scores)
        
        # Test suggestion
        suggestion = await engine.get_suggested_tweet(
            input_tweet="Just launched my new AI project!"
        )
        print("Suggested Tweet:", suggestion)

if __name__ == "__main__":
    asyncio.run(test_evaluation()) 
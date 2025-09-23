from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession
from openai.types.responses import ResponseTextDeltaEvent
import asyncio

load_dotenv(override=True)

session = SQLiteSession("travel_conversation_123")

agent = Agent(
    name="Assistant",
    instructions="Reply very concisely.",
)

async def main():
    user_query = "Give a very precise city and country of birth of cricketer Sachin Tendulkar"
    result = await Runner.run(agent, user_query, session = session)
    print(result.final_output)

    print("---------------------------------------------------------------------------------------------------------")

    user_query = "Give names of the best 5 sight seeing places of that city. Start by giving a headline"
    result = Runner.run_streamed(agent, user_query, session = session,)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

    print("\n--------------------------------------------------------------------------------------------------------")

    user_query = "Give a 2N/3D budget travel itinerary including flight, hotel, transport and restaurant covering those places." \
    "Make sure you have covered all the sight seeing places in your itinerary"
    result = Runner.run_streamed(agent, user_query, session = session,)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

# Run the async function using asyncio
if __name__ == "__main__":
    asyncio.run(main())


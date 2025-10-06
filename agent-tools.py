from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
import os

load_dotenv(override=True)

instructions_agent01 = "You are an intelligent agent who gets the precise city and country of birth of any cricket player. " \
                       "Just give the name of the city and country only and nothing else."

instructions_agent02 = "You are a specialized agent in giving expert budget friendly travel itinerary for a given place or country. " \
                       "Only recommend places, hotels, transport and restaurants suggesations which will in making the plan better; "                        

agent01 = Agent( 
    name="CricketerPlaceOfBirth", 
    instructions = instructions_agent01,
    model="gpt-4o-mini"
 )

tool01 = agent01.as_tool("CricketerPlaceOfBirth_Tool", "Gets cricket's city and country name")

agent02 = Agent( 
    name="TravelItineraryAdvisor", 
    instructions = instructions_agent02,
    model="gpt-4o-mini"
 )

tool02 = agent02.as_tool("TravelItineraryAdvisor_Tool", "Budget friendly travel advisor for a given place or country") 

@function_tool
async def fetch_weather(location:str) -> str:
    """Fetch the weather for a given location.
    Args:
        location: The location to fetch the weather for.
    """
    # In real life, we'd fetch the weather from a weather API
    return "thunderstorm" #try with storm, cloudy, rainy, cyclone

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "You are an intelligent assistant and the first point of contact for customer query. "
        "You assesss all the tools and give the answer. Use the tools multiple time to get the final answer"\
        "If you do not find any matching agent then simply ask the user to " \
        "reframe the question"
    ),
    tools=[tool01,tool02, fetch_weather]
)

async def main():
    user_query = "Give me the city of birth of cricketer Sachin Tendulkar and suggest me a 1N/2D travel itinerary for " \
                 "that city if the weather is fit for travel"
    result = Runner.run_streamed(triage_agent, user_query)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())

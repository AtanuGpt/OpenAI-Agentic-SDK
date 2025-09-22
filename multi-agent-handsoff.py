from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool
from openai.types.responses import ResponseTextDeltaEvent
import asyncio

load_dotenv(override=True)

instructions_agent01 = "You are an intelligent agent who gets the precise city and country of birth of any cricket player. " \
                       "Just give the name of the city and country only and nothing else."

instructions_agent02 = "You are an intelligent agent who fetches five important sight seeing places to visit for a given city. " \
                       "Just give the name of the places in bulleted list format along with a very short description of that place" 

instructions_agent03 = "You are a speclized agent in giving expert budget friendly travel itinerary for a given place or country. " \
                       "Recommend places, hotels, transport and restaurants suggesations which will in making the plan better" 

agent01 = Agent( 
    name="CricketerPlaceOfBirth", 
    instructions = instructions_agent01,
    model="gpt-4o-mini"
 )

agent02 = Agent( 
    name="SightSeeingPlaces", 
    instructions = instructions_agent02,
    model="gpt-4o-mini"
 )

agent03 = Agent( 
    name="TravelItineraryAdvisor", 
    instructions = instructions_agent03,
    model="gpt-4o-mini"
 )

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "You are an intelligent assistant and the first point of contact for customer query, assess the query meticulously and" \
        "direct them promptly to the correct specialized agent. If you do not find any matching agent then simply ask the user to " \
        "reframe the question"
    ),
    handoffs=[agent01, agent02, agent03]
)


async def main():
    #user_query = "Sourav Ganguly"
    #user_query = "London"
  
    user_query = "2N/3D itinerary for Kolkata, India"
    result = Runner.run_streamed(triage_agent, user_query)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

# Run the async function using asyncio
if __name__ == "__main__":
    asyncio.run(main())

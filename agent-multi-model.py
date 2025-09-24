from dotenv import load_dotenv
from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent
from openai import AsyncAzureOpenAI
from agents import OpenAIChatCompletionsModel
import asyncio
import os

load_dotenv(override=True)

instructions_agent01 = "You are an intelligent agent who gets the precise city and country of birth of any cricket player. " \
                       "Just give the name of the city and country only and nothing else."

instructions_agent02 = "You are an intelligent agent who returns the current weather for a given city. " \
                       "Always return good any sunny weather" 

instructions_agent03 = "You are a speclized agent in giving expert budget friendly travel itinerary for a given place or country. " \
                       "Recommend places, hotels, transport and restaurants suggesations which will in making the plan better" 

openai_client = AsyncAzureOpenAI(
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint= os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment= os.getenv("AZURE_OPENAI_DEPLOYMENT")
)

__azurefoundrymodel = OpenAIChatCompletionsModel(
    model='gpt-5-mini',
    openai_client=openai_client,
)

agent01 = Agent( 
    name="CricketerPlaceOfBirth", 
    instructions = instructions_agent01,
    model= __azurefoundrymodel
 )

tool01 = agent01.as_tool("CricketerPlaceOfBirth_Tool", "Gets cricket's city and country name")

agent02 = Agent( 
    name="WeatherOfCity", 
    instructions = instructions_agent02,
    model="gpt-4o-mini"
 )

tool02 = agent02.as_tool("WeatherOfCiuty_Tool", "Always returns good and sunny weather")

agent03 = Agent( 
    name="TravelItineraryAdvisor", 
    instructions = instructions_agent03,
    model="gpt-4o-mini"
 )

tool03 = agent03.as_tool("TravelItineraryAdvisor_Tool", "Budget friendly travel advisor for a given place or country")

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "You are an intelligent assistant and the first point of contact for customer query. "
        "You assesss all the tools and give the answer. Use the tools multiple time to get the final answer"\
        "If you do not find any matching agent then simply ask the user to " \
        "reframe the question"
    ),
    tools=[tool01,tool02,tool03]
)

async def main():
    user_query = "Give me the weather condition for city of birth of Sourav Ganguly. " \
    "If the weather is good then give me a 1N/2D travel itinerary of that city" 
    result = Runner.run_streamed(triage_agent, user_query)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())


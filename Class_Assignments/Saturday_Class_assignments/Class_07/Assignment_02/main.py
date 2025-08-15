# hotel_assistant.py
from typing import Any
from agents import Agent, Runner, RunContextWrapper, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, input_guardrail,GuardrailFunctionOutput, InputGuardrailTripwireTriggered
from decouple import config
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
set_tracing_disabled(True)

key = config("GEMINI_API_KEY")
base_url = config("GEMINI_BASE_URL")

gemini_client = AsyncOpenAI(api_key=key, base_url=base_url)

gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-pro",
    openai_client=gemini_client,
)


# Example hotel data
hotels_data = {
    "Grand Palace": {
        "location": "Karachi, Pakistan",
        "rooms": "Luxury suites, standard rooms",
        "price": "Rs. 15,000 per night",
        "contact": "+92-300-1234567"
    },
    "Sea View Hotel": {
        "location": "Karachi Beachfront",
        "rooms": "Sea view deluxe rooms",
        "price": "Rs. 10,000 per night",
        "contact": "+92-300-7654321"
    }
}

dynamic_instructions = (
    "You are a helpful hotel booking assistant. "
    "Ask the user which hotel they want details for. "
    "If the user asks for details about a Grand Palace or Sea View they are asking about Grand Palace hotel or Sea View hotel, "
    "Available hotels: " + ", ".join(hotels_data.keys())
)


class MyDataType(BaseModel):
    is_query_about_Grand_Palace_Hotel_or_Sea_View_Hotel: bool
    reason: str

guardrial_agent = Agent(
    name="GurdrialAgent",
    instructions="Check queries for Grand Palace or Sea View",
    model=gemini_model,
    output_type=MyDataType

)

@input_guardrail
async def guardrial_input_function(ctx:RunContextWrapper, agent, input):
  
    result = await Runner.run(guardrial_agent, input=input, context= ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_query_about_Grand_Palace_Hotel_or_Sea_View_Hotel
    )

agent = Agent(
    name="HotelAssistant",
    instructions=dynamic_instructions,
    model=gemini_model,
	input_guardrails=[guardrial_input_function]
)

try:

    res = Runner.run_sync(
        starting_agent=agent, 
        input="what is the weather?",
    )

    print(res.final_output)
except InputGuardrailTripwireTriggered as e:
    print(e)
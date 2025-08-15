import os
from agents import Runner
from agents.exceptions import InputGuardrailTripwireTriggered
from Agents.agents import bot_agent, human_agent
import chainlit as cl
from agents import set_tracing_disabled

# Disable LiteralAI/OpenAI instrumentation to avoid NotGiven/tool serialization issues
os.environ["LITERALAI_DISABLED"] = "1"
# cl.instrument_openai()  # disable for non-OpenAI base_url to avoid serialization conflicts
set_tracing_disabled(True)  # disable internal tracing


# Optional terminal testing (uncomment to run outside Chainlit)
if __name__ == "__main__":
    test_inputs = [
        "What is the status of my order 123?",
        "You guys are stupid",
        "I want a refund!",
        "What colors does the widget come in?"
    ]
    for text in test_inputs:
        try:
            res = Runner.run_sync(bot_agent, text, context={"user_input": text})
            print("Bot:", res.final_output)
        except InputGuardrailTripwireTriggered:
            res = Runner.run_sync(human_agent, text, context={"user_input": text})
            print("Human:", res.final_output)

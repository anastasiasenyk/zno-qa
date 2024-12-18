import gradio as gr
import random
from time import sleep
from loguru import logger

import sys
sys.path.append("../../")

from zno_agent import ZNOAgent
agent = ZNOAgent()

def random_response(message, history):
    return random.choice(["Yes", "No"])

def zno_agent_response(prompt, history):
    instruction = "Ти агент, який вміє розв'язувати тести з української мови, української літератури та історії України. Якщо вхідне питання з української мови, не переформульовуй його.\n\n"
    sleep(random.uniform(2, 3))
    try:
        response = agent.ask_question(instruction + prompt)
    except Exception as e:
        logger.error(f"Error: {e}")
        # if error status 429 sleep for 1 min and try again
        if "429" in str(e):
            sleep(60)
            response = agent.ask_question(instruction + prompt)
        else:
            return
    return response["answer"]


if __name__ == "__main__":
    demo = gr.ChatInterface(zno_agent_response, type="messages", autofocus=False)
    demo.launch()

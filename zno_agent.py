from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

from loguru import logger
import os
from dotenv import load_dotenv


# TODO: experiment with ukr/eng prompts and docstrings
@tool
def search_wikipedia(query: str) -> str:
    """AIMessage tool to search wikipedia"""
    # TODO: Add implementation
    return f"Searching wikipedia for {query}"

@tool
def grammar_check(text: str) -> str:
    """AIMessage tool to check grammar and spelling in text"""
    # TODO: Add implementation
    return f"Checking grammar for {text}"

@tool
def search_vocab_dict(word: str) -> str:
    """AIMessage tool to search vocabulary for a word"""
    # TODO: Add implementation
    return f"Searching vocabulary for {word}"

@tool
def extract_from_history_docs(query: str) -> str:
    """AIMessage tool to perform RAG based search on history documents"""
    # TODO: Add implementation
    return f"Extracting information from history documents for {query}"

@tool
def extract_from_ukr_lit_docs(query: str) -> str:
    """AIMessage tool to perform RAG based search on Ukrainian literature documents"""
    # TODO: Add implementation
    return f"Extracting information from Ukrainian literature documents for {query}"

def setup_qa_app():
    history_tools = [extract_from_history_docs]
    ukr_lit_tools = [extract_from_ukr_lit_docs]
    ukr_lang_tools = [grammar_check, search_vocab_dict]
    wikipedia_tools = [search_wikipedia]

    model_with_tools = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0).bind_tools(history_tools + ukr_lit_tools + ukr_lang_tools + wikipedia_tools)

    def should_continue(state: MessagesState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            if last_message.tool_calls[0]["name"] in [f.name for f in history_tools]:
                return "history_tools"
            if last_message.tool_calls[0]["name"] in [f.name for f in ukr_lit_tools]:
                return "ukr_lit_tools"
            if last_message.tool_calls[0]["name"] in [f.name for f in ukr_lang_tools]:
                return "ukr_lang_tools"
            if last_message.tool_calls[0]["name"] in [f.name for f in wikipedia_tools]:
                return "wikipedia_tools"
        return END

    def call_model(state: MessagesState):
        messages = state["messages"]
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}
    
    history_tools_node = ToolNode(history_tools)
    ukr_lit_tools_node = ToolNode(ukr_lit_tools)
    ukr_lang_tools_node = ToolNode(ukr_lang_tools)
    wikipedia_tools_node = ToolNode(wikipedia_tools)

    workflow = StateGraph(MessagesState)

    workflow.add_node("agent", call_model)
    workflow.add_node("history_tools", history_tools_node)
    workflow.add_node("ukr_lit_tools", ukr_lit_tools_node)
    workflow.add_node("ukr_lang_tools", ukr_lang_tools_node)
    workflow.add_node("wikipedia_tools", wikipedia_tools_node)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue, ["history_tools", "ukr_lit_tools", "ukr_lang_tools", "wikipedia_tools", END])
    workflow.add_edge("history_tools", "agent")
    workflow.add_edge("ukr_lit_tools", "agent")
    workflow.add_edge("ukr_lang_tools", "agent")
    workflow.add_edge("wikipedia_tools", "agent")

    app = workflow.compile()
    return app


def setup_output_parser():
    json_schema = {
        "title": "answer",
        "description": "Format the answer to a question with answer options: А, Б, В, Г, Д",
        "type": "object",
        "properties": {
            "answer": {
                "type": "string",
                "description": "One letter answer: А, Б, В, Г, Д",
            },
            "explanation": {
                "type": "string",
                "description": "Explanation of the answer",
            },
        },
        "required": ["answer", "explanation"],
    }
    llm = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0)
    structured_llm = llm.with_structured_output(json_schema)
    return structured_llm


class ZNOAgent:
    def __init__(self):
        load_dotenv('env_variables.env', override=True)
        self.app = setup_qa_app()
        self.parser = setup_output_parser()

    def ask_question(self, question: str):
        result = self.app.invoke({"messages": [HumanMessage(question)]})
        parsed_result = self.parser.invoke(result["messages"][-1].content)
        return parsed_result

    def render_app_graph(self):
        try:
            image_data = self.app.get_graph().draw_mermaid_png()
            with open("output_graph.png", "wb") as file:
                file.write(image_data)
        except Exception:
            # This requires some extra dependencies and is optional
            pass


if __name__ == "__main__":
    agent = ZNOAgent()
    agent.render_app_graph()

    question = "Історія України:" + "Реалізація імперської стратегії Росії в Першій світовій війні щодо \"…злиття землі Ярослава Осмомисла, князів Данила і Романа з Імперією в політичному, соціальному та національному відношеннях…\" стала можливою завдяки\n\nА. Карпатській операції.\nБ. Горліцькому прориву.\nВ. Брусиловському прориву.\nГ. Галицькій битві."
    print(agent.ask_question(question))
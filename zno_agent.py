from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

from retriever_pipeline.retrieve import preprocess_documents, retrieve_relevant_chunks
from tool_spelling.spelling_correction_tool import spelling_check_and_correct
from tool_wikipedia.wikipedia_tool import get_wikipedia_context
from tool_vocab.vocabulary_scrapper_tool import get_vocabulary_info_tool

from loguru import logger
import os
from dotenv import load_dotenv


# TODO: experiment with ukr/eng prompts and docstrings
@tool
def search_wikipedia(query: str) -> str:
    """Інструмент для пошуку інформації в Вікіпедії"""
    result = get_wikipedia_context(query)
    return result

@tool
def spelling_check(text: str) -> str:
    """Інструмент для перевірки правильності написання слів"""
    result = spelling_check_and_correct(text)
    return result

@tool
def search_vocab_dict(word: str) -> str:
    """Інструмент для пошуку слова в словнику, який містить інформацію про наголос, частину мови(іменник, прикметник, дієслово, ...) і форми слова(відмінки, роди, число, ...)"""
    result = get_vocabulary_info_tool(word)
    return result

@tool
def extract_from_history_docs(query: str) -> str:
    """Інструмент для пошуку інформації в документах з історії"""
    model = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.1)
    result = retrieve_relevant_chunks(history_chunks_file, model, query)
    return result

@tool
def extract_from_ukr_lit_docs(query: str) -> str:
    """Інструмент для пошуку інформації в документах з української літератури"""
    model = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.1)
    result = retrieve_relevant_chunks(literature_chunks_file, model, query)
    return result

def setup_qa_app():
    history_tools = [extract_from_history_docs]
    ukr_lit_tools = [extract_from_ukr_lit_docs]
    ukr_lang_tools = [spelling_check, search_vocab_dict]
    wikipedia_tools = [search_wikipedia]

    model_with_tools = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0).bind_tools(history_tools + ukr_lit_tools + ukr_lang_tools + wikipedia_tools)

    def should_continue(state: MessagesState):
        messages = state["messages"]
        if len(messages) == 5:
            return END
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
        documents_dir = os.path.join(base_dir, 'documents_txt')
        os.makedirs(data_dir, exist_ok=True)

        literature_docs = os.path.join(documents_dir, 'literature', '*.txt')
        preprocess_documents(literature_docs, literature_chunks_file)
        history_docs = os.path.join(documents_dir, 'history', '*.txt')
        preprocess_documents(history_docs, history_chunks_file)

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


base_dir = os.path.join('..', '..', 'retriever_pipeline')
data_dir = os.path.join(base_dir, 'data')
literature_chunks_file = os.path.join(data_dir, 'literature_chunks.pkl')
history_chunks_file = os.path.join(data_dir, 'history_chunks.pkl')


if __name__ == "__main__":


    agent = ZNOAgent()
    agent.render_app_graph()

    question = "Ти агент, який вміє розв'язувати тести з української мови, української літератури та історії України. Якщо вхідне питання з української мови, не переформульовуй його" + "Реалізація імперської стратегії Росії в Першій світовій війні щодо \"…злиття землі Ярослава Осмомисла, князів Данила і Романа з Імперією в політичному, соціальному та національному відношеннях…\" стала можливою завдяки\nА. Карпатській операції.\nБ. Горліцькому прориву.\nВ. Брусиловському прориву.\nГ. Галицькій битві."
    print(agent.ask_question(question))

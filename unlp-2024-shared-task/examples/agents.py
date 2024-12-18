from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain.llms.base import LLM
from typing import Optional, List
from pydantic import BaseModel, PrivateAttr


# Custom Mistral Wrapper for LangChain
class MistralLLM(LLM, BaseModel):
    api_key: str
    model: str = "mistral-large-latest"
    _client = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from mistralai import Mistral  # Import the Mistral library here
        self._client = Mistral(api_key=self.api_key)

    @property
    def _llm_type(self) -> str:
        return "mistral"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        chat_response = self._client.chat.complete(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
            ]
        )
        return chat_response.choices[0].message.content


# Initialize the Mistral client through the custom LLM wrapper
mistral_llm = MistralLLM(api_key="apikey")

# Define the prompt template
prompt = PromptTemplate(
    template="""
You are an AI assistant with expertise in data analysis and automation. Answer the following question:
Question: {question}
""",
    input_variables=["question"]
)

# Create a runnable sequence
chain = prompt | mistral_llm

# Example query
query = "What is the impact of AI in healthcare?"
response = chain.invoke({"question": query})
print(f"Agent Response: {response}")

from typing import Any, Dict, List
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
import os
from dotenv import load_dotenv

load_dotenv()

class RunLLM:
    def __init__(self, index_name):
        self.llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=os.environ.get("OPENAI_API_KEY"))
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
        self.vectorstore = PineconeVectorStore(
            index_name=index_name, embedding=self.embeddings
            )
        self.rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

        self.retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
        #self.combine_docs_chain = create_stuff_documents_chain(self.llm, self.retrieval_qa_chat_prompt)
        self.stuff_documents_chain = create_stuff_documents_chain(self.llm, self.retrieval_qa_chat_prompt)

        self.history_aware_retriever = create_history_aware_retriever(
            llm=self.llm, retriever=self.vectorstore.as_retriever(), prompt=self.rephrase_prompt
        )

        self.qa = create_retrieval_chain(
            retriever=self.history_aware_retriever, combine_docs_chain=self.stuff_documents_chain
        )
        # self.retrival_chain = create_retrieval_chain(
        #     retriever=self.vectorstore.as_retriever(), combine_docs_chain=self.combine_docs_chain
        # )

    def run_query(self, query, chat_history):
        result = self.qa.invoke(input={"input": query, "chat_history": chat_history})
        return result['answer']



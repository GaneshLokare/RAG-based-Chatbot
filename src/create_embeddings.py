from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
import time
from pinecone import Pinecone, ServerlessSpec
import re

#Load environment variables
load_dotenv()


class CreateEmbeddings:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))

    def create_index(self, index_name):


        pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

        cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
        region = os.environ.get('PINECONE_REGION') or 'us-east-1'
        spec = ServerlessSpec(cloud=cloud, region=region)

        # index_name = "rag-getting-started"

        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=1536,
                metric="cosine",
                spec=spec
            )
            # Wait for index to be ready
            while not pc.describe_index(index_name).status['ready']:
                time.sleep(1)

        # See that it is empty
        print("Index before upsert:")
        print(pc.Index(index_name).describe_index_stats())
        print("\n")


    def create_embeddings(self, texts, index_name):
        self.create_index(index_name)
        PineconeVectorStore.from_documents(texts, self.embeddings, index_name = index_name)
        print("****** Added to Pinecone vectorstore vectors")







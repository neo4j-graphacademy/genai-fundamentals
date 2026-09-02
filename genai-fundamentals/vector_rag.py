import os
from dotenv import load_dotenv
load_dotenv()

from neo4j import GraphDatabase
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings
from neo4j_graphrag.retrievers import VectorRetriever
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.generation import GraphRAG

# Connect to Neo4j database
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"), 
    auth=(
        os.getenv("NEO4J_USERNAME"), 
        os.getenv("NEO4J_PASSWORD")
    )
)

# Create embedder
embedder = OpenAIEmbeddings(model="text-embedding-ada-002")

# Create retriever
retriever = VectorRetriever(
    driver,
    neo4j_database=os.getenv("NEO4J_DATABASE"),
    index_name="moviePlots",
    embedder=embedder,
    return_properties=["title", "plot"],
)

# Create the LLM
llm = OpenAILLM(
    model_name=os.getenv("OPENROUTER_MODEL"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model_params={
        "temperature": 0.2,
        "max_tokens": 1000
    }
)

# Create GraphRAG pipeline
rag = GraphRAG(retriever=retriever, llm=llm)


# Search
query_text = "Give me the most interesting drama movies"

response = rag.search(
    query_text=query_text, 
    retriever_config={"top_k": 5}
)

print()
print()
print()
print()
print(response.answer)
# Close the database connection

driver.close()
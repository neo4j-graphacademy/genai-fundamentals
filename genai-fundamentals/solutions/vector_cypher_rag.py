import os
from dotenv import load_dotenv
load_dotenv()

from neo4j import GraphDatabase
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings
# tag::import-retriever[]
from neo4j_graphrag.retrievers import VectorCypherRetriever
# end::import-retriever[]
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

# tag::retrieval_query[]
# Define retrieval query
retrieval_query = """
MATCH (node)<-[r:RATED]-()
RETURN 
  node.title AS title, node.plot AS plot, score AS similarityScore, 
  collect { MATCH (node)-[:IN_GENRE]->(g) RETURN g.name } as genres, 
  collect { MATCH (node)<-[:ACTED_IN]->(a) RETURN a.name } as actors, 
  avg(r.rating) as userRating
ORDER BY userRating DESC
"""
# end::retrieval_query[]

# tag::retriever[]
# Create retriever
retriever = VectorCypherRetriever(
    driver,
    index_name="moviePlots",
    embedder=embedder,
    retrieval_query=retrieval_query,
)
# end::retriever[]

#  Create the LLM
llm = OpenAILLM(model_name="gpt-4o")

# Create GraphRAG pipeline
rag = GraphRAG(retriever=retriever, llm=llm)

# Search
query_text = "Find the highest rated action movie about travelling to other planets"

response = rag.search(
    query_text=query_text, 
    retriever_config={"top_k": 5},
    return_context=True
)

print(response.answer)
print("CONTEXT:", response.retriever_result.items)

# Close the database connection
driver.close()
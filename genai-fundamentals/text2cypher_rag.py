import os
from dotenv import load_dotenv
load_dotenv()

from neo4j import GraphDatabase
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.retrievers import Text2CypherRetriever


# Connect to Neo4j database
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"), 
    auth=(
        os.getenv("NEO4J_USERNAME"), 
        os.getenv("NEO4J_PASSWORD")
    )
)

# Create LLM 
t2c_llm = OpenAILLM(
    model_name=os.getenv("OPENROUTER_MODEL"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model_params={
        "temperature": 0.2,
        "max_tokens": 1000
    }
)

# Cypher examples as input/query pairs
examples = [
    "USER INPUT: 'Get user ratings for a movie?' QUERY: MATCH (u:User)-[r:RATED]->(m:Movie) WHERE m.title = 'Movie Title' RETURN r.rating"
]

# Specify your own Neo4j schema
neo4j_schema = """
Node properties:
Person {name: STRING, born: INTEGER}
Movie {tagline: STRING, title: STRING, released: INTEGER}
Genre {name: STRING}
User {name: STRING}

Relationship properties:
ACTED_IN {role: STRING}
RATED {rating: INTEGER}

The relationships:
(:Person)-[:ACTED_IN]->(:Movie)
(:Person)-[:DIRECTED]->(:Movie)
(:User)-[:RATED]->(:Movie)
(:Movie)-[:IN_GENRE]->(:Genre)
"""

# Build the retriever
retriever = Text2CypherRetriever(
    driver=driver,
    neo4j_database=os.getenv("NEO4J_DATABASE"),
    llm=t2c_llm,
    neo4j_schema=neo4j_schema,
    examples=examples
)


llm = OpenAILLM(model_name="gpt-5.2")
rag = GraphRAG(retriever=retriever, llm=llm)

query_text = "Which user has given the most reviews for the Horror genre?"

response = rag.search(
    query_text=query_text,
    return_context=True
    )

print(response.answer)
print()
print()
print("CYPHER :", response.retriever_result.metadata["cypher"])
print()
print()
print("CONTEXT:", response.retriever_result.items)

driver.close()

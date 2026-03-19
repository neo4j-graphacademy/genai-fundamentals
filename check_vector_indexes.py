import os
from dotenv import load_dotenv
load_dotenv()

from neo4j import GraphDatabase

# Connect to Neo4j database
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"), 
    auth=(
        os.getenv("NEO4J_USERNAME"), 
        os.getenv("NEO4J_PASSWORD")
    )
)

def check_vector_indexes(tx, db_name):
    # Query to get vector indexes in specific database
    result = tx.run(f"SHOW INDEXES WHERE type = 'VECTOR'")
    return result.data()

# Execute the query
with driver.session(database=os.getenv("NEO4J_DATABASE")) as session:
    indexes = session.execute_read(check_vector_indexes, os.getenv("NEO4J_DATABASE"))
    
print(f"Vector indexes in database '{os.getenv('NEO4J_DATABASE')}':")
print("-" * 80)
if indexes:
    for idx in indexes:
        print(f"Name: {idx['name']}")
        print(f"Type: {idx['type']}")
        print(f"State: {idx['state']}")
        print(f"Properties: {idx['properties']}")
        print(f"Dimension: {idx.get('dimension', 'N/A')}")
        print()
else:
    print("No vector indexes found")

driver.close()

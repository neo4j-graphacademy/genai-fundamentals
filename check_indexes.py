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

def check_indexes(tx):
    # Query to get all vector indexes
    result = tx.run("SHOW INDEXES")
    return result.data()

# Execute the query
with driver.session() as session:
    indexes = session.execute_read(check_indexes)
    
print("Available indexes in the database:")
print("-" * 80)
for idx in indexes:
    print(f"Name: {idx['name']}")
    print(f"Type: {idx['type']}")
    print(f"State: {idx['state']}")
    print(f"Properties: {idx['properties']}")
    print()

driver.close()

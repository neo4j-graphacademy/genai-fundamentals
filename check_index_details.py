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

def get_index_info(tx):
    # Get detailed info about moviePlots index
    result = tx.run("""
        SHOW INDEXES WHERE name = 'moviePlots'
    """)
    return result.data()

# Execute the query
with driver.session(database=os.getenv("NEO4J_DATABASE")) as session:
    indexes = session.execute_read(get_index_info)
    
print("Detailed information for moviePlots index:")
print("-" * 80)
for idx in indexes:
    for key, value in idx.items():
        print(f"{key}: {value}")

driver.close()

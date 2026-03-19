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

def check_index_infos_query(tx, index_name):
    # This is what neo4j_graphrag uses internally
    query = f"""
    SHOW INDEXES 
    WHERE name = $index_name 
    AND type = "VECTOR"
    """
    result = tx.run(query, index_name=index_name)
    return result.data()

# Execute the query
with driver.session(database=os.getenv("NEO4J_DATABASE")) as session:
    records = session.execute_read(check_index_infos_query, "moviePlots")
    
print(f"Records returned: {len(records)}")
for i, record in enumerate(records):
    print(f"\nRecord {i}:")
    print(record)

driver.close()

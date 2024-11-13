from .base_agent import BaseAgent
from neo4j import GraphDatabase

class DatabaseAgent(BaseAgent):
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def query_papers(self, topic, year):
        with self.driver.session() as session:
            query = f"MATCH (p:Paper {{topic: '{topic}', year: {year}}}) RETURN p"
            return session.run(query)

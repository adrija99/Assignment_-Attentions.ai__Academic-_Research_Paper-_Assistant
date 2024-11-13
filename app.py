import arxivpy
from neo4j import GraphDatabase
from fastapi import FastAPI
from pydantic import BaseModel

# Neo4j connection details
NEO4J_BOLT_URL = "neo4j+s://<instance-id>.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "m31ng71vgWSUotm9Qn8DiK9fEZNoGZ74HBHJqzD-71k"

# Initialize the FastAPI app
app = FastAPI()

# Create a Neo4j driver instance
driver = GraphDatabase.driver(NEO4J_BOLT_URL, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# Define the Paper data model for API endpoints
class Paper(BaseModel):
    title: str
    abstract: str
    year: int
    topic: str
    url: str

# Search papers from Arxiv based on a topic
def search_papers_from_arxiv(topic: str, max_results: int = 5):
    search_results = arxivpy.query(query=topic, max_results=max_results, start=0, sort_by="submittedDate", order="descending")
    papers = []

    for entry in search_results:
        papers.append({
            "title": entry["title"],
            "abstract": entry["summary"],
            "year": entry["published"][:4],  # Extract year from date string
            "topic": topic,
            "url": entry["link"]
        })

    return papers

# Store the fetched papers in Neo4j
def store_papers_in_neo4j(papers):
    with driver.session() as session:
        for paper in papers:
            session.run(
                """
                CREATE (p:Paper {title: $title, abstract: $abstract, year: $year, topic: $topic, url: $url})
                """,
                title=paper["title"],
                abstract=paper["abstract"],
                year=paper["year"],
                topic=paper["topic"],
                url=paper["url"]
            )

# API endpoint to search and store papers
@app.get("/search_and_store_papers")
async def search_and_store_papers(topic: str, max_results: int = 5):
    papers = search_papers_from_arxiv(topic, max_results)
    store_papers_in_neo4j(papers)
    return {"status": "Papers successfully fetched and stored in Neo4j", "papers": papers}

# Shutdown event to close Neo4j connection
@app.on_event("shutdown")
async def shutdown_event():
    driver.close()


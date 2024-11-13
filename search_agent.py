from .base_agent import BaseAgent

class SearchAgent(BaseAgent):
    def search_papers(self, topic):
        prompt = f"Search for recent research papers on {topic}"
        results = self.call_model(prompt)
        # Code to interact with an API or fetch papers goes here
        return results

from .base_agent import BaseAgent

class FutureWorksAgent(BaseAgent):
    def suggest_future_research(self, papers_summary):
        prompt = f"Suggest future research directions based on: {papers_summary}"
        return self.call_model(prompt)

class BaseAgent:
    def __init__(self, model):
        self.model = model

    def call_model(self, prompt):
        # General method to interact with the LLM
        return self.model(prompt)

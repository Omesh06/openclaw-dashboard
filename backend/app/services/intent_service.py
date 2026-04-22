import os

class IntentTranslationService:
    def __init__(self, llm_provider=None):
        self.llm_provider = llm_provider

    def summarize_intent(self, jira_context):
        """
        Translates raw Jira data into a plain-English intent summary.
        """
        summary = jira_context.get("summary", "")
        description = jira_context.get("description", "")
        comments = "\n".join(jira_context.get("comments", []))

        prompt = f"""
        You are a technical analyst. Based on the following Jira ticket details, 
        provide a concise, 2-sentence summary of the 'Developer Intent'.
        Explain WHY this change was made and what the primary goal was.

        Summary: {summary}
        Description: {description}
        Comments: {comments}
        
        Intent Summary:
        """
        
        # In a real scenario, this would call OpenAI/Claude/etc.
        # For the verification phase, we mock the AI response.
        if self.llm_provider == "mock":
            return f"[MOCK AI] The developer intended to {summary.lower()} to improve system stability and fulfill the requirements in the description."
        
        # Real implementation would go here
        # return self.llm_provider.generate(prompt)
        return "LLM Provider not configured. Please set provider to 'mock' for testing."

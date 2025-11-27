class Orchestrator:
    def __init__(self, vision_agent, knowledge_agent, session_store: dict):
        self.vision_agent = vision_agent
        self.knowledge_agent = knowledge_agent
        self.session_store = session_store

    def run(self, user_id: str, image_path: str | None, query: str) -> dict:
        session = self.session_store.get(user_id, {"history": [], "skill_level": "beginner"})
        vision_result = None
        if image_path:
            vision_result = self.vision_agent.analyze(image_path, session["skill_level"])
        coach_result = self.knowledge_agent.coach(
            query=query,
            vision_analysis=vision_result,
            session=session,
        )
        session["history"].append({"query": query, "vision": vision_result, "coach": coach_result})
        self.session_store[user_id] = session
        return {"vision": vision_result, "coach": coach_result, "session": session}

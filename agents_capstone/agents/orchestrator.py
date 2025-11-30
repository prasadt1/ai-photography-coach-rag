from dataclasses import asdict
from typing import Optional, Dict, Any

from agents_capstone.agents.vision_agent import VisionAgent, VisionAnalysis
from agents_capstone.agents.knowledge_agent import KnowledgeAgent, CoachingResponse
from agents_capstone.agents import SESSION_STORE

class Orchestrator:
    """Coordinates agents and tracks session state."""

    def __init__(self, vision_agent: VisionAgent, knowledge_agent: KnowledgeAgent):
        self.vision_agent = vision_agent
        self.knowledge_agent = knowledge_agent

    def _get_session(self, user_id: str) -> Dict[str, Any]:
        if user_id not in SESSION_STORE:
            SESSION_STORE[user_id] = {
                "skill_level": "beginner",
                "history": [],
            }
        return SESSION_STORE[user_id]

    def run(
        self,
        user_id: str,
        image_path: Optional[str],
        query: str,
    ) -> Dict[str, Any]:
        session = self._get_session(user_id)
        skill_level = session.get("skill_level", "beginner")

        vision_result: Optional[VisionAnalysis] = None
        if image_path:
            vision_result = self.vision_agent.analyze(image_path, skill_level)

        coach_result: CoachingResponse = self.knowledge_agent.coach(
            query=query,
            vision_analysis=vision_result,
            session=session,
        )

        session["history"].append(
            {
                "query": query,
                "issues": vision_result.issues if vision_result else [],
            }
        )

        combined: Dict[str, Any] = {
            "vision": asdict(vision_result) if vision_result else None,
            "coach": {
                "text": coach_result.text,
                "issues": coach_result.issues,
                "exercise": coach_result.exercise,
                "principles": [asdict(p) for p in coach_result.principles],
            },
            "session": session,
        }
        return combined

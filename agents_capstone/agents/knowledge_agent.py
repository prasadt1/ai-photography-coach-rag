from dataclasses import dataclass
from typing import List, Optional

from agents_capstone.tools.knowledge_base import simple_retrieve, Principle

@dataclass
class CoachingResponse:
    text: str
    principles: List[Principle]
    issues: List[str]
    exercise: str

class KnowledgeAgent:
    """Turns analysis + question + history into coaching text."""

    def coach(
        self,
        query: str,
        vision_analysis: Optional[object],
        session: dict,
    ) -> CoachingResponse:
        issues: List[str] = []
        if vision_analysis is not None:
            issues = list(getattr(vision_analysis, "issues", []))

        retrieval_query = query + " " + " ".join(issues)
        principles = simple_retrieve(retrieval_query)

        lines: List[str] = []
        lines.append("Here is how you can improve this photo:")

        if "subject_centered" in issues:
            lines.append(
                "- Move your main subject towards one of the thirds instead of the exact center."
            )
        if "shallow_depth_of_field" in issues:
            lines.append(
                "- At very wide apertures, be careful where you place focus so key details stay sharp."
            )

        lines.append(
            "- Check that your horizon is level; a small tilt can make landscapes feel unbalanced."
        )
        lines.append(
            "- Use foreground elements or leading lines to guide the viewer’s eye into the scene."
        )

        exercise = (
            "Exercise: Take 10 photos of a similar scene. For each frame, place the subject "
            "on a different third, keep the horizon straight, and review which compositions feel strongest."
        )

        return CoachingResponse(
            text="\n".join(lines),
            principles=principles,
            issues=issues,
            exercise=exercise,
        )

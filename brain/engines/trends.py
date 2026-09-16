"""
Engine 9 — TREND DETECTION
Detects emerging technical narratives before they saturate:
- AI Agents & Agent Payments (x402)
- Verifiable Onchain Inference & TEEs
- Parallel EVM & Real-Time Settlement
- ZK Coprocessors & State Attestation
- DePIN & Compute Coordination

Tracks discussion velocity, repository growth, grant capital allocation, and new SDKs.
Focuses strictly on developer incentives and technical traction, NOT speculative token price.
"""
from typing import Dict, List, Any
from brain.db.database import Database


class TrendDetector:
    def __init__(self, db: Database = None):
        self.db = db or Database()

    def get_narrative_velocity(self) -> List[Dict[str, Any]]:
        """
        Returns all tracked technical narratives ranked by composite velocity score.
        """
        return self.db.get_all_trends()

    def identify_leading_edges(self) -> List[Dict[str, Any]]:
        """
        Identifies trends where discussion velocity + grants moving >= 180.0
        """
        trends = self.db.get_all_trends()
        leading = []
        for t in trends:
            total_momentum = t.get("discussion_velocity", 0.0) + t.get("grants_moving", 0.0)
            if total_momentum >= 175.0:
                leading.append(t)
        return leading

    def assess_trend_relevance(self, project_idea: str) -> Dict[str, Any]:
        """
        Assesses how well a proposed project aligns with the strongest builder trends.
        """
        trends = self.db.get_all_trends()
        matched = []
        for t in trends:
            name_words = set(t["narrative_name"].lower().split())
            if any(w in project_idea.lower() for w in name_words if len(w) > 3):
                matched.append(t)

        return {
            "matched_trends": matched,
            "alignment_score": min(len(matched) * 35.0, 100.0)
        }

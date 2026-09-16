"""
-------------------------------------------------------------------------------
ENGINE 9: TREND DETECTION
-------------------------------------------------------------------------------
This engine tracks emerging technical narratives BEFORE they become crowded:

- AI Agents onchain (autonomous agent wallets, x402 HTTP micropayments)
- Verifiable Onchain Inference & TEE Guardrails
- Parallel EVM high-throughput settlement (Monad, MegaETH)
- ZK Coprocessors & Cross-Chain State Proofs
- DePIN & Compute Coordination

Crucial Rule:
We track developer traction, new SDKs, and grant capital flow —
NEVER speculative token price movements!
"""

from typing import Dict, List, Any
from brain.db.database import Database


class TrendDetector:
    """Discovers emerging technical narratives where developer incentives are moving."""

    def __init__(self, db: Database = None):
        self.db = db if db is not None else Database()

    def get_narrative_velocity(self) -> List[Dict[str, Any]]:
        """
        Step 1: Returns all technical narratives ranked by composite velocity score.
        """
        return self.db.get_all_trends()

    def identify_leading_edges(self) -> List[Dict[str, Any]]:
        """
        Step 2: Finds trends where both discussion velocity and grant capital flow
        are at the absolute top tier (total momentum >= 175).
        """
        all_trends = self.db.get_all_trends()
        leading_edges = []

        for trend in all_trends:
            discussion = trend.get("discussion_velocity", 0.0)
            grants = trend.get("grants_moving", 0.0)
            total_momentum = discussion + grants

            if total_momentum >= 175.0:
                leading_edges.append(trend)

        return leading_edges

    def assess_trend_relevance(self, project_idea: str) -> Dict[str, Any]:
        """
        Step 3: Checks how well a proposed project idea aligns with hot builder trends.
        """
        all_trends = self.db.get_all_trends()
        matched_trends = []

        for trend in all_trends:
            name_words = set(trend["narrative_name"].lower().split())
            if any(word in project_idea.lower() for word in name_words if len(word) > 3):
                matched_trends.append(trend)

        alignment_score = min(len(matched_trends) * 35.0, 100.0)

        return {
            "matched_trends": matched_trends,
            "alignment_score": alignment_score
        }

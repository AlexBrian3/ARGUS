"""
Engine 2 — ECOSYSTEM RADAR
Continuously monitors important and emerging developer ecosystems.
Calculates Ecosystem Momentum Score /100 and trajectory (↑ accelerating, → stable, ↓ declining).
Detects ecosystems BEFORE their major hackathons.
"""
from typing import Dict, List, Any, Tuple
from brain.config import ECOSYSTEM_MOMENTUM_WEIGHTS
from brain.db.database import Database


class EcosystemRadar:
    def __init__(self, db: Database = None):
        self.db = db or Database()

    def calculate_momentum_score(self, metrics: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
        """
        Calculate total momentum score /100 based on 8 weighted factors:
        - Developer programs: 20
        - Hackathons/grants: 20
        - Developer activity acceleration: 15
        - SDK/protocol launches: 10
        - Sponsor activity: 10
        - Social discussion acceleration: 10
        - Funding/startup activity: 5
        - Competition opportunity: 10
        """
        score = 0.0
        breakdown = {}
        for key, weight in ECOSYSTEM_MOMENTUM_WEIGHTS.items():
            val = float(metrics.get(key, 0.0))
            # clamp value to max weight
            clamped = min(max(val, 0.0), float(weight))
            score += clamped
            breakdown[key] = round(clamped, 2)

        return round(score, 1), breakdown

    def determine_trajectory(self, current_score: float, previous_score: float = None, delta_threshold: float = 2.0) -> str:
        """
        Determines whether momentum is:
        ↑ accelerating
        → stable
        ↓ declining
        """
        if previous_score is None:
            if current_score >= 85.0:
                return "↑"
            elif current_score >= 70.0:
                return "→"
            else:
                return "↓"

        diff = current_score - previous_score
        if diff >= delta_threshold:
            return "↑"
        elif diff <= -delta_threshold:
            return "↓"
        else:
            return "→"

    def update_ecosystem_momentum(
        self,
        slug: str,
        name: str,
        category: str,
        metrics: Dict[str, float],
        notes: str = "",
        tracked_repos: List[str] = None
    ) -> Dict[str, Any]:
        existing = self.db.get_ecosystem(slug)
        prev_score = existing["momentum_score"] if existing else None

        score, breakdown = self.calculate_momentum_score(metrics)
        trajectory = self.determine_trajectory(score, prev_score)

        data = {
            "slug": slug,
            "name": name,
            "category": category,
            "momentum_score": score,
            "momentum_trajectory": trajectory,
            "breakdown_scores": breakdown,
            "tracked_repos": tracked_repos or (existing["tracked_repos"] if existing else []),
            "notes": notes or (existing["notes"] if existing else "")
        }
        self.db.upsert_ecosystem(data)
        return data

    def get_leaderboard(self) -> List[Dict[str, Any]]:
        """Returns all monitored ecosystems ranked by momentum score."""
        return self.db.get_all_ecosystems()

    def detect_stealth_opportunities(self) -> List[Dict[str, Any]]:
        """
        Detects ecosystems that are accelerating (↑) with high dev program/grant activity
        before mainstream hackathon announcements.
        """
        ecosystems = self.db.get_all_ecosystems()
        stealth = []
        for eco in ecosystems:
            if eco["momentum_trajectory"] == "↑" and eco["momentum_score"] >= 80.0:
                breakdown = eco["breakdown_scores"]
                programs = breakdown.get("developer_programs", 0.0)
                grants = breakdown.get("hackathons_and_grants", 0.0)
                if (programs + grants) >= 32.0:
                    stealth.append(eco)
        return stealth

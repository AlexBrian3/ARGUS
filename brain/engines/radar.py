"""
-------------------------------------------------------------------------------
ENGINE 2: ECOSYSTEM RADAR
-------------------------------------------------------------------------------
Continuously monitors important developer ecosystems (Solana, Base, Monad, etc.).

Calculates:
1. ECOSYSTEM MOMENTUM SCORE (out of 100)
2. TRAJECTORY (↑ accelerating, → stable, ↓ declining)
3. STEALTH OPPORTUNITIES: Detects ecosystems BEFORE their big hackathons!
"""

from typing import Dict, List, Any, Tuple
from brain.config import ECOSYSTEM_MOMENTUM_WEIGHTS
from brain.db.database import Database


class EcosystemRadar:
    """Monitors developer momentum across emerging and established ecosystems."""

    def __init__(self, db: Database = None):
        # If no database is passed in, create a connection to the default one
        self.db = db if db is not None else Database()

    def calculate_momentum_score(self, metrics: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
        """
        Step 1: Calculate the momentum score (out of 100) by checking 8 key factors:
        - Developer programs (20 pts)
        - Hackathons and grants (20 pts)
        - Developer activity acceleration (15 pts)
        - SDK launches (10 pts)
        - Sponsor activity (10 pts)
        - Social discussion (10 pts)
        - Funding activity (5 pts)
        - Competition opportunity (10 pts)
        """
        total_score = 0.0
        score_breakdown = {}

        for factor_name, max_allowed_weight in ECOSYSTEM_MOMENTUM_WEIGHTS.items():
            # Get the raw value (default to 0.0 if not provided)
            raw_value = float(metrics.get(factor_name, 0.0))

            # Make sure the value cannot be negative or higher than the max allowed weight
            clamped_value = min(max(raw_value, 0.0), float(max_allowed_weight))

            total_score += clamped_value
            score_breakdown[factor_name] = round(clamped_value, 2)

        return round(total_score, 1), score_breakdown

    def determine_trajectory(
        self,
        current_score: float,
        previous_score: float = None,
        delta_threshold: float = 2.0
    ) -> str:
        """
        Step 2: Determine if momentum is speeding up, staying flat, or slowing down:
        ↑ = accelerating (heating up!)
        → = stable (healthy and steady)
        ↓ = declining (cooling off)
        """
        # If this is our very first time measuring this ecosystem:
        if previous_score is None:
            if current_score >= 85.0:
                return "↑"
            elif current_score >= 70.0:
                return "→"
            else:
                return "↓"

        # Compare new score against old score
        score_difference = current_score - previous_score

        if score_difference >= delta_threshold:
            return "↑"  # Score jumped by at least 2 points
        elif score_difference <= -delta_threshold:
            return "↓"  # Score dropped by at least 2 points
        else:
            return "→"  # Within normal variation

    def update_ecosystem_momentum(
        self,
        slug: str,
        name: str,
        category: str,
        metrics: Dict[str, float],
        notes: str = "",
        tracked_repos: List[str] = None
    ) -> Dict[str, Any]:
        """
        Step 3: Save the updated scores into persistent database memory.
        """
        existing_record = self.db.get_ecosystem(slug)
        previous_score = existing_record["momentum_score"] if existing_record else None

        score, breakdown = self.calculate_momentum_score(metrics)
        trajectory = self.determine_trajectory(score, previous_score)

        data = {
            "slug": slug,
            "name": name,
            "category": category,
            "momentum_score": score,
            "momentum_trajectory": trajectory,
            "breakdown_scores": breakdown,
            "tracked_repos": tracked_repos or (existing_record["tracked_repos"] if existing_record else []),
            "notes": notes or (existing_record["notes"] if existing_record else "")
        }

        self.db.upsert_ecosystem(data)
        return data

    def get_leaderboard(self) -> List[Dict[str, Any]]:
        """Returns all ecosystems sorted from highest momentum to lowest."""
        return self.db.get_all_ecosystems()

    def detect_stealth_opportunities(self) -> List[Dict[str, Any]]:
        """
        Step 4: Find ecosystems that are quietly ramping up developer incentives
        before their big hackathon is announced to the public crowd!
        """
        all_ecosystems = self.db.get_all_ecosystems()
        stealth_list = []

        for ecosystem in all_ecosystems:
            is_accelerating = ecosystem.get("momentum_trajectory") == "↑"
            has_high_score = ecosystem.get("momentum_score", 0.0) >= 80.0

            if is_accelerating and has_high_score:
                breakdown = ecosystem.get("breakdown_scores", {})
                programs = breakdown.get("developer_programs", 0.0)
                grants = breakdown.get("hackathons_and_grants", 0.0)

                # If developer incentives + grants add up to 32+ points:
                if (programs + grants) >= 32.0:
                    stealth_list.append(ecosystem)

        return stealth_list

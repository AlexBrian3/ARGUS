"""
Engine 3 — SPONSOR INTELLIGENCE
Maintains persistent Sponsor Intelligence Cards.
Calculates Sponsor Predictability Score /100 and Likelihood of Appearing /100.
Identifies recurring winning product types, features frequently used vs rarely used,
oversaturated vs underserved ideas, and proactive preparation playbooks.
"""
from typing import Dict, List, Any, Optional
from brain.db.database import Database


class SponsorIntelligence:
    def __init__(self, db: Database = None):
        self.db = db or Database()

    def get_sponsor_card(self, slug: str) -> Optional[Dict[str, Any]]:
        """Retrieve persistent Sponsor Intelligence Card."""
        return self.db.get_sponsor(slug)

    def calculate_predictability_score(self, sponsor_data: Dict[str, Any]) -> float:
        """
        Calculates Sponsor Predictability Score /100 based on:
        - Repetition of previous hackathons (consistency across seasons) (30%)
        - Consistency of recurring bounty tracks and technologies (30%)
        - Repeat prize structure stability (20%)
        - Clear, reliable documentation and integration support (20%)
        """
        score = 0.0

        # Previous hackathons count
        prev_events = sponsor_data.get("previous_hackathons", [])
        score += min(len(prev_events) * 7.5, 30.0)

        # Recurring technologies & tracks
        recurring_tech = sponsor_data.get("recurring_technologies", [])
        score += min(len(recurring_tech) * 7.5, 30.0)

        # Documentation quality
        doc_qual = sponsor_data.get("documentation_quality", "Good")
        doc_points = {"Exceptional": 20.0, "Good": 15.0, "Moderate": 10.0, "Poor": 5.0}
        score += doc_points.get(doc_qual, 12.0)

        # Prize stability
        if sponsor_data.get("typical_prize_distribution"):
            score += 20.0
        else:
            score += 10.0

        return round(min(score, 100.0), 1)

    def calculate_upcoming_likelihood(self, slug: str, target_organizer: str = "ETHGlobal") -> float:
        """
        Calculate likelihood /100 of sponsor appearing at an upcoming event based on historical frequency.
        """
        sponsor = self.db.get_sponsor(slug)
        if not sponsor:
            return 50.0

        freq_str = sponsor.get("repeat_sponsorship_frequency", "").lower()
        if "universal" in freq_str or "9 of the last 10" in freq_str or "high" in freq_str:
            return 95.0
        elif "frequent" in freq_str or "regular" in freq_str:
            return 85.0
        elif "moderate" in freq_str:
            return 65.0
        else:
            return 45.0

    def get_proactive_prep_advisory(self, slug: str) -> str:
        """
        Generates actionable preparation advice before the next hackathon opens.
        """
        sponsor = self.db.get_sponsor(slug)
        if not sponsor:
            return "No intelligence card found for sponsor."

        pred_score = sponsor.get("predictability_score", 0.0)
        upcoming_score = sponsor.get("upcoming_likelihood", 0.0)
        name = sponsor.get("name", slug)
        prep = sponsor.get("recommended_preparation", "")
        frequent_feats = ", ".join(sponsor.get("features_frequently_used", []))
        rare_feats = ", ".join(sponsor.get("features_rarely_used", []))
        underserved = ", ".join(sponsor.get("underserved_ideas", []))

        return (
            f"**Sponsor Advisory: {name}**\n"
            f"- Predictability Score: {pred_score}/100 | Upcoming Likelihood: {upcoming_score}/100\n"
            f"- What they repeatedly reward: {sponsor.get('recurring_bounty_categories', [])}\n"
            f"- Features winners frequently use: {frequent_feats}\n"
            f"- High-leverage / rarely used features: {rare_feats}\n"
            f"- Underserved opportunity niches: {underserved}\n"
            f"- Recommended Preparation NOW: {prep}"
        )

    def get_all_sponsor_cards(self) -> List[Dict[str, Any]]:
        return self.db.get_all_sponsors()

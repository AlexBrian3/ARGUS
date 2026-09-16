"""
-------------------------------------------------------------------------------
ENGINE 3: SPONSOR INTELLIGENCE
-------------------------------------------------------------------------------
Whenever a company or protocol sponsors a hackathon, ARGUS reverse-engineers
their previous behavior:

1. What do they repeatedly reward? (e.g. Mini Apps, Oracle integrations)
2. What sponsor features do winning projects use that competitors ignore?
3. What are oversaturated ideas to avoid?
4. What is the SPONSOR PREDICTABILITY SCORE (out of 100)?
5. What is the LIKELIHOOD OF REAPPEARING in the next event?

Example:
"World has appeared in 9 of the last 10 ETHGlobal events. High predictability.
Preparation: Learn MiniKit + World ID now before the next event opens."
"""

from typing import Dict, List, Any, Optional
from brain.db.database import Database


class SponsorIntelligence:
    """Maintains persistent intelligence cards on repeating hackathon sponsors."""

    def __init__(self, db: Database = None):
        self.db = db if db is not None else Database()

    def get_sponsor_card(self, slug: str) -> Optional[Dict[str, Any]]:
        """Fetch the persistent profile card for a sponsor."""
        return self.db.get_sponsor(slug)

    def calculate_predictability_score(self, sponsor_data: Dict[str, Any]) -> float:
        """
        Step 1: Calculate Sponsor Predictability Score (out of 100).
        High score means this sponsor consistently offers the same bounties
        and rewards the same types of projects.
        """
        score = 0.0

        # Criterion 1: Consistency of attending past hackathons (max 30 points)
        previous_events = sponsor_data.get("previous_hackathons", [])
        score += min(len(previous_events) * 7.5, 30.0)

        # Criterion 2: Consistency of recurring technologies (max 30 points)
        recurring_tech = sponsor_data.get("recurring_technologies", [])
        score += min(len(recurring_tech) * 7.5, 30.0)

        # Criterion 3: Documentation and SDK quality (max 20 points)
        doc_quality = sponsor_data.get("documentation_quality", "Good")
        quality_points = {
            "Exceptional": 20.0,
            "Good": 15.0,
            "Moderate": 10.0,
            "Poor": 5.0
        }
        score += quality_points.get(doc_quality, 12.0)

        # Criterion 4: Reliable prize distribution (max 20 points)
        if sponsor_data.get("typical_prize_distribution"):
            score += 20.0
        else:
            score += 10.0

        return round(min(score, 100.0), 1)

    def calculate_upcoming_likelihood(self, slug: str, target_organizer: str = "ETHGlobal") -> float:
        """
        Step 2: Estimate how likely this sponsor will appear at the next big event.
        Returns a probability score between 0.0 and 100.0.
        """
        sponsor = self.db.get_sponsor(slug)
        if not sponsor:
            return 50.0

        frequency_text = sponsor.get("repeat_sponsorship_frequency", "").lower()

        if "universal" in frequency_text or "9 of the last 10" in frequency_text or "high" in frequency_text:
            return 95.0
        elif "frequent" in frequency_text or "regular" in frequency_text:
            return 85.0
        elif "moderate" in frequency_text:
            return 65.0
        else:
            return 45.0

    def get_proactive_prep_advisory(self, slug: str) -> str:
        """
        Step 3: Generate a simple, plain-English study guide so you can learn
        the right tools BEFORE registration opens.
        """
        sponsor = self.db.get_sponsor(slug)
        if not sponsor:
            return "No intelligence card found for this sponsor."

        name = sponsor.get("name", slug)
        pred_score = sponsor.get("predictability_score", 0.0)
        upcoming_score = sponsor.get("upcoming_likelihood", 0.0)
        frequent_features = ", ".join(sponsor.get("features_frequently_used", []))
        rare_features = ", ".join(sponsor.get("features_rarely_used", []))
        underserved_niches = ", ".join(sponsor.get("underserved_ideas", []))
        prep_action = sponsor.get("recommended_preparation", "")

        return (
            f"**Sponsor Advisory: {name}**\n"
            f"- Predictability Score: {pred_score}/100 | Upcoming Likelihood: {upcoming_score}/100\n"
            f"- What they repeatedly reward: {sponsor.get('recurring_bounty_categories', [])}\n"
            f"- Features winners frequently use: {frequent_features}\n"
            f"- High-leverage features rarely used: {rare_features}\n"
            f"- Underserved opportunity niches: {underserved_niches}\n"
            f"- Recommended Preparation NOW: {prep_action}"
        )

    def get_all_sponsor_cards(self) -> List[Dict[str, Any]]:
        """Returns all persistent sponsor intelligence cards."""
        return self.db.get_all_sponsors()

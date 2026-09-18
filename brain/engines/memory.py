"""
-------------------------------------------------------------------------------
ENGINE 10: PERSISTENT MEMORY & KNOWLEDGE RETRIEVAL
-------------------------------------------------------------------------------
Rule: Never throw away research after an event ends!

This engine connects all 9 other engines to SQLite persistent storage.
Whenever a new opportunity appears, ARGUS automatically queries historical records:
- Has this sponsor appeared before? What did they reward?
- Did previous winners build infrastructure or consumer apps?
- What were the common losing mistakes?

The system gets smarter after every single competition!
"""

from typing import Dict, List, Any
from brain.db.database import Database


class PersistentMemory:
    """Unified knowledge retrieval across past competitions, winners, and sponsors."""

    def __init__(self, db: Database = None):
        self.db = db if db is not None else Database()

    def _get_ecosystem_context(self, ecosystem: str) -> Any:
        """Shared helper: looks up the ecosystem momentum card for an ecosystem string."""
        primary_ecosystem = (ecosystem or "").lower().split("/")[0].strip()
        return self.db.get_ecosystem(primary_ecosystem)

    def _match_sponsors(self, sponsor_names: List[str]) -> List[Dict[str, Any]]:
        """Shared helper: matches raw sponsor name strings against saved Sponsor Intelligence Cards."""
        matched_sponsors = []
        all_sponsors = self.db.get_all_sponsors()

        for sponsor_name in (sponsor_names or []):
            clean_name = sponsor_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
            for s in all_sponsors:
                if s["slug"] in clean_name or clean_name in s["slug"] or s["name"].lower() in sponsor_name.lower():
                    matched_sponsors.append(s)
                    break

        return matched_sponsors

    def get_context_for_raw_opportunity(self, ecosystem: str, sponsors: List[str]) -> Dict[str, Any]:
        """
        Looks up real ecosystem momentum and sponsor predictability scores from
        persistent memory for an opportunity that hasn't been saved to the database
        yet. Used by the Opportunity Scout (Engine 1) while it's still scoring a
        fresh opportunity, so HackScore reflects actual historical intelligence
        instead of a flat default.
        """
        ecosystem_card = self._get_ecosystem_context(ecosystem)
        matched_sponsors = self._match_sponsors(sponsors)

        ecosystem_momentum = ecosystem_card["momentum_score"] if ecosystem_card else None

        if matched_sponsors:
            sponsor_predictability = sum(
                s["predictability_score"] for s in matched_sponsors
            ) / len(matched_sponsors)
        else:
            sponsor_predictability = None

        return {
            "ecosystem_context": ecosystem_card,
            "sponsor_cards": matched_sponsors,
            "ecosystem_momentum": ecosystem_momentum,
            "sponsor_predictability": sponsor_predictability
        }

    def query_intelligence_for_opportunity(self, opp_slug: str) -> Dict[str, Any]:
        """
        Step 1: Pull together all historical intelligence for a target opportunity.
        """
        opportunity = self.db.get_opportunity(opp_slug)
        if not opportunity:
            return {"error": f"Opportunity '{opp_slug}' was not found in persistent memory."}

        # ------------------------------------------------------------------- #
        # Step 2: Fetch ecosystem momentum context                            #
        # ------------------------------------------------------------------- #
        ecosystem_card = self._get_ecosystem_context(opportunity.get("ecosystem", ""))

        # ------------------------------------------------------------------- #
        # Step 3: Find matching Sponsor Intelligence Cards                    #
        # ------------------------------------------------------------------- #
        matched_sponsors = self._match_sponsors(opportunity.get("sponsors", []))

        # ------------------------------------------------------------------- #
        # Step 4: Find historical winners from this organizer or event        #
        # ------------------------------------------------------------------- #
        all_winners = self.db.get_all_winners(limit=50)
        organizer = opportunity.get("organizer", "").lower()

        related_winners = [
            winner for winner in all_winners
            if organizer in winner["event_name"].lower() or (
                opportunity.get("id") and winner.get("opportunity_id") == opportunity["id"]
            )
        ]

        return {
            "opportunity": opportunity,
            "ecosystem_context": ecosystem_card,
            "sponsors_intelligence": matched_sponsors,
            "historical_winners": related_winners,
            "system_insights": (
                f"Memory synthesized for {opportunity['name']}: {len(matched_sponsors)} sponsor profiles matched; "
                f"{len(related_winners)} historical winner records analyzed."
            )
        }

    def record_competition_completion(
        self,
        opportunity_id: str,
        winning_projects: List[Dict[str, Any]],
        new_sponsor_notes: Dict[str, str] = None
    ):
        """
        Step 5: Record results after a hackathon finishes so ARGUS remembers
        what worked and gets smarter for the next season.
        """
        for winner in winning_projects:
            winner["opportunity_id"] = opportunity_id
            self.db.insert_winner(winner)

        if new_sponsor_notes:
            for sponsor_slug, note in new_sponsor_notes.items():
                sponsor = self.db.get_sponsor(sponsor_slug)
                if sponsor:
                    existing_prep = sponsor.get("recommended_preparation", "")
                    sponsor["recommended_preparation"] = f"{existing_prep} | Post-event update: {note}"
                    self.db.upsert_sponsor(sponsor)

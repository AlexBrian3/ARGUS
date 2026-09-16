"""
Engine 10 — PERSISTENT MEMORY
Unified knowledge retrieval & historical intelligence interface.
Ensures zero research is discarded after events conclude.
Cross-references new opportunities against historical sponsors, winners, and ecosystems.
"""
from typing import Dict, List, Any, Optional
from brain.db.database import Database


class PersistentMemory:
    def __init__(self, db: Database = None):
        self.db = db or Database()

    def query_intelligence_for_opportunity(self, opp_slug: str) -> Dict[str, Any]:
        """
        Synthesizes complete historical intelligence for any target opportunity:
        - Matched Ecosystem Radar status
        - Historical Sponsor Intelligence Cards
        - Historical Winner Patterns
        - Past Winning Repos & Demos
        """
        opp = self.db.get_opportunity(opp_slug)
        if not opp:
            return {"error": f"Opportunity {opp_slug} not found in persistent memory."}

        # 1. Fetch Ecosystem context
        eco_slug = opp.get("ecosystem", "").lower().split("/")[0].strip()
        ecosystem_card = self.db.get_ecosystem(eco_slug)

        # 2. Fetch matched Sponsor Cards
        sponsor_cards = []
        for sp_name in opp.get("sponsors", []):
            sp_slug = sp_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
            # check direct or partial match
            all_sponsors = self.db.get_all_sponsors()
            for s in all_sponsors:
                if s["slug"] in sp_slug or sp_slug in s["slug"] or s["name"].lower() in sp_name.lower():
                    sponsor_cards.append(s)

        # 3. Fetch past winners for this organizer or ecosystem
        all_winners = self.db.get_all_winners(limit=50)
        related_winners = [
            w for w in all_winners
            if opp["organizer"].lower() in w["event_name"].lower() or (opp.get("id") and w.get("opportunity_id") == opp["id"])
        ]

        return {
            "opportunity": opp,
            "ecosystem_context": ecosystem_card,
            "sponsors_intelligence": sponsor_cards,
            "historical_winners": related_winners,
            "system_insights": (
                f"Memory synthesized for {opp['name']}: {len(sponsor_cards)} sponsor profiles matched; "
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
        Updates persistent memory after a competition ends, making the brain smarter for the next cycle.
        """
        for win in winning_projects:
            win["opportunity_id"] = opportunity_id
            self.db.insert_winner(win)

        if new_sponsor_notes:
            for sp_slug, note in new_sponsor_notes.items():
                sp = self.db.get_sponsor(sp_slug)
                if sp:
                    sp["recommended_preparation"] = f"{sp.get('recommended_preparation', '')} | Post-event: {note}"
                    self.db.upsert_sponsor(sp)

"""
-------------------------------------------------------------------------------
ENGINE 7: EARLY SIGNAL ALERTS
-------------------------------------------------------------------------------
This engine turns intelligence into actionable notifications.

We use 3 strict alert levels:
🔴 LEVEL 1 — FIRST SIGNAL:
   Stealth early evidence (a new GitHub repo, an RFC, or a DevRel teaser)
   before registration is even open.

🟠 LEVEL 2 — CONFIRMED:
   Official event is announced with dates, verified prize pools, and sponsors.

🟢 LEVEL 3 — ACTIONABLE EDGE:
   Unusually attractive, mispriced opportunities where the prize-to-competitor
   ratio is massive and matches your skills.

ALERT SELECTIVITY:
We never spam you! Alerts are cryptographically hashed so you never receive
the same alert twice.
"""

import hashlib
import json
from typing import Dict, List, Any, Optional
from brain.db.database import Database
from brain.config import (
    ACTIONABLE_EDGE_MIN_HACKSCORE,
    ACTIONABLE_EDGE_MIN_SKILL_MATCH
)


class AlertEngine:
    """Classifies opportunities into 3 alert levels and manages deduplication."""

    def __init__(self, db: Database = None):
        self.db = db if db is not None else Database()

    def generate_dedupe_hash(self, alert_level: int, key: str, payload_str: str) -> str:
        """
        Step 1: Create a unique fingerprint (MD5 hash) for each alert.
        If we see this exact fingerprint again, we know it's a duplicate and ignore it.
        """
        raw_text = f"{alert_level}:{key}:{payload_str}"
        return hashlib.md5(raw_text.encode("utf-8")).hexdigest()

    def evaluate_opportunity_alerts(self, opportunity: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Step 2: Check if this opportunity qualifies for an alert.
        Returns the alert dictionary if it's new, or None if it's a duplicate or doesn't qualify.
        """
        hack_score = opportunity.get("hack_score", 0.0)
        skill_match = opportunity.get("skill_match_score", 0.0)
        status = opportunity.get("status", "confirmed")
        name = opportunity.get("name", "")
        slug = opportunity.get("slug", "")

        # ------------------------------------------------------------------- #
        # Check A: Does it qualify as a Level 3 Actionable Edge?              #
        # ------------------------------------------------------------------- #
        # Requires high HackScore (75+) AND high Skill Match (70+)
        is_actionable_edge = (
            hack_score >= ACTIONABLE_EDGE_MIN_HACKSCORE and
            skill_match >= ACTIONABLE_EDGE_MIN_SKILL_MATCH
        )

        if is_actionable_edge:
            deadline = opportunity.get("submission_deadline", "")
            fingerprint = self.generate_dedupe_hash(3, slug, f"{hack_score}:{deadline}")

            expected_competitors = opportunity.get("expected_competitors", 0)
            serious_builders = int(expected_competitors * 0.28)
            prize_ratio = opportunity.get("prize_to_competitor_ratio", 0.0)

            alert = {
                "id": f"alert_edge_{slug}",
                "alert_level": 3,
                "opportunity_id": opportunity.get("id"),
                "title": f"🟢 [LEVEL 3 ACTIONABLE EDGE] {name}",
                "summary": (
                    f"Asymmetric Opportunity Detected. HackScore: {hack_score}/100 | "
                    f"Skill Match: {skill_match}/100. Total Prize: ${opportunity.get('total_prize_usd', 0):,.0f}."
                ),
                "why_mispriced": (
                    f"Expected serious competitors is only ~{serious_builders} builders, "
                    f"giving a prize-to-competitor ratio of ${prize_ratio:,.2f} per serious builder. "
                    f"Tracks and participation bounties give a high probability of taking home capital."
                ),
                "action_items": [
                    "Register immediately to lock spot and claim testnet RPC / builder credits",
                    "Clone hackathon-launchpad boilerplate and wire recommended build direction",
                    f"Prepare key SDKs: {', '.join(opportunity.get('technologies_to_learn', []))}"
                ],
                "what_to_learn_immediately": ", ".join(opportunity.get("technologies_to_learn", [])),
                "should_register_immediately": True,
                "dedupe_hash": fingerprint
            }

            was_inserted = self.db.insert_alert_if_new(alert)
            return alert if was_inserted else None

        # ------------------------------------------------------------------- #
        # Check B: Is this an early Level 1 First Signal?                     #
        # ------------------------------------------------------------------- #
        # If it came from Tier 0 (new repo / RFC) and registration is not open yet:
        is_first_signal = (status == "unconfirmed" or opportunity.get("source_tier") == "Tier 0")

        if is_first_signal:
            fingerprint = self.generate_dedupe_hash(1, slug, "first_signal")
            alert = {
                "id": f"alert_signal_{slug}",
                "alert_level": 1,
                "opportunity_id": opportunity.get("id"),
                "title": f"🔴 [LEVEL 1 FIRST SIGNAL] Emerging Builder Program: {name}",
                "summary": f"Early signal detected via {opportunity.get('source_tier')}. Registration is not yet open.",
                "why_mispriced": "Early preparation window before general developer crowd is aware.",
                "action_items": [
                    "Inspect tracked repos and documentation commits",
                    "Build initial proof-of-concept ahead of official opening"
                ],
                "what_to_learn_immediately": ", ".join(opportunity.get("technologies_to_learn", [])),
                "should_register_immediately": False,
                "dedupe_hash": fingerprint
            }

            was_inserted = self.db.insert_alert_if_new(alert)
            return alert if was_inserted else None

        # ------------------------------------------------------------------- #
        # Check C: Standard Level 2 Confirmed Event                           #
        # ------------------------------------------------------------------- #
        fingerprint = self.generate_dedupe_hash(2, slug, str(opportunity.get("submission_deadline")))
        alert = {
            "id": f"alert_confirmed_{slug}",
            "alert_level": 2,
            "opportunity_id": opportunity.get("id"),
            "title": f"🟠 [LEVEL 2 CONFIRMED] {name}",
            "summary": f"Official opportunity open. HackScore: {hack_score}/100. Prize: ${opportunity.get('total_prize_usd', 0):,.0f}.",
            "why_mispriced": f"Standard market event with {len(opportunity.get('sponsors', []))} verified sponsors.",
            "action_items": [f"Review tracks and bookmark deadline: {opportunity.get('submission_deadline')}"],
            "what_to_learn_immediately": ", ".join(opportunity.get("technologies_to_learn", [])),
            "should_register_immediately": False,
            "dedupe_hash": fingerprint
        }

        was_inserted = self.db.insert_alert_if_new(alert)
        return alert if was_inserted else None

    def scan_and_generate_alerts(self) -> List[Dict[str, Any]]:
        """
        Step 3: Run alert checks across all opportunities stored in the database.
        Returns a list of freshly triggered alerts.
        """
        all_opportunities = self.db.get_all_opportunities(limit=50)
        newly_fired_alerts = []

        for opportunity in all_opportunities:
            alert = self.evaluate_opportunity_alerts(opportunity)
            if alert is not None:
                newly_fired_alerts.append(alert)

        return newly_fired_alerts

    def get_recent_alerts(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Returns the most recent alerts from the database."""
        return self.db.get_recent_alerts(limit=limit)

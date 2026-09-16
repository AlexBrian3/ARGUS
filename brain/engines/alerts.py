"""
Engine 7 — EARLY SIGNAL ALERTS
Implements 3-tier alert classification with strict deduplication:
🔴 LEVEL 1 — FIRST SIGNAL: Stealth early evidence (new repo, RFC, DevRel teaser, grant commit).
🟠 LEVEL 2 — CONFIRMED: Official opportunity with verified prizes, sponsors, deadlines.
🟢 LEVEL 3 — ACTIONABLE EDGE: Asymmetric, mispriced opportunities with unfair skill match.
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
    def __init__(self, db: Database = None):
        self.db = db or Database()

    def generate_dedupe_hash(self, alert_level: int, key: str, payload_str: str) -> str:
        """Generates deterministic MD5 hash to prevent duplicate notifications."""
        raw = f"{alert_level}:{key}:{payload_str}"
        return hashlib.md5(raw.encode("utf-8")).hexdigest()

    def evaluate_opportunity_alerts(self, opp: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Evaluates an opportunity to determine whether to trigger a Level 1, 2, or 3 alert.
        """
        hack_score = opp.get("hack_score", 0.0)
        skill_match = opp.get("skill_match_score", 0.0)
        status = opp.get("status", "confirmed")
        name = opp.get("name", "")
        slug = opp.get("slug", "")

        # 1. Check for Level 3: Actionable Edge
        # High HackScore, High Skill Match, Active/Confirmed
        if hack_score >= ACTIONABLE_EDGE_MIN_HACKSCORE and skill_match >= ACTIONABLE_EDGE_MIN_SKILL_MATCH:
            dedupe_hash = self.generate_dedupe_hash(3, slug, f"{hack_score}:{opp.get('submission_deadline')}")
            alert = {
                "id": f"alert_edge_{slug}",
                "alert_level": 3,
                "opportunity_id": opp.get("id"),
                "title": f"🟢 [LEVEL 3 ACTIONABLE EDGE] {name}",
                "summary": (
                    f"Asymmetric Opportunity Detected. HackScore: {hack_score}/100 | Skill Match: {skill_match}/100. "
                    f"Total Prize: ${opp.get('total_prize_usd', 0):,.0f}."
                ),
                "why_mispriced": (
                    f"Expected serious competitors is only ~{opp.get('expected_competitors', 0) * 0.28:.0f} "
                    f"yielding a prize-to-competitor ratio of ${opp.get('prize_to_competitor_ratio', 0):,.2f} per serious builder. "
                    f"Participation rewards and tracks offer 38-60% probability of taking home capital."
                ),
                "action_items": [
                    "Register immediately to lock spot and claim testnet RPC / builder credits",
                    f"Clone hackathon-launchpad boilerplate and wire recommended build direction",
                    f"Prepare key SDKs: {', '.join(opp.get('technologies_to_learn', []))}"
                ],
                "what_to_learn_immediately": ", ".join(opp.get("technologies_to_learn", [])),
                "should_register_immediately": True,
                "dedupe_hash": dedupe_hash
            }
            inserted = self.db.insert_alert_if_new(alert)
            return alert if inserted else None

        # 2. Check for Level 1: First Signal (Unconfirmed or early signal)
        elif status == "unconfirmed" or opp.get("source_tier") == "Tier 0":
            dedupe_hash = self.generate_dedupe_hash(1, slug, "first_signal")
            alert = {
                "id": f"alert_signal_{slug}",
                "alert_level": 1,
                "opportunity_id": opp.get("id"),
                "title": f"🔴 [LEVEL 1 FIRST SIGNAL] Emerging Builder Program: {name}",
                "summary": f"Early signal detected via {opp.get('source_tier')}. Registration is not yet open.",
                "why_mispriced": "Early preparation window before general developer crowd is aware.",
                "action_items": [
                    "Inspect tracked repos and documentation commits",
                    "Build initial proof-of-concept ahead of official opening"
                ],
                "what_to_learn_immediately": ", ".join(opp.get("technologies_to_learn", [])),
                "should_register_immediately": False,
                "dedupe_hash": dedupe_hash
            }
            inserted = self.db.insert_alert_if_new(alert)
            return alert if inserted else None

        # 3. Level 2: Confirmed Opportunity
        else:
            dedupe_hash = self.generate_dedupe_hash(2, slug, f"{opp.get('submission_deadline')}")
            alert = {
                "id": f"alert_confirmed_{slug}",
                "alert_level": 2,
                "opportunity_id": opp.get("id"),
                "title": f"🟠 [LEVEL 2 CONFIRMED] {name}",
                "summary": f"Official opportunity open. HackScore: {hack_score}/100. Prize: ${opp.get('total_prize_usd', 0):,.0f}.",
                "why_mispriced": f"Standard market event with {len(opp.get('sponsors', []))} verified sponsors.",
                "action_items": ["Review tracks and bookmark deadline: " + str(opp.get("submission_deadline"))],
                "what_to_learn_immediately": ", ".join(opp.get("technologies_to_learn", [])),
                "should_register_immediately": False,
                "dedupe_hash": dedupe_hash
            }
            inserted = self.db.insert_alert_if_new(alert)
            return alert if inserted else None

    def scan_and_generate_alerts(self) -> List[Dict[str, Any]]:
        """
        Runs alert evaluation across all stored opportunities. Returns newly fired alerts.
        """
        opportunities = self.db.get_all_opportunities(limit=50)
        new_alerts = []
        for opp in opportunities:
            alert = self.evaluate_opportunity_alerts(opp)
            if alert:
                new_alerts.append(alert)
        return new_alerts

    def get_recent_alerts(self, limit: int = 20) -> List[Dict[str, Any]]:
        return self.db.get_recent_alerts(limit=limit)

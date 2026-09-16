"""
Engine 1 — OPPORTUNITY SCOUT
Scans across Tier 0, Tier 1, and Tier 2 sources for hackathons, bounties, grants,
accelerators, and builder programs before they become crowded.
"""
from typing import Dict, List, Any
import datetime
from brain.db.database import Database
from brain.engines.scoring import OpportunityScorer
from brain.engines.user_fit import UserFitEngine
from brain.engines.alerts import AlertEngine
from brain.engines.content import SocialContentEngine


class OpportunityScout:
    def __init__(self, db: Database = None):
        self.db = db or Database()
        self.scorer = OpportunityScorer()
        self.user_fit = UserFitEngine()
        self.alert_engine = AlertEngine(self.db)
        self.content_engine = SocialContentEngine(self.db)

    def process_raw_opportunity(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes raw opportunity data from any tier, calculates HackScore, SkillMatch,
        determines alert levels, generates content package if strong, and persists.
        """
        name = raw["name"]
        slug = raw["slug"]
        prize_usd = float(raw.get("total_prize_usd", 0.0))
        expected_comps = int(raw.get("expected_competitors", 500))
        tags = raw.get("tags", [])
        sponsors = raw.get("sponsors", [])
        ecosystem = raw.get("ecosystem", "Multi-chain")

        # 1. Evaluate User Fit
        fit_analysis = self.user_fit.analyze_fit(raw)
        skill_match = fit_analysis["skill_match"]

        # 2. Evaluate HackScore
        scoring_result = self.scorer.calculate_hack_score(
            prize_usd=prize_usd,
            expected_competitors=expected_comps,
            skill_fit_score=skill_match,
            num_tracks_and_bounties=len(raw.get("tracks", [])) or 4,
            has_participation_rewards=bool(raw.get("participation_rewards")),
            is_accelerator_or_vc_backed=("accelerator" in raw.get("type", "").lower() or "seed" in str(raw.get("prize_breakdown", "")).lower())
        )

        hack_score = scoring_result["hack_score"]

        # 3. Determine Alert Level
        if hack_score >= 75.0 and skill_match >= 70.0:
            alert_level = 3 # Actionable Edge
        elif raw.get("source_tier") == "Tier 0" or raw.get("status") == "unconfirmed":
            alert_level = 1 # First Signal
        else:
            alert_level = 2 # Confirmed

        record = {
            "id": raw.get("id", f"opp_{slug}"),
            "name": name,
            "slug": slug,
            "type": raw.get("type", "hackathon"),
            "organizer": raw.get("organizer", "Unknown"),
            "ecosystem": ecosystem,
            "registration_open": raw.get("registration_open", True),
            "registration_deadline": raw.get("registration_deadline", ""),
            "submission_deadline": raw.get("submission_deadline", ""),
            "total_prize_usd": prize_usd,
            "prize_breakdown": raw.get("prize_breakdown", {}),
            "tracks": raw.get("tracks", []),
            "sponsors": sponsors,
            "participation_rewards": raw.get("participation_rewards", ""),
            "expected_competitors": expected_comps,
            "prize_to_competitor_ratio": scoring_result["prize_to_competitor_ratio_est"],
            "prob_placing": scoring_result["prob_placing_est"],
            "prob_any_reward": scoring_result["prob_any_reward_est"],
            "hack_score": hack_score,
            "skill_match_score": skill_match,
            "score_breakdown": scoring_result["breakdown"],
            "alert_level": alert_level,
            "status": raw.get("status", "confirmed"),
            "url": raw.get("url", ""),
            "source_tier": raw.get("source_tier", "Tier 2"),
            "source_url": raw.get("source_url", ""),
            "tags": tags,
            "recommended_build_direction": fit_analysis["recommended_build_direction"],
            "technologies_to_learn": fit_analysis["technologies_to_learn"]
        }

        # Persist to SQLite
        self.db.upsert_opportunity(record)

        # Trigger alerts if criteria met
        self.alert_engine.evaluate_opportunity_alerts(record)

        # Generate Social Content if high conviction
        if hack_score >= 80.0:
            self.content_engine.generate_content_package(record)

        return record

    def run_full_scan(self) -> Dict[str, Any]:
        """
        Executes scout pipeline across all known sources and updates persistent memory.
        """
        all_opps = self.db.get_all_opportunities(limit=100)
        processed = []
        for opp in all_opps:
            res = self.process_raw_opportunity(opp)
            processed.append(res)

        new_alerts = self.alert_engine.scan_and_generate_alerts()

        return {
            "total_opportunities_scanned": len(processed),
            "new_alerts_fired": len(new_alerts),
            "timestamp": datetime.datetime.now().isoformat()
        }

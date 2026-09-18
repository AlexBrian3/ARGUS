"""
-------------------------------------------------------------------------------
ENGINE 1: OPPORTUNITY SCOUT
-------------------------------------------------------------------------------
This is the master scanner that gathers raw signals from all tiers:

- Tier 0: Earliest signals (new GitHub repos, RFCs, DevRel announcements)
- Tier 1: Official sources (Foundation blogs, developer portals, grant pages)
- Tier 2: Major organizers (ETHGlobal, Colosseum, DoraHacks, Devpost)

It normalizes every event, feeds it through all 10 engines, and saves the
resulting intelligence into SQLite memory.
"""

from typing import Dict, List, Any
import datetime
from brain.db.database import Database
from brain.engines.scoring import OpportunityScorer
from brain.engines.user_fit import UserFitEngine
from brain.engines.alerts import AlertEngine
from brain.engines.content import SocialContentEngine
from brain.engines.memory import PersistentMemory


class OpportunityScout:
    """Orchestrates scanning, evaluating, and alerting across all sources."""

    def __init__(self, db: Database = None):
        self.db = db if db is not None else Database()
        self.scorer = OpportunityScorer()
        self.user_fit = UserFitEngine()
        self.alert_engine = AlertEngine(self.db)
        self.content_engine = SocialContentEngine(self.db)
        self.memory = PersistentMemory(self.db)

    def process_raw_opportunity(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes raw event data, runs it through all engines, and stores it in memory.
        """
        name = raw_data["name"]
        slug = raw_data["slug"]
        prize_usd = float(raw_data.get("total_prize_usd", 0.0))
        expected_competitors = int(raw_data.get("expected_competitors", 500))
        tags = raw_data.get("tags", [])
        sponsors = raw_data.get("sponsors", [])
        ecosystem = raw_data.get("ecosystem", "Multi-chain")

        # ------------------------------------------------------------------- #
        # Step 1: Evaluate User Fit (Engine 6)                                #
        # ------------------------------------------------------------------- #
        fit_analysis = self.user_fit.analyze_fit(raw_data)
        skill_match = fit_analysis["skill_match"]

        # ------------------------------------------------------------------- #
        # Step 2: Pull real Sponsor & Ecosystem intelligence (Engine 10)      #
        # ------------------------------------------------------------------- #
        # Looks up this opportunity's actual sponsors and ecosystem in
        # persistent memory, so scoring reflects real predictability and
        # momentum data instead of a flat default for every opportunity.
        memory_context = self.memory.get_context_for_raw_opportunity(ecosystem, sponsors)
        sponsor_predictability = memory_context["sponsor_predictability"]
        ecosystem_momentum = memory_context["ecosystem_momentum"]

        # ------------------------------------------------------------------- #
        # Step 3: Compute HackScore (Engine 5)                                #
        # ------------------------------------------------------------------- #
        num_tracks = len(raw_data.get("tracks", [])) or 4
        has_rewards = bool(raw_data.get("participation_rewards"))
        is_vc_backed = (
            "accelerator" in raw_data.get("type", "").lower() or
            "seed" in str(raw_data.get("prize_breakdown", "")).lower()
        )

        scoring_kwargs = dict(
            prize_usd=prize_usd,
            expected_competitors=expected_competitors,
            skill_fit_score=skill_match,
            num_tracks_and_bounties=num_tracks,
            has_participation_rewards=has_rewards,
            is_accelerator_or_vc_backed=is_vc_backed
        )
        # Only override the defaults when memory actually has data for this
        # opportunity's sponsors/ecosystem; otherwise let calculate_hack_score
        # fall back to its own defaults.
        if sponsor_predictability is not None:
            scoring_kwargs["sponsor_predictability"] = sponsor_predictability
        if ecosystem_momentum is not None:
            scoring_kwargs["ecosystem_momentum"] = ecosystem_momentum

        scoring_result = self.scorer.calculate_hack_score(**scoring_kwargs)

        hack_score = scoring_result["hack_score"]

        # ------------------------------------------------------------------- #
        # Step 4: Determine Alert Level (Engine 7)                            #
        # ------------------------------------------------------------------- #
        if hack_score >= 75.0 and skill_match >= 70.0:
            alert_level = 3  # Level 3: Actionable Edge!
        elif raw_data.get("source_tier") == "Tier 0" or raw_data.get("status") == "unconfirmed":
            alert_level = 1  # Level 1: First Signal
        else:
            alert_level = 2  # Level 2: Confirmed

        # Package into clean structured record
        clean_record = {
            "id": raw_data.get("id", f"opp_{slug}"),
            "name": name,
            "slug": slug,
            "type": raw_data.get("type", "hackathon"),
            "organizer": raw_data.get("organizer", "Unknown"),
            "ecosystem": ecosystem,
            "registration_open": raw_data.get("registration_open", True),
            "registration_deadline": raw_data.get("registration_deadline", ""),
            "submission_deadline": raw_data.get("submission_deadline", ""),
            "total_prize_usd": prize_usd,
            "prize_breakdown": raw_data.get("prize_breakdown", {}),
            "tracks": raw_data.get("tracks", []),
            "sponsors": sponsors,
            "participation_rewards": raw_data.get("participation_rewards", ""),
            "expected_competitors": expected_competitors,
            "prize_to_competitor_ratio": scoring_result["prize_to_competitor_ratio_est"],
            "prob_placing": scoring_result["prob_placing_est"],
            "prob_any_reward": scoring_result["prob_any_reward_est"],
            "hack_score": hack_score,
            "skill_match_score": skill_match,
            "score_breakdown": scoring_result["breakdown"],
            "alert_level": alert_level,
            "status": raw_data.get("status", "confirmed"),
            "url": raw_data.get("url", ""),
            "source_tier": raw_data.get("source_tier", "Tier 2"),
            "source_url": raw_data.get("source_url", ""),
            "tags": tags,
            "recommended_build_direction": fit_analysis["recommended_build_direction"],
            "technologies_to_learn": fit_analysis["technologies_to_learn"]
        }

        # ------------------------------------------------------------------- #
        # Step 5: Save to SQLite Database (Engine 10)                         #
        # ------------------------------------------------------------------- #
        self.db.upsert_opportunity(clean_record)

        # ------------------------------------------------------------------- #
        # Step 6: Check Alerts & Draft Content if High Score                  #
        # ------------------------------------------------------------------- #
        self.alert_engine.evaluate_opportunity_alerts(clean_record)

        if hack_score >= 80.0:
            self.content_engine.generate_content_package(clean_record)

        return clean_record

    def run_full_scan(self) -> Dict[str, Any]:
        """
        Runs the complete intelligence cycle across all stored opportunities.
        """
        all_opportunities = self.db.get_all_opportunities(limit=100)
        processed_list = []

        for opp in all_opportunities:
            processed = self.process_raw_opportunity(opp)
            processed_list.append(processed)

        new_alerts = self.alert_engine.scan_and_generate_alerts()

        return {
            "total_opportunities_scanned": len(processed_list),
            "new_alerts_fired": len(new_alerts),
            "timestamp": datetime.datetime.now().isoformat()
        }

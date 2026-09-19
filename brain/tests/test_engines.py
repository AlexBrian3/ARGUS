"""
Unit tests for ARGUS database and intelligence engines.
"""
import unittest
from pathlib import Path
from brain.db.database import Database
from brain.engines.radar import EcosystemRadar
from brain.engines.scoring import OpportunityScorer
from brain.engines.user_fit import UserFitEngine
from brain.engines.sponsor import SponsorIntelligence
from brain.engines.alerts import AlertEngine
from brain.engines.content import SocialContentEngine
from brain.engines.winners import WinnerAnalyzer
from brain.engines.benefits import BenefitsTracker
from brain.engines.jobs import JobsScout

TEST_DB_PATH = Path(__file__).parent / "test_brain.db"


class TestBuilderBrain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if TEST_DB_PATH.exists():
            TEST_DB_PATH.unlink()
        cls.db = Database(db_path=TEST_DB_PATH)
        # Seed test data
        from brain.db.seed import seed_database
        seed_database(cls.db)

    @classmethod
    def tearDownClass(cls):
        if TEST_DB_PATH.exists():
            try:
                TEST_DB_PATH.unlink()
            except Exception:
                pass

    def test_database_persistence(self):
        ecosystems = self.db.get_all_ecosystems()
        self.assertGreaterEqual(len(ecosystems), 50)
        solana = self.db.get_ecosystem("solana")
        self.assertIsNotNone(solana)
        self.assertEqual(solana["name"], "Solana")
        self.assertEqual(solana.get("maturity_stage"), "established")
        self.assertIn("developer_programs", solana["breakdown_scores"])

    def test_ecosystem_radar(self):
        radar = EcosystemRadar(self.db)
        score, breakdown = radar.calculate_momentum_score({
            "developer_programs": 20.0,
            "hackathons_and_grants": 18.0,
            "dev_activity_acceleration": 14.0,
            "sdk_product_launches": 9.0,
            "sponsor_activity": 9.0,
            "social_discussion": 9.0,
            "funding_activity": 4.0,
            "competition_opportunity": 8.0
        })
        self.assertGreaterEqual(score, 85.0)
        self.assertEqual(radar.determine_trajectory(90.0, 80.0), "↑")
        self.assertEqual(radar.determine_trajectory(75.0, 85.0), "↓")
        self.assertEqual(radar.determine_trajectory(80.0, 80.0), "→")

    def test_ecosystem_discovery_engine_11(self):
        """Engine 11: Early ecosystem discovery, stage filtering, and promotion triggers."""
        radar = EcosystemRadar(self.db)
        watchlist = radar.get_ecosystems_by_stage("watchlist")
        emerging = radar.get_ecosystems_by_stage("emerging")
        established = radar.get_ecosystems_by_stage("established")

        self.assertGreaterEqual(len(watchlist), 5)
        self.assertGreaterEqual(len(emerging), 10)
        self.assertGreaterEqual(len(established), 15)

        # Discover a new stealth ecosystem
        discovered = radar.discover_new_ecosystem(
            name="Quantum L3 Testnet",
            category="Quantum Proofs",
            notes="Stealth cryptographic execution environment",
            initial_momentum=50.0
        )
        self.assertEqual(discovered["maturity_stage"], "watchlist")
        self.assertEqual(discovered["slug"], "quantum-l3-testnet")

        # Promote to emerging (momentum >= 70)
        promoted_emerging = radar.update_stage_on_momentum("quantum-l3-testnet", 72.0)
        self.assertEqual(promoted_emerging, "emerging")
        eco = self.db.get_ecosystem("quantum-l3-testnet")
        self.assertEqual(eco["maturity_stage"], "emerging")

        # Promote to established (momentum >= 85)
        promoted_established = radar.update_stage_on_momentum("quantum-l3-testnet", 88.0)
        self.assertEqual(promoted_established, "established")
        eco = self.db.get_ecosystem("quantum-l3-testnet")
        self.assertEqual(eco["maturity_stage"], "established")

    def test_benefits_tracker_engine_12(self):
        """Engine 12: Standing benefits, rolling grants, gas credits, and user fit scoring."""
        tracker = BenefitsTracker(self.db)
        benefits = tracker.get_ranked_benefits()
        self.assertGreaterEqual(len(benefits), 10)

        # Check user fit score computation
        top_benefit = benefits[0]
        self.assertIn("user_fit_score", top_benefit)
        self.assertGreaterEqual(top_benefit["user_fit_score"], 50.0)

        # Query benefits by ecosystem
        sol_benefits = tracker.get_benefits_by_ecosystem("Solana")
        self.assertGreaterEqual(len(sol_benefits), 1)

        # Upsert a new benefit
        new_b = tracker.upsert_benefit_record({
            "title": "Custom Test Fellowship",
            "slug": "custom-test-fellowship",
            "ecosystem": "Arbitrum",
            "category": "fellowship",
            "amount_usd": 15000,
            "description": "Fellowship for AI agent and Python developers building DeFi",
            "eligibility": "Open to solo builders"
        })
        self.assertEqual(new_b["slug"], "custom-test-fellowship")
        fetched = self.db.get_benefit("custom-test-fellowship")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["amount_usd"], 15000)

    def test_jobs_scout_engine_13(self):
        """Engine 13: High-relevance jobs scout, 24h freshness, and Level 1 alerts."""
        scout = JobsScout(self.db)
        all_jobs = scout.get_all_ranked_listings()
        self.assertGreaterEqual(len(all_jobs), 5)

        # Test fresh listings
        fresh = scout.get_fresh_listings(hours=24)
        self.assertGreaterEqual(len(fresh), 1)
        for f in fresh:
            self.assertTrue(f["is_fresh"])

        # Test skill matching
        test_job = {
            "title": "Senior AI Agent Protocol Engineer",
            "company": "Autonomous Labs",
            "ecosystem": "Solana",
            "description": "Building autonomous AI agents using Python, FastAPI, Solana smart contracts and Pyth oracle integrations.",
            "compensation": "$160k - $210k + tokens",
            "apply_url": "https://example.com/jobs/ai-agent-engineer"
        }
        processed = scout.process_raw_listing(test_job)
        self.assertGreaterEqual(processed["skill_match_score"], 80.0)

        # Test scan_and_alert_fresh_jobs generates alerts and marks alert sent
        alerts = scout.scan_and_alert_fresh_jobs()
        self.assertGreaterEqual(len(alerts), 1)

        # Scanning again should not send duplicate alerts
        repeat_alerts = scout.scan_and_alert_fresh_jobs()
        self.assertEqual(len(repeat_alerts), 0)

    def test_opportunity_scorer(self):
        scorer = OpportunityScorer()
        res = scorer.calculate_hack_score(
            prize_usd=3340000.0,
            expected_competitors=2200,
            skill_fit_score=92.0,
            num_tracks_and_bounties=5,
            has_participation_rewards=True,
            is_accelerator_or_vc_backed=True
        )
        self.assertGreaterEqual(res["hack_score"], 80.0)
        self.assertGreater(res["prize_to_competitor_ratio_est"], 1000.0)
        self.assertGreater(res["prob_any_reward_est"], 0.20)
        self.assertIn("competition_attractiveness", res["breakdown"])

    def test_user_fit_engine(self):
        fit_engine = UserFitEngine()
        match = fit_engine.evaluate_skill_match(["AI Agents", "FastAPI", "Python", "Solana"])
        self.assertGreaterEqual(match, 85.0)

        analysis = fit_engine.analyze_fit({
            "name": "Colosseum World's Fair",
            "ecosystem": "Solana",
            "tags": ["AI Agents", "Payments", "Solana"],
            "sponsors": ["Solana Foundation"]
        })
        self.assertIn("FastAPI", analysis["reusable_code"][0])
        
        # Test strengthened build direction
        direction = analysis["recommended_build_direction"]
        self.assertIsInstance(direction, dict)
        self.assertIn("what_everyone_else_will_build", direction)
        self.assertIn("your_unfair_advantage_build", direction)
        self.assertIn("x402", direction["your_unfair_advantage_build"])
        self.assertTrue(len(direction["what_everyone_else_will_build"]) > 20)

    def test_sponsor_intelligence(self):
        sponsor_engine = SponsorIntelligence(self.db)
        card = sponsor_engine.get_sponsor_card("world")
        self.assertIsNotNone(card)
        self.assertGreaterEqual(card["predictability_score"], 85.0)
        self.assertTrue(any("MiniKit" in t for t in card["recurring_technologies"]))

    def test_alert_engine_deduplication(self):
        alert_engine = AlertEngine(self.db)
        alerts = alert_engine.scan_and_generate_alerts()
        self.assertGreaterEqual(len(alerts), 1)

        # Scanning again immediately should not duplicate alerts
        second_scan = alert_engine.scan_and_generate_alerts()
        self.assertEqual(len(second_scan), 0)

    def test_social_content_generation(self):
        content_engine = SocialContentEngine(self.db)
        opp = self.db.get_opportunity("colosseum-crypto-worlds-fair-2026")
        self.assertIsNotNone(opp)
        pkg = content_engine.generate_content_package(opp)
        self.assertGreaterEqual(pkg["content_potential_score"], 80.0)
        self.assertGreaterEqual(len(pkg["x_thread"]), 4)
        self.assertIn("Hook", pkg["tiktok_reels_script"].title())

    def test_winner_analyzer(self):
        analyzer = WinnerAnalyzer(self.db)
        res = analyzer.analyze_event_patterns()
        self.assertGreaterEqual(res["total_analyzed"], 1)
        self.assertIn("underexplored_ideas", res)


if __name__ == "__main__":
    unittest.main()

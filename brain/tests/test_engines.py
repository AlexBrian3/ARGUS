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
        self.assertGreaterEqual(len(ecosystems), 5)
        solana = self.db.get_ecosystem("solana")
        self.assertIsNotNone(solana)
        self.assertEqual(solana["name"], "Solana")
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
        self.assertIn("x402", analysis["recommended_build_direction"])

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

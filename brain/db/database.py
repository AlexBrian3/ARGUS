"""
Database manager for ARGUS (Engine 10: Persistent Memory).
Handles SQLite connection, schema migrations, and relational queries.
"""
import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from brain.config import DB_PATH, USER_PROFILE

SCHEMA_FILE = Path(__file__).parent / "schema.sql"


class Database:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self):
        """Initialize tables using schema.sql and populate default user profile if empty."""
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        with self.get_connection() as conn:
            conn.executescript(schema_sql)

            # Check if default user profile exists
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM user_profiles WHERE id = 'default'")
            if not cursor.fetchone():
                cursor.execute(
                    """
                    INSERT INTO user_profiles (id, role, skills, reusable_assets, focus_areas)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        "default",
                        USER_PROFILE["name"],
                        json.dumps(USER_PROFILE["primary_skills"]),
                        json.dumps(USER_PROFILE["reusable_assets"]),
                        json.dumps(USER_PROFILE["target_focus_areas"])
                    )
                )
            conn.commit()

    # --- Ecosystems (Engine 2) ---
    def upsert_ecosystem(self, data: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO ecosystems (slug, name, category, momentum_score, momentum_trajectory, breakdown_scores, tracked_repos, notes, last_updated)
                VALUES (:slug, :name, :category, :momentum_score, :momentum_trajectory, :breakdown_scores, :tracked_repos, :notes, CURRENT_TIMESTAMP)
                ON CONFLICT(slug) DO UPDATE SET
                    name=excluded.name,
                    category=excluded.category,
                    momentum_score=excluded.momentum_score,
                    momentum_trajectory=excluded.momentum_trajectory,
                    breakdown_scores=excluded.breakdown_scores,
                    tracked_repos=excluded.tracked_repos,
                    notes=excluded.notes,
                    last_updated=CURRENT_TIMESTAMP
                """,
                {
                    "slug": data["slug"],
                    "name": data["name"],
                    "category": data.get("category", "L1"),
                    "momentum_score": float(data.get("momentum_score", 0.0)),
                    "momentum_trajectory": data.get("momentum_trajectory", "→"),
                    "breakdown_scores": json.dumps(data.get("breakdown_scores", {})),
                    "tracked_repos": json.dumps(data.get("tracked_repos", [])),
                    "notes": data.get("notes", "")
                }
            )

    def get_all_ecosystems(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ecosystems ORDER BY momentum_score DESC")
            rows = cursor.fetchall()
            result = []
            for r in rows:
                item = dict(r)
                item["breakdown_scores"] = json.loads(item["breakdown_scores"] or "{}")
                item["tracked_repos"] = json.loads(item["tracked_repos"] or "[]")
                result.append(item)
            return result

    def get_ecosystem(self, slug: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ecosystems WHERE slug = ?", (slug,))
            row = cursor.fetchone()
            if not row:
                return None
            item = dict(row)
            item["breakdown_scores"] = json.loads(item["breakdown_scores"] or "{}")
            item["tracked_repos"] = json.loads(item["tracked_repos"] or "[]")
            return item

    # --- Sponsors (Engine 3) ---
    def upsert_sponsor(self, data: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO sponsors (
                    slug, name, ecosystem, technology, predictability_score, upcoming_likelihood,
                    previous_hackathons, prize_amounts_total, tracks, bounties, recurring_technologies,
                    recurring_bounty_categories, common_winning_product_types, features_frequently_used,
                    features_rarely_used, oversaturated_ideas, underserved_ideas, integration_difficulty,
                    documentation_quality, typical_prize_distribution, historical_participation_rewards,
                    repeat_sponsorship_frequency, recommended_preparation, last_updated
                ) VALUES (
                    :slug, :name, :ecosystem, :technology, :predictability_score, :upcoming_likelihood,
                    :previous_hackathons, :prize_amounts_total, :tracks, :bounties, :recurring_technologies,
                    :recurring_bounty_categories, :common_winning_product_types, :features_frequently_used,
                    :features_rarely_used, :oversaturated_ideas, :underserved_ideas, :integration_difficulty,
                    :documentation_quality, :typical_prize_distribution, :historical_participation_rewards,
                    :repeat_sponsorship_frequency, :recommended_preparation, CURRENT_TIMESTAMP
                ) ON CONFLICT(slug) DO UPDATE SET
                    name=excluded.name,
                    ecosystem=excluded.ecosystem,
                    technology=excluded.technology,
                    predictability_score=excluded.predictability_score,
                    upcoming_likelihood=excluded.upcoming_likelihood,
                    previous_hackathons=excluded.previous_hackathons,
                    prize_amounts_total=excluded.prize_amounts_total,
                    tracks=excluded.tracks,
                    bounties=excluded.bounties,
                    recurring_technologies=excluded.recurring_technologies,
                    recurring_bounty_categories=excluded.recurring_bounty_categories,
                    common_winning_product_types=excluded.common_winning_product_types,
                    features_frequently_used=excluded.features_frequently_used,
                    features_rarely_used=excluded.features_rarely_used,
                    oversaturated_ideas=excluded.oversaturated_ideas,
                    underserved_ideas=excluded.underserved_ideas,
                    integration_difficulty=excluded.integration_difficulty,
                    documentation_quality=excluded.documentation_quality,
                    typical_prize_distribution=excluded.typical_prize_distribution,
                    historical_participation_rewards=excluded.historical_participation_rewards,
                    repeat_sponsorship_frequency=excluded.repeat_sponsorship_frequency,
                    recommended_preparation=excluded.recommended_preparation,
                    last_updated=CURRENT_TIMESTAMP
                """,
                {
                    "slug": data["slug"],
                    "name": data["name"],
                    "ecosystem": data["ecosystem"],
                    "technology": data.get("technology", ""),
                    "predictability_score": float(data.get("predictability_score", 0.0)),
                    "upcoming_likelihood": float(data.get("upcoming_likelihood", 0.0)),
                    "previous_hackathons": json.dumps(data.get("previous_hackathons", [])),
                    "prize_amounts_total": float(data.get("prize_amounts_total", 0.0)),
                    "tracks": json.dumps(data.get("tracks", [])),
                    "bounties": json.dumps(data.get("bounties", [])),
                    "recurring_technologies": json.dumps(data.get("recurring_technologies", [])),
                    "recurring_bounty_categories": json.dumps(data.get("recurring_bounty_categories", [])),
                    "common_winning_product_types": json.dumps(data.get("common_winning_product_types", [])),
                    "features_frequently_used": json.dumps(data.get("features_frequently_used", [])),
                    "features_rarely_used": json.dumps(data.get("features_rarely_used", [])),
                    "oversaturated_ideas": json.dumps(data.get("oversaturated_ideas", [])),
                    "underserved_ideas": json.dumps(data.get("underserved_ideas", [])),
                    "integration_difficulty": data.get("integration_difficulty", "Medium"),
                    "documentation_quality": data.get("documentation_quality", "Good"),
                    "typical_prize_distribution": data.get("typical_prize_distribution", ""),
                    "historical_participation_rewards": data.get("historical_participation_rewards", ""),
                    "repeat_sponsorship_frequency": data.get("repeat_sponsorship_frequency", ""),
                    "recommended_preparation": data.get("recommended_preparation", "")
                }
            )

    def get_all_sponsors(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sponsors ORDER BY predictability_score DESC")
            rows = cursor.fetchall()
            result = []
            for r in rows:
                item = dict(r)
                for json_col in [
                    "previous_hackathons", "tracks", "bounties", "recurring_technologies",
                    "recurring_bounty_categories", "common_winning_product_types",
                    "features_frequently_used", "features_rarely_used",
                    "oversaturated_ideas", "underserved_ideas"
                ]:
                    item[json_col] = json.loads(item[json_col] or "[]")
                result.append(item)
            return result

    def get_sponsor(self, slug: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sponsors WHERE slug = ?", (slug,))
            row = cursor.fetchone()
            if not row:
                return None
            item = dict(row)
            for json_col in [
                "previous_hackathons", "tracks", "bounties", "recurring_technologies",
                "recurring_bounty_categories", "common_winning_product_types",
                "features_frequently_used", "features_rarely_used",
                "oversaturated_ideas", "underserved_ideas"
            ]:
                item[json_col] = json.loads(item[json_col] or "[]")
            return item

    # --- Opportunities (Engine 1, 5, 6) ---
    def upsert_opportunity(self, data: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO opportunities (
                    id, name, slug, type, organizer, ecosystem, registration_open,
                    registration_deadline, submission_deadline, total_prize_usd, prize_breakdown,
                    tracks, sponsors, participation_rewards, expected_competitors,
                    prize_to_competitor_ratio, prob_placing, prob_any_reward, hack_score,
                    skill_match_score, score_breakdown, alert_level, status, url,
                    source_tier, source_url, tags, recommended_build_direction,
                    technologies_to_learn, updated_at
                ) VALUES (
                    :id, :name, :slug, :type, :organizer, :ecosystem, :registration_open,
                    :registration_deadline, :submission_deadline, :total_prize_usd, :prize_breakdown,
                    :tracks, :sponsors, :participation_rewards, :expected_competitors,
                    :prize_to_competitor_ratio, :prob_placing, :prob_any_reward, :hack_score,
                    :skill_match_score, :score_breakdown, :alert_level, :status, :url,
                    :source_tier, :source_url, :tags, :recommended_build_direction,
                    :technologies_to_learn, CURRENT_TIMESTAMP
                ) ON CONFLICT(slug) DO UPDATE SET
                    name=excluded.name,
                    type=excluded.type,
                    organizer=excluded.organizer,
                    ecosystem=excluded.ecosystem,
                    registration_open=excluded.registration_open,
                    registration_deadline=excluded.registration_deadline,
                    submission_deadline=excluded.submission_deadline,
                    total_prize_usd=excluded.total_prize_usd,
                    prize_breakdown=excluded.prize_breakdown,
                    tracks=excluded.tracks,
                    sponsors=excluded.sponsors,
                    participation_rewards=excluded.participation_rewards,
                    expected_competitors=excluded.expected_competitors,
                    prize_to_competitor_ratio=excluded.prize_to_competitor_ratio,
                    prob_placing=excluded.prob_placing,
                    prob_any_reward=excluded.prob_any_reward,
                    hack_score=excluded.hack_score,
                    skill_match_score=excluded.skill_match_score,
                    score_breakdown=excluded.score_breakdown,
                    alert_level=excluded.alert_level,
                    status=excluded.status,
                    url=excluded.url,
                    source_tier=excluded.source_tier,
                    source_url=excluded.source_url,
                    tags=excluded.tags,
                    recommended_build_direction=excluded.recommended_build_direction,
                    technologies_to_learn=excluded.technologies_to_learn,
                    updated_at=CURRENT_TIMESTAMP
                """,
                {
                    "id": data["id"],
                    "name": data["name"],
                    "slug": data["slug"],
                    "type": data.get("type", "hackathon"),
                    "organizer": data.get("organizer", "Unknown"),
                    "ecosystem": data.get("ecosystem", "Multi-chain"),
                    "registration_open": 1 if data.get("registration_open", True) else 0,
                    "registration_deadline": data.get("registration_deadline", ""),
                    "submission_deadline": data.get("submission_deadline", ""),
                    "total_prize_usd": float(data.get("total_prize_usd", 0.0)),
                    "prize_breakdown": json.dumps(data.get("prize_breakdown", {})),
                    "tracks": json.dumps(data.get("tracks", [])),
                    "sponsors": json.dumps(data.get("sponsors", [])),
                    "participation_rewards": data.get("participation_rewards", ""),
                    "expected_competitors": int(data.get("expected_competitors", 0)),
                    "prize_to_competitor_ratio": float(data.get("prize_to_competitor_ratio", 0.0)),
                    "prob_placing": float(data.get("prob_placing", 0.0)),
                    "prob_any_reward": float(data.get("prob_any_reward", 0.0)),
                    "hack_score": float(data.get("hack_score", 0.0)),
                    "skill_match_score": float(data.get("skill_match_score", 0.0)),
                    "score_breakdown": json.dumps(data.get("score_breakdown", {})),
                    "alert_level": int(data.get("alert_level", 2)),
                    "status": data.get("status", "confirmed"),
                    "url": data.get("url", ""),
                    "source_tier": data.get("source_tier", "Tier 2"),
                    "source_url": data.get("source_url", ""),
                    "tags": json.dumps(data.get("tags", [])),
                    "recommended_build_direction": data.get("recommended_build_direction", ""),
                    "technologies_to_learn": json.dumps(data.get("technologies_to_learn", []))
                }
            )

    def get_all_opportunities(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM opportunities ORDER BY hack_score DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            result = []
            for r in rows:
                item = dict(r)
                for json_col in ["prize_breakdown", "tracks", "sponsors", "score_breakdown", "tags", "technologies_to_learn"]:
                    item[json_col] = json.loads(item[json_col] or ("{}" if "breakdown" in json_col else "[]"))
                result.append(item)
            return result

    def get_opportunity(self, slug: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM opportunities WHERE slug = ? OR id = ?", (slug, slug))
            row = cursor.fetchone()
            if not row:
                return None
            item = dict(row)
            for json_col in ["prize_breakdown", "tracks", "sponsors", "score_breakdown", "tags", "technologies_to_learn"]:
                item[json_col] = json.loads(item[json_col] or ("{}" if "breakdown" in json_col else "[]"))
            return item

    # --- Winners (Engine 4) ---
    def insert_winner(self, data: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO winners (
                    id, opportunity_id, event_name, project_name, category, problem_solved,
                    product_category, infra_vs_consumer, frontend_quality, ux_quality,
                    technical_depth, sponsor_integration_depth, originality, demo_quality,
                    github_quality, number_of_integrations, ai_usage, privacy_usage,
                    financial_use_case, judges, prize_won, repo_url, demo_url,
                    winning_patterns, losing_patterns_identified, oversaturated_category
                ) VALUES (
                    :id, :opportunity_id, :event_name, :project_name, :category, :problem_solved,
                    :product_category, :infra_vs_consumer, :frontend_quality, :ux_quality,
                    :technical_depth, :sponsor_integration_depth, :originality, :demo_quality,
                    :github_quality, :number_of_integrations, :ai_usage, :privacy_usage,
                    :financial_use_case, :judges, :prize_won, :repo_url, :demo_url,
                    :winning_patterns, :losing_patterns_identified, :oversaturated_category
                ) ON CONFLICT(id) DO UPDATE SET
                    prize_won=excluded.prize_won,
                    winning_patterns=excluded.winning_patterns,
                    losing_patterns_identified=excluded.losing_patterns_identified
                """,
                {
                    "id": data["id"],
                    "opportunity_id": data.get("opportunity_id"),
                    "event_name": data["event_name"],
                    "project_name": data["project_name"],
                    "category": data.get("category", "General"),
                    "problem_solved": data.get("problem_solved", ""),
                    "product_category": data.get("product_category", "infra"),
                    "infra_vs_consumer": data.get("infra_vs_consumer", "Hybrid"),
                    "frontend_quality": data.get("frontend_quality", "High"),
                    "ux_quality": data.get("ux_quality", "High"),
                    "technical_depth": data.get("technical_depth", "High"),
                    "sponsor_integration_depth": data.get("sponsor_integration_depth", "Deep"),
                    "originality": data.get("originality", "High"),
                    "demo_quality": data.get("demo_quality", "High"),
                    "github_quality": data.get("github_quality", "High"),
                    "number_of_integrations": int(data.get("number_of_integrations", 1)),
                    "ai_usage": 1 if data.get("ai_usage", False) else 0,
                    "privacy_usage": 1 if data.get("privacy_usage", False) else 0,
                    "financial_use_case": 1 if data.get("financial_use_case", False) else 0,
                    "judges": data.get("judges", ""),
                    "prize_won": data.get("prize_won", ""),
                    "repo_url": data.get("repo_url", ""),
                    "demo_url": data.get("demo_url", ""),
                    "winning_patterns": data.get("winning_patterns", ""),
                    "losing_patterns_identified": data.get("losing_patterns_identified", ""),
                    "oversaturated_category": 1 if data.get("oversaturated_category", False) else 0
                }
            )

    def get_all_winners(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM winners ORDER BY event_name, prize_won LIMIT ?", (limit,))
            return [dict(r) for r in cursor.fetchall()]

    # --- Alerts (Engine 7) ---
    def insert_alert_if_new(self, alert_data: Dict[str, Any]) -> bool:
        """Insert alert if dedupe_hash does not exist. Returns True if inserted, False if duplicate."""
        with self.get_connection() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO alerts (
                        id, alert_level, opportunity_id, title, summary, why_mispriced,
                        action_items, what_to_learn_immediately, should_register_immediately,
                        dedupe_hash, sent_at
                    ) VALUES (
                        :id, :alert_level, :opportunity_id, :title, :summary, :why_mispriced,
                        :action_items, :what_to_learn_immediately, :should_register_immediately,
                        :dedupe_hash, CURRENT_TIMESTAMP
                    )
                    """,
                    {
                        "id": alert_data["id"],
                        "alert_level": int(alert_data["alert_level"]),
                        "opportunity_id": alert_data.get("opportunity_id"),
                        "title": alert_data["title"],
                        "summary": alert_data["summary"],
                        "why_mispriced": alert_data.get("why_mispriced", ""),
                        "action_items": json.dumps(alert_data.get("action_items", [])),
                        "what_to_learn_immediately": alert_data.get("what_to_learn_immediately", ""),
                        "should_register_immediately": 1 if alert_data.get("should_register_immediately", False) else 0,
                        "dedupe_hash": alert_data["dedupe_hash"]
                    }
                )
                return True
            except sqlite3.IntegrityError:
                return False

    def get_recent_alerts(self, limit: int = 20) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alerts ORDER BY sent_at DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            result = []
            for r in rows:
                item = dict(r)
                item["action_items"] = json.loads(item["action_items"] or "[]")
                result.append(item)
            return result

    # --- Content Opportunities (Engine 8) ---
    def upsert_content_opportunity(self, data: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO content_opportunities (
                    id, opportunity_id, title, topic, angle, content_potential_score,
                    novelty, timeliness, usefulness, dev_interest, discussion_potential,
                    search_interest, proof_data, x_thread, tiktok_reels_script,
                    yt_shorts_script, linkedin_post, created_at
                ) VALUES (
                    :id, :opportunity_id, :title, :topic, :angle, :content_potential_score,
                    :novelty, :timeliness, :usefulness, :dev_interest, :discussion_potential,
                    :search_interest, :proof_data, :x_thread, :tiktok_reels_script,
                    :yt_shorts_script, :linkedin_post, CURRENT_TIMESTAMP
                ) ON CONFLICT(id) DO UPDATE SET
                    title=excluded.title,
                    content_potential_score=excluded.content_potential_score,
                    x_thread=excluded.x_thread,
                    tiktok_reels_script=excluded.tiktok_reels_script,
                    yt_shorts_script=excluded.yt_shorts_script,
                    linkedin_post=excluded.linkedin_post
                """,
                {
                    "id": data["id"],
                    "opportunity_id": data.get("opportunity_id"),
                    "title": data["title"],
                    "topic": data["topic"],
                    "angle": data["angle"],
                    "content_potential_score": float(data.get("content_potential_score", 0.0)),
                    "novelty": float(data.get("novelty", 0.0)),
                    "timeliness": float(data.get("timeliness", 0.0)),
                    "usefulness": float(data.get("usefulness", 0.0)),
                    "dev_interest": float(data.get("dev_interest", 0.0)),
                    "discussion_potential": float(data.get("discussion_potential", 0.0)),
                    "search_interest": float(data.get("search_interest", 0.0)),
                    "proof_data": data.get("proof_data", ""),
                    "x_thread": json.dumps(data.get("x_thread", [])),
                    "tiktok_reels_script": data.get("tiktok_reels_script", ""),
                    "yt_shorts_script": data.get("yt_shorts_script", ""),
                    "linkedin_post": data.get("linkedin_post", "")
                }
            )

    def get_all_content_opportunities(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM content_opportunities ORDER BY content_potential_score DESC")
            rows = cursor.fetchall()
            result = []
            for r in rows:
                item = dict(r)
                item["x_thread"] = json.loads(item["x_thread"] or "[]")
                result.append(item)
            return result

    # --- Trends (Engine 9) ---
    def upsert_trend(self, data: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO trends (
                    id, narrative_name, category, discussion_velocity, repository_growth,
                    grants_moving, description, key_ecosystems, actionable_implications, last_updated
                ) VALUES (
                    :id, :narrative_name, :category, :discussion_velocity, :repository_growth,
                    :grants_moving, :description, :key_ecosystems, :actionable_implications, CURRENT_TIMESTAMP
                ) ON CONFLICT(narrative_name) DO UPDATE SET
                    discussion_velocity=excluded.discussion_velocity,
                    repository_growth=excluded.repository_growth,
                    grants_moving=excluded.grants_moving,
                    description=excluded.description,
                    key_ecosystems=excluded.key_ecosystems,
                    actionable_implications=excluded.actionable_implications,
                    last_updated=CURRENT_TIMESTAMP
                """,
                {
                    "id": data["id"],
                    "narrative_name": data["narrative_name"],
                    "category": data.get("category", "General"),
                    "discussion_velocity": float(data.get("discussion_velocity", 0.0)),
                    "repository_growth": float(data.get("repository_growth", 0.0)),
                    "grants_moving": float(data.get("grants_moving", 0.0)),
                    "description": data.get("description", ""),
                    "key_ecosystems": json.dumps(data.get("key_ecosystems", [])),
                    "actionable_implications": data.get("actionable_implications", "")
                }
            )

    def get_all_trends(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM trends ORDER BY (discussion_velocity + repository_growth + grants_moving) DESC")
            rows = cursor.fetchall()
            result = []
            for r in rows:
                item = dict(r)
                item["key_ecosystems"] = json.loads(item["key_ecosystems"] or "[]")
                result.append(item)
            return result

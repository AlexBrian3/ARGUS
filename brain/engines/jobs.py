"""
-------------------------------------------------------------------------------
ENGINE 13: JOBS & INTERNSHIPS SCOUT ("AS EARLY AS THEY COME")
-------------------------------------------------------------------------------
Surfaces high-conviction engineering roles, internships, and research fellowships
as early as they are posted — BEFORE they become flooded with applicants!

Production Target Sources (documented for live scraper deployment):
- Web3 Job Boards: web3.career, CryptoJobsList, cryptocurrencyjobs.co
- Ecosystem Bounties & Grants: Superteam Earn (Solana), Base Ecosystem jobs
- Direct Foundation Careers: Ethereum Foundation, Uniswap Foundation, Solana Foundation
- AI Research & Lab Boards: Company career portals, AI lab fellowship pages

Key Superpower:
ARGUS immediately evaluates candidate fit against your AI Platform & backend
stack (Python, FastAPI, vLLM, LangGraph, React, Kubernetes). Fresh high-fit roles
trigger an immediate Level 1 'First Signal' alert so you can apply in the first 24 hours.
"""

from typing import Dict, List, Any, Optional
import datetime
from brain.db.database import Database
from brain.engines.user_fit import UserFitEngine
from brain.engines.alerts import AlertEngine


class JobsScout:
    """Scouts, scores, and alerts on newly posted Web3 and AI developer roles."""

    def __init__(self, db: Database = None):
        self.db = db if db is not None else Database()
        self.user_fit = UserFitEngine()
        self.alert_engine = AlertEngine(self.db)

    def match_listing_to_user_skills(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 1: Calculate how well this role matches your background.
        Returns a fit score out of 100.0 and tailored application talking points.
        """
        title = listing.get("title", "").lower()
        company = listing.get("company", "").lower()
        category = listing.get("ecosystem_or_category", "").lower()
        role_type = listing.get("role_type", "").lower()
        tags = [t.lower() for t in listing.get("skill_tags", [])]

        # Combine text for holistic matching
        combined_text = f"{title} {company} {category} {role_type} {' '.join(tags)}"

        # Evaluate against primary skills
        fit_score = self.user_fit.evaluate_skill_match(
            opportunity_tags=tags or [title, category],
            required_tech=[category]
        )

        # High priority roles for Staff/Senior AI Platform profile
        is_ai_platform = any(
            term in combined_text
            for term in ["ai platform", "model serving", "infra", "inference", "eval", "agent", "llm gateway", "fastapi"]
        )

        if is_ai_platform:
            fit_score = min(max(fit_score, 88.0) + 4.0, 99.0)

        # ------------------------------------------------------------------- #
        # Step 2: Unfair Advantage Application Strategy                       #
        # ------------------------------------------------------------------- #
        if "agent" in combined_text or "ai" in combined_text:
            pitch = (
                "Lead with autonomous model evaluation pipelines (Ragas/DeepEval) "
                "and high-concurrency token streaming via FastAPI / Ray Serve."
            )
        elif "intern" in role_type or "fellowship" in role_type:
            pitch = (
                "Showcase demonstrable production codebases (hackathon-launchpad dual-pane UI + async backend) "
                "and competitive placement track record."
            )
        else:
            pitch = (
                "Emphasize production infrastructure reliability, Langfuse tracing, "
                "and low-latency microservice architecture."
            )

        return {
            "fit_score": round(fit_score, 1),
            "is_high_fit": fit_score >= 75.0,
            "application_strategy": pitch
        }

    def process_raw_listing(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 3: Ingest, normalize, evaluate, and store a job/internship listing.
        """
        job_id = raw_data.get("id") or f"job_{raw_data.get('company', '').lower()}_{raw_data.get('title', '').lower()}".replace(" ", "_")
        now_iso = datetime.datetime.now().isoformat()

        tags = list(raw_data.get("skill_tags") or [])
        if not tags and "description" in raw_data:
            desc = raw_data["description"].lower()
            for kw in ["python", "solana", "fastapi", "ai agents", "smart contracts", "pyth", "typescript", "ai"]:
                if kw in desc:
                    tags.append(kw)

        clean_record = {
            "id": job_id,
            "title": raw_data["title"],
            "company": raw_data["company"],
            "ecosystem_or_category": raw_data.get("ecosystem_or_category") or raw_data.get("ecosystem", "Web3"),
            "role_type": raw_data.get("role_type", "full_time"),
            "location": raw_data.get("location", "Remote"),
            "remote": bool(raw_data.get("remote", True)),
            "compensation_notes": raw_data.get("compensation_notes") or raw_data.get("compensation", "Competitive"),
            "first_seen": raw_data.get("first_seen", now_iso),
            "application_deadline": raw_data.get("application_deadline", "Rolling"),
            "url": raw_data.get("url") or raw_data.get("apply_url", ""),
            "skill_tags": tags,
            "freshness_alert_sent": bool(raw_data.get("freshness_alert_sent", False))
        }

        match_res = self.match_listing_to_user_skills(clean_record)
        clean_record["fit_score"] = match_res["fit_score"]
        clean_record["skill_match_score"] = match_res["fit_score"]
        clean_record["is_high_fit"] = match_res["is_high_fit"]
        clean_record["application_strategy"] = match_res["application_strategy"]

        self.db.upsert_job_listing(clean_record)
        return clean_record

    def get_fresh_listings(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Step 4: Returns listings first detected within the past N hours.
        This provides the 'as early as they come' information advantage.
        """
        raw_fresh = self.db.get_fresh_job_listings(hours=hours)
        scored = []
        for job in raw_fresh:
            match_res = self.match_listing_to_user_skills(job)
            item = dict(job)
            item["fit_score"] = match_res["fit_score"]
            item["skill_match_score"] = match_res["fit_score"]
            item["is_fresh"] = True
            item["is_high_fit"] = match_res["is_high_fit"]
            item["application_strategy"] = match_res["application_strategy"]
            scored.append(item)

        scored.sort(key=lambda x: x["fit_score"], reverse=True)
        return scored

    def get_all_ranked_listings(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Returns all job listings ranked by user skill fit score.
        """
        from datetime import datetime, timezone, timedelta
        all_jobs = self.db.get_all_job_listings(limit=limit)
        scored = []
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        for job in all_jobs:
            match_res = self.match_listing_to_user_skills(job)
            item = dict(job)
            item["fit_score"] = match_res["fit_score"]
            item["skill_match_score"] = match_res["fit_score"]
            item["is_high_fit"] = match_res["is_high_fit"]
            item["application_strategy"] = match_res["application_strategy"]
            try:
                first_seen_str = str(job.get("first_seen", "")).replace("Z", "+00:00")
                first_seen_dt = datetime.fromisoformat(first_seen_str)
                if first_seen_dt.tzinfo is None:
                    first_seen_dt = first_seen_dt.replace(tzinfo=timezone.utc)
                item["is_fresh"] = first_seen_dt >= cutoff
            except Exception:
                item["is_fresh"] = False
            scored.append(item)

        scored.sort(key=lambda x: x["fit_score"], reverse=True)
        return scored

    def scan_and_alert_fresh_jobs(self, fit_threshold: float = 75.0) -> List[Dict[str, Any]]:
        """
        Step 5: Detects newly posted listings and triggers an immediate Level 1 alert
        if the listing matches the user's stack above the fit threshold.
        """
        fresh_jobs = self.get_fresh_listings(hours=24)
        fired_alerts = []

        for job in fresh_jobs:
            # Only alert if high fit and alert has not yet been sent
            if job["fit_score"] >= fit_threshold and not job["freshness_alert_sent"]:
                fingerprint = self.alert_engine.generate_dedupe_hash(1, job["id"], "fresh_job_alert")
                alert = {
                    "id": f"alert_job_{job['id']}",
                    "alert_level": 1,
                    "opportunity_id": None,
                    "title": f"🔴 [LEVEL 1 FIRST SIGNAL] Fresh Role Detected: {job['title']} @ {job['company']}",
                    "summary": (
                        f"Newly posted {job['role_type']} ({job['location']}) matches your stack "
                        f"with a Fit Score of {job['fit_score']:.1f}/100. Compensation: {job['compensation_notes']}."
                    ),
                    "why_mispriced": "Early application window before job board saturation. First 24-48 hours have highest callback rate.",
                    "action_items": [
                        f"Apply via link: {job['url'] or 'Direct company careers portal'}",
                        f"Tailor pitch: {job['application_strategy']}"
                    ],
                    "what_to_learn_immediately": f"Review {job['company']}'s latest technical blogs and GitHub repos",
                    "should_register_immediately": True,
                    "dedupe_hash": fingerprint
                }

                if self.db.insert_alert_if_new(alert):
                    self.db.mark_job_alert_sent(job["id"])
                    fired_alerts.append(alert)

        return fired_alerts

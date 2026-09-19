"""
-------------------------------------------------------------------------------
ENGINE 12: BENEFITS & PERKS TRACKER
-------------------------------------------------------------------------------
Tracks standing, non-hackathon developer support programs:

1. Foundation grants (e.g. Ethereum Foundation, Uniswap Foundation)
2. Fellowships & researcher stipends (e.g. Polygon, Starknet)
3. Retroactive funding (e.g. Optimism RetroPGF)
4. Gas rebates, testnet credits, and accelerator perks

Unlike hackathons, these opportunities are often on a ROLLING basis with
no single ticking countdown. ARGUS matches each benefit against YOUR
specific AI Platform superpowers so you focus on grants where you have
the highest probability of getting funded.
"""

from typing import Dict, List, Any, Optional
from brain.db.database import Database
from brain.engines.user_fit import UserFitEngine


class BenefitsTracker:
    """Discovers, tracks, and ranks standing grants, fellowships, and developer perks."""

    def __init__(self, db: Database = None):
        # Connect to persistent database memory
        self.db = db if db is not None else Database()
        # Connect to user fit engine to evaluate personal relevance
        self.user_fit = UserFitEngine()

    def upsert_benefit(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 1: Save or update a benefit record in SQLite storage.
        """
        self.db.upsert_benefit(data)
        return data

    def upsert_benefit_record(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Alias for upsert_benefit."""
        return self.upsert_benefit(data)

    def get_all_benefits(self) -> List[Dict[str, Any]]:
        """
        Returns all standing benefits stored in the database.
        """
        return self.db.get_all_benefits()

    def get_benefits_for_ecosystem(self, ecosystem_slug: str) -> List[Dict[str, Any]]:
        """
        Returns standing benefits filtered by target ecosystem or provider name.
        """
        return self.db.get_benefits_for_ecosystem(ecosystem_slug)

    def get_benefits_by_ecosystem(self, ecosystem_slug: str) -> List[Dict[str, Any]]:
        """Alias for get_benefits_for_ecosystem."""
        return self.get_benefits_for_ecosystem(ecosystem_slug)

    def match_benefits_to_user_fit(self, benefit: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 2: Compare a benefit program against your specific technical stack.
        Returns a relevance score (0.0 to 100.0) and custom application tips.
        """
        notes = benefit.get("eligibility_notes", "").lower()
        name = benefit.get("name", "").lower()
        b_type = benefit.get("benefit_type", "").lower()
        ecosystem = benefit.get("ecosystem", "").lower()

        # Combine all textual keywords for matching
        combined_text = f"{name} {notes} {b_type} {ecosystem}"

        # Extract user profile skills
        user_skills = [s.lower() for s in self.user_fit.profile["primary_skills"]]

        # Count direct skill mentions
        matched_skills = [s for s in user_skills if s in combined_text]

        # Calculate baseline match score
        base_score = 65.0

        # AI/ML, Agents, or Infrastructure grants have an immediate high affinity
        if any(term in combined_text for term in ["ai", "agent", "infra", "eval", "tooling", "python", "developer tool"]):
            base_score += 20.0

        # Retroactive funding or research fellowships reward open-source tooling
        if b_type in ["retroactive_funding", "fellowship", "grant"]:
            base_score += 5.0

        # Bonus for matching specific technologies
        skill_bonus = min(len(matched_skills) * 4.0, 10.0)
        final_relevance = min(base_score + skill_bonus, 98.0)

        # ------------------------------------------------------------------- #
        # Step 3: Plain-English application advisory                          #
        # ------------------------------------------------------------------- #
        if "agent" in combined_text or "ai" in combined_text:
            pitch_angle = "Frame application around autonomous evaluation harnesses, x402 payment proxies, or verifiable inference."
        elif "infra" in combined_text or "tool" in combined_text:
            pitch_angle = "Highlight FastAPI high-concurrency event telemetry and open-source benchmark suites."
        elif "retro" in combined_text:
            pitch_angle = "Document public GitHub commits and developer adoption metrics from your reusable assets."
        else:
            pitch_angle = f"Focus on developer productivity and tooling infrastructure for the {benefit.get('ecosystem')} ecosystem."

        return {
            "relevance_score": round(final_relevance, 1),
            "matched_skills": matched_skills,
            "recommended_pitch_angle": pitch_angle,
            "is_high_priority": final_relevance >= 85.0
        }

    def get_ranked_benefits(self, ecosystem_slug: str = None) -> List[Dict[str, Any]]:
        """
        Step 4: Return benefits ranked by user relevance score first,
        then by typical dollar funding amount.
        """
        if ecosystem_slug:
            raw_benefits = self.get_benefits_for_ecosystem(ecosystem_slug)
        else:
            raw_benefits = self.get_all_benefits()

        scored_benefits = []
        for b in raw_benefits:
            fit_result = self.match_benefits_to_user_fit(b)
            item = dict(b)
            item["relevance_score"] = fit_result["relevance_score"]
            item["user_fit_score"] = fit_result["relevance_score"]
            item["title"] = item.get("title") or item.get("name", "Ecosystem Benefit")
            item["amount_usd"] = item.get("amount_usd") or item.get("typical_amount_usd", 0)
            item["slug"] = item.get("slug") or item.get("id", "")
            item["matched_skills"] = fit_result["matched_skills"]
            item["recommended_pitch_angle"] = fit_result["recommended_pitch_angle"]
            item["is_high_priority"] = fit_result["is_high_priority"]
            scored_benefits.append(item)

        # Sort: Highest relevance first, then highest amount
        scored_benefits.sort(
            key=lambda x: (x["relevance_score"], x.get("amount_usd", 0.0)),
            reverse=True
        )

        return scored_benefits

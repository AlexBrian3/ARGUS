"""
-------------------------------------------------------------------------------
ENGINE 2: ECOSYSTEM RADAR
-------------------------------------------------------------------------------
Continuously monitors important developer ecosystems (Solana, Base, Monad, etc.).

Calculates:
1. ECOSYSTEM MOMENTUM SCORE (out of 100)
2. TRAJECTORY (↑ accelerating, → stable, ↓ declining)
3. STEALTH OPPORTUNITIES: Detects ecosystems BEFORE their big hackathons!
"""

from typing import Dict, List, Any, Tuple
from brain.config import ECOSYSTEM_MOMENTUM_WEIGHTS
from brain.db.database import Database


class EcosystemRadar:
    """Monitors developer momentum across emerging and established ecosystems."""

    def __init__(self, db: Database = None):
        # If no database is passed in, create a connection to the default one
        self.db = db if db is not None else Database()

    def calculate_momentum_score(self, metrics: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
        """
        Step 1: Calculate the momentum score (out of 100) by checking 8 key factors:
        - Developer programs (20 pts)
        - Hackathons and grants (20 pts)
        - Developer activity acceleration (15 pts)
        - SDK launches (10 pts)
        - Sponsor activity (10 pts)
        - Social discussion (10 pts)
        - Funding activity (5 pts)
        - Competition opportunity (10 pts)
        """
        total_score = 0.0
        score_breakdown = {}

        for factor_name, max_allowed_weight in ECOSYSTEM_MOMENTUM_WEIGHTS.items():
            # Get the raw value (default to 0.0 if not provided)
            raw_value = float(metrics.get(factor_name, 0.0))

            # Make sure the value cannot be negative or higher than the max allowed weight
            clamped_value = min(max(raw_value, 0.0), float(max_allowed_weight))

            total_score += clamped_value
            score_breakdown[factor_name] = round(clamped_value, 2)

        return round(total_score, 1), score_breakdown

    def determine_trajectory(
        self,
        current_score: float,
        previous_score: float = None,
        delta_threshold: float = 2.0
    ) -> str:
        """
        Step 2: Determine if momentum is speeding up, staying flat, or slowing down:
        ↑ = accelerating (heating up!)
        → = stable (healthy and steady)
        ↓ = declining (cooling off)
        """
        # If this is our very first time measuring this ecosystem:
        if previous_score is None:
            if current_score >= 85.0:
                return "↑"
            elif current_score >= 70.0:
                return "→"
            else:
                return "↓"

        # Compare new score against old score
        score_difference = current_score - previous_score

        if score_difference >= delta_threshold:
            return "↑"  # Score jumped by at least 2 points
        elif score_difference <= -delta_threshold:
            return "↓"  # Score dropped by at least 2 points
        else:
            return "→"  # Within normal variation

    def update_ecosystem_momentum(
        self,
        slug: str,
        name: str,
        category: str,
        metrics: Dict[str, float],
        notes: str = "",
        tracked_repos: List[str] = None,
        maturity_stage: str = None
    ) -> Dict[str, Any]:
        """
        Step 3: Save the updated scores into persistent database memory.
        """
        existing_record = self.db.get_ecosystem(slug)
        previous_score = existing_record["momentum_score"] if existing_record else None
        current_stage = maturity_stage or (existing_record.get("maturity_stage", "established") if existing_record else "watchlist")

        score, breakdown = self.calculate_momentum_score(metrics)
        trajectory = self.determine_trajectory(score, previous_score)

        data = {
            "slug": slug,
            "name": name,
            "category": category,
            "momentum_score": score,
            "momentum_trajectory": trajectory,
            "breakdown_scores": breakdown,
            "tracked_repos": tracked_repos or (existing_record["tracked_repos"] if existing_record else []),
            "notes": notes or (existing_record["notes"] if existing_record else ""),
            "maturity_stage": current_stage,
            "first_detected": existing_record.get("first_detected") if existing_record else None
        }

        self.db.upsert_ecosystem(data)
        return data

    def discover_new_ecosystems(self, raw_signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Step 4 (Engine 11): Ecosystem Discovery Radar.
        Scans raw ecosystem signals, discovers new platforms, promotes stages
        when momentum thresholds are crossed, and triggers Level 1 alerts.
        """
        from brain.engines.alerts import AlertEngine
        alert_engine = AlertEngine(self.db)
        discovered_or_updated = []

        for signal in raw_signals:
            slug = signal.get("slug") or signal.get("name", "").lower().replace(" ", "-").replace("/", "-")
            name = signal.get("name", slug.title())
            category = signal.get("category", "L1")
            notes = signal.get("notes", "")
            metrics = signal.get("metrics") or signal.get("breakdown_scores", {})
            stage = signal.get("maturity_stage", "watchlist")

            existing = self.db.get_ecosystem(slug)

            if not existing:
                # Brand new platform detected!
                score, breakdown = self.calculate_momentum_score(metrics)
                trajectory = self.determine_trajectory(score)
                eco_data = {
                    "slug": slug,
                    "name": name,
                    "category": category,
                    "momentum_score": score,
                    "momentum_trajectory": trajectory,
                    "breakdown_scores": breakdown,
                    "tracked_repos": signal.get("tracked_repos", []),
                    "notes": notes,
                    "maturity_stage": stage
                }
                self.db.upsert_ecosystem(eco_data)
                discovered_or_updated.append(eco_data)
            else:
                # Platform already monitored; calculate latest momentum
                score, breakdown = self.calculate_momentum_score(metrics) if metrics else (existing["momentum_score"], existing.get("breakdown_scores", {}))
                trajectory = self.determine_trajectory(score, existing["momentum_score"])
                old_stage = existing.get("maturity_stage", "watchlist")
                new_stage = old_stage

                # ----------------------------------------------------------- #
                # Stage Promotion Logic                                       #
                # ----------------------------------------------------------- #
                # If watchlist platform reaches 70+ momentum -> promote to emerging
                if old_stage == "watchlist" and score >= 70.0:
                    new_stage = "emerging"

                # If emerging platform reaches 85+ momentum -> promote to established
                elif old_stage == "emerging" and score >= 85.0:
                    new_stage = "established"

                eco_data = {
                    "slug": slug,
                    "name": name,
                    "category": category,
                    "momentum_score": score,
                    "momentum_trajectory": trajectory,
                    "breakdown_scores": breakdown,
                    "tracked_repos": signal.get("tracked_repos", existing.get("tracked_repos", [])),
                    "notes": notes or existing.get("notes", ""),
                    "maturity_stage": new_stage
                }
                self.db.upsert_ecosystem(eco_data)

                # Fire Level 1 alert if promoted to a higher stage
                if new_stage != old_stage:
                    fingerprint = alert_engine.generate_dedupe_hash(1, slug, f"promoted_{new_stage}")
                    alert = {
                        "id": f"alert_promo_{slug}_{new_stage}",
                        "alert_level": 1,
                        "opportunity_id": None,
                        "title": f"🔴 [LEVEL 1 FIRST SIGNAL] Ecosystem Promoted: {name} → {new_stage.upper()}",
                        "summary": (
                            f"{name} crossed momentum threshold ({score:.1f}/100) and was promoted "
                            f"from '{old_stage}' to '{new_stage}'."
                        ),
                        "why_mispriced": f"Early momentum surge ({trajectory}) before general developer crowd migration.",
                        "action_items": [
                            f"Inspect {name} documentation and SDK repos",
                            f"Check for newly launched grant pools or builder challenges"
                        ],
                        "what_to_learn_immediately": f"{name} core SDKs and testnet RPC",
                        "should_register_immediately": False,
                        "dedupe_hash": fingerprint
                    }
                    self.db.insert_alert_if_new(alert)

                discovered_or_updated.append(eco_data)

        return discovered_or_updated

    def discover_new_ecosystem(
        self,
        name: str,
        category: str,
        notes: str = "",
        initial_momentum: float = 50.0,
        maturity_stage: str = "watchlist"
    ) -> Dict[str, Any]:
        """Convenience method to register and start monitoring a single newly discovered platform."""
        results = self.discover_new_ecosystems([{
            "name": name,
            "category": category,
            "notes": notes,
            "maturity_stage": maturity_stage,
            "breakdown_scores": {"developer_programs": initial_momentum * 0.25}
        }])
        return results[0] if results else {}

    def update_stage_on_momentum(self, slug: str, new_momentum: float) -> str:
        """
        Updates an ecosystem's momentum score, promotes stage if crossing threshold,
        and fires a Level 1 First Signal alert if promoted.
        Returns the updated maturity stage.
        """
        existing = self.db.get_ecosystem(slug)
        if not existing:
            return "watchlist"

        old_stage = existing.get("maturity_stage", "watchlist")
        new_stage = old_stage

        if old_stage == "watchlist" and new_momentum >= 70.0:
            new_stage = "emerging"
        elif old_stage == "emerging" and new_momentum >= 85.0:
            new_stage = "established"

        trajectory = self.determine_trajectory(new_momentum, existing.get("momentum_score", 0.0))
        eco_data = dict(existing)
        eco_data["momentum_score"] = new_momentum
        eco_data["momentum_trajectory"] = trajectory
        eco_data["maturity_stage"] = new_stage
        self.db.upsert_ecosystem(eco_data)

        if new_stage != old_stage:
            from brain.engines.alerts import AlertEngine
            alert_engine = AlertEngine(self.db)
            fingerprint = alert_engine.generate_dedupe_hash(1, slug, f"promoted_{new_stage}")
            alert = {
                "id": f"alert_promo_{slug}_{new_stage}",
                "alert_level": 1,
                "opportunity_id": None,
                "title": f"🔴 [LEVEL 1 FIRST SIGNAL] Ecosystem Promoted: {existing.get('name')} → {new_stage.upper()}",
                "summary": (
                    f"{existing.get('name')} crossed momentum threshold ({new_momentum:.1f}/100) and was promoted "
                    f"from '{old_stage}' to '{new_stage}'."
                ),
                "why_mispriced": f"Early momentum surge ({trajectory}) before general developer crowd migration.",
                "action_items": [
                    f"Inspect {existing.get('name')} documentation and SDK repos",
                    f"Check for newly launched grant pools or builder challenges"
                ],
                "what_to_learn_immediately": f"{existing.get('name')} core SDKs and testnet RPC",
                "should_register_immediately": False,
                "dedupe_hash": fingerprint
            }
            self.db.insert_alert_if_new(alert)

        return new_stage

    def get_leaderboard(self) -> List[Dict[str, Any]]:
        """Returns all ecosystems sorted from highest momentum to lowest."""
        return self.db.get_all_ecosystems()

    def get_ecosystems_by_stage(self, stage: str) -> List[Dict[str, Any]]:
        """Returns ecosystems filtered by maturity stage (watchlist, emerging, established)."""
        return self.db.get_ecosystems_by_stage(stage)

    def detect_stealth_opportunities(self) -> List[Dict[str, Any]]:
        """
        Step 5: Find ecosystems that are quietly ramping up developer incentives
        before their big hackathon is announced to the public crowd!
        """
        all_ecosystems = self.db.get_all_ecosystems()
        stealth_list = []

        for ecosystem in all_ecosystems:
            is_accelerating = ecosystem.get("momentum_trajectory") == "↑"
            has_high_score = ecosystem.get("momentum_score", 0.0) >= 80.0

            if is_accelerating and has_high_score:
                breakdown = ecosystem.get("breakdown_scores", {})
                programs = breakdown.get("developer_programs", 0.0)
                grants = breakdown.get("hackathons_and_grants", 0.0)

                # If developer incentives + grants add up to 32+ points:
                if (programs + grants) >= 32.0:
                    stealth_list.append(ecosystem)

        return stealth_list

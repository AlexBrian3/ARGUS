"""
-------------------------------------------------------------------------------
ENGINE 6: USER FIT & UNFAIR ADVANTAGE MATCHER
-------------------------------------------------------------------------------
This engine compares the requirements of any hackathon, bounty, or grant
against YOUR specific background and pre-built code assets.

Never recommend generic ideas! We calculate:
1. SKILL MATCH (out of 100)
2. Reusable backend code you can copy in 5 minutes
3. Reusable UI components from hackathon-launchpad
4. Technologies you already know vs. what you need to learn
5. A tailored, non-generic build direction giving you an unfair advantage.
"""

from typing import Dict, List, Any
from brain.config import USER_PROFILE


class UserFitEngine:
    """Evaluates how well an opportunity fits your technical superpowers."""

    def __init__(self, profile: Dict[str, Any] = None):
        # Default to the user profile saved in config.py
        self.profile = profile if profile is not None else USER_PROFILE

    def evaluate_skill_match(
        self,
        opportunity_tags: List[str],
        required_tech: List[str] = None
    ) -> float:
        """
        Step 1: Check how many requirements match your skills.
        Returns a score between 0.0 and 100.0.
        """
        # Convert all user skills to lowercase for easy matching
        user_skills_lowercase = {skill.lower() for skill in self.profile["primary_skills"]}

        # Add helpful broad matching keywords related to your background
        broad_keywords = [
            "ai", "ml", "fastapi", "python", "llm", "agents",
            "react", "tailwind", "api", "infra", "evals", "observability"
        ]
        user_skills_lowercase.update(broad_keywords)

        # Collect all keywords that describe this opportunity
        opportunity_keywords = [tag.lower() for tag in opportunity_tags]
        if required_tech:
            opportunity_keywords.extend([tech.lower() for tech in required_tech])

        # If no keywords were provided, give a sensible baseline
        if not opportunity_keywords:
            return 80.0

        # Count how many opportunity keywords match your skill list
        matched_count = 0
        for keyword in opportunity_keywords:
            for skill in user_skills_lowercase:
                if skill in keyword or keyword in skill:
                    matched_count += 1
                    break

        match_ratio = matched_count / len(opportunity_keywords)

        # If the competition is focused on AI Agents, Developer Tools, or Infrastructure,
        # your AI Platform background gives you an automatic high-tier match:
        is_ai_or_infra = any(
            "agent" in kw or "ai" in kw or "devtool" in kw or "infra" in kw
            for kw in opportunity_keywords
        )

        if is_ai_or_infra:
            score = 82.0 + (match_ratio * 16.0)
        else:
            score = 65.0 + (match_ratio * 30.0)

        # Clamp score between 0 and 98 max
        return round(min(score, 98.0), 1)

    def analyze_fit(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 2: Generate a complete action plan showing exactly what to build,
        what code to reuse, and what to study before opening registration.
        """
        tags = opportunity.get("tags", [])
        sponsors = opportunity.get("sponsors", [])
        ecosystem = opportunity.get("ecosystem", "")
        name = opportunity.get("name", "")

        # Calculate skill match score
        skill_match = self.evaluate_skill_match(tags)

        # ------------------------------------------------------------------- #
        # Step 3: Select reusable code modules from your arsenal              #
        # ------------------------------------------------------------------- #
        reusable_code = [
            "FastAPI asynchronous event-driven SSE pipeline (from hackathon-launchpad)",
            "Multi-agent loop execution & tool-call streaming (backend/app/agent.py)",
            "Enterprise semantic caching & LLM gateway routing",
            "Autonomous evaluation harness (Ragas / DeepEval regression scoring)"
        ]

        reusable_ui = [
            "Hackathon Launchpad React + Tailwind dual-pane canvas (AgentTimeline + OutputCanvas)",
            "1-Click Fail-Safe Judge Demo Presets (guaranteed live demo under flaky Wi-Fi)",
            "Streaming token-counter and tool execution steppers"
        ]

        technologies_understood = [
            "Python / FastAPI / AsyncIO microservices",
            "High-throughput model serving & token streaming",
            "Agent state machines (LangGraph)",
            "Vector databases & hybrid retrieval",
            "React & Tailwind component architectures"
        ]

        # ------------------------------------------------------------------- #
        # Step 4: Identify gaps — what do you need to learn beforehand?       #
        # ------------------------------------------------------------------- #
        technologies_to_learn = []
        ecosystem_lower = ecosystem.lower()
        tags_str = " ".join(tags).lower()
        sponsors_str = str(sponsors).lower()

        if "solana" in ecosystem_lower:
            technologies_to_learn.append("Solana Web3.js / Anchor client basics or Python Solana RPC")
        if "base" in ecosystem_lower or "world" in sponsors_str:
            technologies_to_learn.append("World ID MiniKit SDK / Coinbase AgentKit Python")
        if "x402" in tags_str:
            technologies_to_learn.append("HTTP 402 Payment Required header signing & facilitator specs")
        if "monad" in ecosystem_lower:
            technologies_to_learn.append("Monad parallel execution RPC and testnet contracts")

        if not technologies_to_learn:
            technologies_to_learn.append("Ecosystem-specific RPC connectors")

        prep_difficulty = "Low (1-2 days)" if len(technologies_to_learn) <= 2 else "Moderate (3-4 days)"

        # ------------------------------------------------------------------- #
        # Step 5: Design a custom, non-generic build direction                #
        # ------------------------------------------------------------------- #
        name_lower = name.lower()

        if "colosseum" in name_lower or "solana" in ecosystem_lower:
            direction = (
                "Unfair Advantage Build: Autonomous Agent x402 Micropayment Gateway.\n"
                "Combine your FastAPI high-concurrency engine with an x402 reverse proxy. "
                "AI agents querying your endpoints pay micro-tokens per LLM inference call on Solana/Base. "
                "Use hackathon-launchpad's dual-pane canvas to show the live payment verification in the left pane "
                "and the streaming LLM inference in the right pane."
            )
        elif "world" in sponsors_str or "ethglobal" in name_lower:
            direction = (
                "Unfair Advantage Build: Human-Guarded Autonomous Agent Escrow.\n"
                "Deploy a LangGraph multi-agent team with NeMo Guardrails that manages onchain treasury or API keys, "
                "requiring World ID biometric zero-knowledge proofs only when a spending threshold or anomalous tool call is detected. "
                "Pitch it as enterprise agent safety backed by World ID."
            )
        else:
            direction = (
                f"Unfair Advantage Build for {ecosystem}:\n"
                "Package your autonomous eval & regression pipeline (DeepEval/Ragas) into a verifiable developer platform "
                "with live SSE event telemetry powered by hackathon-launchpad."
            )

        return {
            "skill_match": skill_match,
            "reusable_code": reusable_code,
            "reusable_ui": reusable_ui,
            "technologies_understood": technologies_understood,
            "technologies_to_learn": technologies_to_learn,
            "preparation_difficulty": prep_difficulty,
            "recommended_build_direction": direction
        }

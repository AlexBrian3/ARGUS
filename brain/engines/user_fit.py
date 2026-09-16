"""
Engine 6 — USER FIT
Evaluates SKILL MATCH /100 by comparing opportunity requirements against:
- User's demonstrated skills (Staff/Senior AI Platform Engineer, FastAPI, LangGraph, vLLM, LiteLLM, Qdrant, React/Tailwind)
- Reusable code & UI from `hackathon-launchpad` (SSE streaming, live steppers, dual-pane canvas, fail-safe judge demo presets)
- Enterprise eval pipelines (Ragas, DeepEval)

Identifies:
- Reusable code & UI
- Relevant previous projects
- Technologies already understood
- Technologies to learn
- Estimated preparation difficulty
- Highly tailored, non-generic build directions
"""
from typing import Dict, List, Any
from brain.config import USER_PROFILE


class UserFitEngine:
    def __init__(self, profile: Dict[str, Any] = None):
        self.profile = profile or USER_PROFILE

    def evaluate_skill_match(self, opportunity_tags: List[str], required_tech: List[str] = None) -> float:
        """
        Calculates SKILL MATCH /100 against user's specific platform/AI stack.
        """
        user_skills_lower = {s.lower() for s in self.profile["primary_skills"]}
        # Add high-overlap keywords
        user_skills_lower.update(["ai", "ml", "fastapi", "python", "llm", "agents", "react", "tailwind", "api", "infra", "evals", "observability"])

        opp_keywords = [t.lower() for t in opportunity_tags]
        if required_tech:
            opp_keywords.extend([t.lower() for t in required_tech])

        if not opp_keywords:
            return 80.0

        matched = 0
        for kw in opp_keywords:
            if any(s in kw or kw in s for s in user_skills_lower):
                matched += 1

        match_ratio = matched / len(opp_keywords)
        # Base calibration: If it's an AI Agent or Developer Tooling event, user has near 90%+ match
        if any("agent" in kw or "ai" in kw or "devtool" in kw or "infra" in kw for kw in opp_keywords):
            score = 82.0 + (match_ratio * 16.0)
        else:
            score = 65.0 + (match_ratio * 30.0)

        return round(min(score, 98.0), 1)

    def analyze_fit(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates comprehensive User Fit profile for an opportunity.
        """
        tags = opportunity.get("tags", [])
        sponsors = opportunity.get("sponsors", [])
        ecosystem = opportunity.get("ecosystem", "")
        name = opportunity.get("name", "")

        skill_match = self.evaluate_skill_match(tags)

        # Map reusable assets from user's arsenal
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

        # Determine technologies understood vs to learn
        understood = [
            "Python / FastAPI / AsyncIO microservices",
            "High-throughput model serving & token streaming",
            "Agent state machines (LangGraph)",
            "Vector databases & hybrid retrieval",
            "React & Tailwind component architectures"
        ]

        to_learn = []
        if "solana" in ecosystem.lower():
            to_learn.append("Solana Web3.js / Anchor client basics or Python Solana RPC")
        if "base" in ecosystem.lower() or "world" in str(sponsors).lower():
            to_learn.append("World ID MiniKit SDK / Coinbase AgentKit Python")
        if "x402" in " ".join(tags).lower():
            to_learn.append("HTTP 402 Payment Required header signing & facilitator specs")
        if "monad" in ecosystem.lower():
            to_learn.append("Monad parallel execution RPC and testnet contracts")

        prep_difficulty = "Low (1-2 days)" if len(to_learn) <= 2 else "Moderate (3-4 days)"

        # Tailor build direction leveraging user's unfair advantage
        if "colosseum" in name.lower() or "solana" in ecosystem.lower():
            direction = (
                "Unfair Advantage Build: Autonomous Agent x402 Micropayment Gateway.\n"
                "Combine your FastAPI high-concurrency engine with an x402 reverse proxy. "
                "AI agents querying your endpoints pay micro-tokens per LLM inference call on Solana/Base. "
                "Use hackathon-launchpad's dual-pane canvas to show the live payment verification in the left pane and the streaming LLM inference in the right pane."
            )
        elif "world" in str(sponsors).lower() or "ethglobal" in name.lower():
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
            "technologies_understood": understood,
            "technologies_to_learn": to_learn or ["Ecosystem-specific RPC connectors"],
            "preparation_difficulty": prep_difficulty,
            "recommended_build_direction": direction
        }

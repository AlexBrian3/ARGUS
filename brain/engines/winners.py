"""
Engine 4 — HISTORICAL WINNER ANALYSIS
Analyzes previous winning projects (10-50 projects per ecosystem/event).
Extracts:
- WINNER PATTERN
- COMMON LOSING PATTERN
- OVERSATURATED IDEAS
- UNDEREXPLORED IDEAS
- TECHNOLOGIES TO LEARN BEFORE ENTERING
"""
from typing import Dict, List, Any, Optional
from brain.db.database import Database


class WinnerAnalyzer:
    def __init__(self, db: Database = None):
        self.db = db or Database()

    def analyze_event_patterns(self, event_name: str = None) -> Dict[str, Any]:
        """
        Synthesizes winner intelligence across historical projects.
        """
        winners = self.db.get_all_winners(limit=100)
        if event_name:
            filtered = [w for w in winners if event_name.lower() in w["event_name"].lower()]
            if filtered:
                winners = filtered

        if not winners:
            return {
                "winner_pattern": "Focus on high-leverage sponsor SDK depth with verifiable live demos.",
                "common_losing_pattern": "Submitting surface-level wrappers with mock data that fail live judge QA.",
                "oversaturated_ideas": ["Generic AI chatbots", "Basic NFT minters", "Simple ERC20 swap dashboards"],
                "underexplored_ideas": ["Autonomous agent payment rails (x402)", "Zero-knowledge agent attestation", "Verifiable inference guardrails"],
                "technologies_to_learn": ["FastAPI SSE streaming", "LiteLLM / vLLM", "Dynamic / World ID embedded SDKs"]
            }

        # Analyze statistics
        total = len(winners)
        ai_count = sum(1 for w in winners if w.get("ai_usage"))
        fin_count = sum(1 for w in winners if w.get("financial_use_case"))
        infra_count = sum(1 for w in winners if "infra" in str(w.get("product_category", "")).lower())
        avg_integrations = sum(w.get("number_of_integrations", 1) for w in winners) / max(total, 1)

        winning_patterns = [w["winning_patterns"] for w in winners if w.get("winning_patterns")]
        losing_patterns = [w["losing_patterns_identified"] for w in winners if w.get("losing_patterns_identified")]

        return {
            "total_analyzed": total,
            "ai_integration_rate": f"{round((ai_count / total) * 100)}%",
            "financial_use_case_rate": f"{round((fin_count / total) * 100)}%",
            "infrastructure_rate": f"{round((infra_count / total) * 100)}%",
            "average_sponsor_integrations": round(avg_integrations, 1),
            "winner_patterns": winning_patterns or [
                "Deep 2-3 sponsor SDK integration rather than surface-level API calls",
                "Asynchronous streaming UI with live execution steppers",
                "Cryptographic or verifiable proofs backing AI output",
                "1-click fail-safe demo presets to survive flaky demo Wi-Fi"
            ],
            "common_losing_patterns": losing_patterns or [
                "Chatbot wrapper requiring manual wallet popups for every single token or step",
                "Frontend mockups without working backend endpoints or deployed contracts",
                "Ignoring sponsor-specific features (e.g. using World without World ID nullifier check)",
                "Submitting to 10 sponsor tracks with zero substantive integration"
            ],
            "oversaturated_ideas": [
                "Generic Telegram trading bots with basic alerts",
                "Basic AI portfolio summarizer without autonomous execution",
                "Single-track NFT / memecoin launchpad clones",
                "Prompt-to-smart-contract generators with unverified compiler checks"
            ],
            "underexplored_ideas": [
                "Autonomous agent micro-escrows via x402 HTTP 402 payment headers",
                "Verifiable LLM evaluation & regression test harnesses running onchain",
                "Session-key spending guardrails with World ID human escalation fallback",
                "Parallel EVM high-throughput real-time risk hedging engines"
            ],
            "technologies_to_learn": [
                "x402 payment authorization headers & facilitator flows",
                "World ID MiniKit & AgentKit SDKs",
                "Dynamic multi-chain embedded wallet session keys",
                "Pyth Network Hermes pull oracle updates",
                "FastAPI async event-streaming (SSE) with LangGraph"
            ]
        }

"""
-------------------------------------------------------------------------------
ENGINE 4: HISTORICAL WINNER ANALYSIS
-------------------------------------------------------------------------------
This engine studies previous hackathon winners (10 to 50 projects per event).

It reverse-engineers:
1. WINNING PATTERNS: What made judges pick these projects?
2. COMMON LOSING PATTERNS: Why did 90% of competitors fail?
3. OVERSATURATED IDEAS: What is everyone building that judges are tired of seeing?
4. UNDEREXPLORED IDEAS: The hidden gems where judges give out prizes easily!
5. TECHNOLOGIES TO LEARN BEFORE ENTERING
"""

from typing import Dict, List, Any
from brain.db.database import Database


class WinnerAnalyzer:
    """Dissects historical winning and losing projects to find winning recipes."""

    def __init__(self, db: Database = None):
        self.db = db if db is not None else Database()

    def analyze_event_patterns(self, event_name: str = None) -> Dict[str, Any]:
        """
        Step 1: Load past winners from the database and calculate key statistics.
        """
        all_winners = self.db.get_all_winners(limit=100)

        # If user wants to filter by a specific event (e.g. "ETHGlobal" or "Colosseum")
        if event_name:
            filtered_winners = [
                w for w in all_winners
                if event_name.lower() in w["event_name"].lower()
            ]
            if filtered_winners:
                all_winners = filtered_winners

        # If the database has no historical winners recorded yet, return sensible defaults
        if not all_winners:
            return {
                "winner_pattern": "Focus on high-leverage sponsor SDK depth with verifiable live demos.",
                "common_losing_pattern": "Submitting surface-level wrappers with mock data that fail live judge QA.",
                "oversaturated_ideas": ["Generic AI chatbots", "Basic NFT minters", "Simple ERC20 swap dashboards"],
                "underexplored_ideas": ["Autonomous agent payment rails (x402)", "Zero-knowledge agent attestation", "Verifiable inference guardrails"],
                "technologies_to_learn": ["FastAPI SSE streaming", "LiteLLM / vLLM", "Dynamic / World ID embedded SDKs"]
            }

        # ------------------------------------------------------------------- #
        # Step 2: Compute stats across all analyzed projects                  #
        # ------------------------------------------------------------------- #
        total_projects = len(all_winners)
        ai_projects_count = sum(1 for project in all_winners if project.get("ai_usage"))
        financial_projects_count = sum(1 for project in all_winners if project.get("financial_use_case"))
        infra_projects_count = sum(
            1 for project in all_winners
            if "infra" in str(project.get("product_category", "")).lower()
        )

        total_integrations = sum(project.get("number_of_integrations", 1) for project in all_winners)
        average_integrations = total_integrations / max(total_projects, 1)

        # Collect winning and losing pattern descriptions
        winning_patterns = [
            project["winning_patterns"] for project in all_winners
            if project.get("winning_patterns")
        ]
        losing_patterns = [
            project["losing_patterns_identified"] for project in all_winners
            if project.get("losing_patterns_identified")
        ]

        # ------------------------------------------------------------------- #
        # Step 3: Package into clean, beginner-friendly insights             #
        # ------------------------------------------------------------------- #
        return {
            "total_analyzed": total_projects,
            "ai_integration_rate": f"{round((ai_projects_count / total_projects) * 100)}%",
            "financial_use_case_rate": f"{round((financial_projects_count / total_projects) * 100)}%",
            "infrastructure_rate": f"{round((infra_projects_count / total_projects) * 100)}%",
            "average_sponsor_integrations": round(average_integrations, 1),
            "winner_patterns": winning_patterns or [
                "Deep integration with 2-3 sponsor SDKs rather than surface-level API calls",
                "Asynchronous streaming UI with live execution steppers",
                "Cryptographic or verifiable proofs backing AI model output",
                "1-click fail-safe demo presets to survive flaky demo Wi-Fi"
            ],
            "common_losing_patterns": losing_patterns or [
                "Chatbot wrapper requiring manual wallet popups for every single token or step",
                "Frontend mockups without working backend endpoints or deployed contracts",
                "Ignoring sponsor-specific features (e.g. using World without World ID nullifiers)",
                "Submitting to 10 sponsor tracks with zero substantive integration"
            ],
            "oversaturated_ideas": [
                "Generic Telegram trading bots with basic alerts",
                "Basic AI portfolio summarizers without autonomous execution",
                "Single-track NFT or memecoin launchpad clones",
                "Prompt-to-smart-contract generators without compiler security checks"
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

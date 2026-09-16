"""
Configuration and constants for ARGUS: The Hundred-Eyed Builder Intelligence Engine.
"""
from pathlib import Path

# Directory paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DASHBOARD_DIR = BASE_DIR / "dashboard"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "brain.db"

# User Profile definition (derived from user's AI Platform engineering background and hackathon-launchpad)
USER_PROFILE = {
    "name": "Staff/Senior AI Platform Engineer",
    "primary_skills": [
        "Python", "FastAPI", "AsyncIO", "PyTorch", "vLLM", "Ray Serve",
        "Triton Inference Server", "LiteLLM", "LangGraph", "LlamaIndex",
        "Qdrant", "Milvus", "Ragas", "DeepEval", "NeMo Guardrails",
        "TypeScript", "React", "TailwindCSS", "Go", "Docker", "Kubernetes"
    ],
    "reusable_assets": [
        "hackathon-launchpad (FastAPI SSE streaming, live execution steppers, dual-pane output canvas, fail-safe judge demo presets)",
        "Enterprise LLM gateway with semantic caching and intelligent prompt routing",
        "End-to-end multi-agent span tracing and observability (Langfuse / OpenTelemetry)",
        "Autonomous LLM evaluation and regression harness",
        "High-throughput model serving KV-cache optimization pipeline"
    ],
    "target_focus_areas": [
        "Web3 / Crypto (AI Agents, x402 payments, Solana, Base, Monad, MegaETH, ZK coprocessors)",
        "AI / ML infrastructure, verifiable inference, synthetic data, evals",
        "Open-source and developer tools",
        "FinTech / autonomous micro-commerce",
        "High-EV Bounties, Accelerators, Builder Programs, Hackathons"
    ]
}

# HackScore Weights (Sum = 100)
HACKSCORE_WEIGHTS = {
    "reward_quality": 20,
    "competition_attractiveness": 20,
    "skill_fit": 15,
    "sponsor_history": 10,
    "ecosystem_momentum": 10,
    "prize_breadth": 10,
    "participation_rewards": 5,
    "startup_potential": 5,
    "portfolio_value": 5
}

# Ecosystem Momentum Weights (Sum = 100)
ECOSYSTEM_MOMENTUM_WEIGHTS = {
    "developer_programs": 20,
    "hackathons_and_grants": 20,
    "dev_activity_acceleration": 15,
    "sdk_product_launches": 10,
    "sponsor_activity": 10,
    "social_discussion": 10,
    "funding_activity": 5,
    "competition_opportunity": 10
}

# Alert Thresholds
ALERT_LEVEL_1_NAME = "FIRST_SIGNAL"
ALERT_LEVEL_2_NAME = "CONFIRMED"
ALERT_LEVEL_3_NAME = "ACTIONABLE_EDGE"

# Actionable Edge Criteria: HackScore >= 75, SkillMatch >= 70
ACTIONABLE_EDGE_MIN_HACKSCORE = 75
ACTIONABLE_EDGE_MIN_SKILL_MATCH = 70

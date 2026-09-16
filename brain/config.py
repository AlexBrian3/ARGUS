"""
-------------------------------------------------------------------------------
ARGUS: The Hundred-Eyed Builder Intelligence Engine
Configuration and Global Settings
-------------------------------------------------------------------------------
This file holds all the settings, file paths, weights, and user preferences
used across the entire ARGUS system.
"""

from pathlib import Path

# --------------------------------------------------------------------------- #
#                             1. FILE PATHS & FOLDERS                         #
# --------------------------------------------------------------------------- #

# Find the main project directory (one level above this brain/ folder)
BASE_DIR = Path(__file__).resolve().parent.parent

# Set up the data directory where our SQLite database will live
DATA_DIR = BASE_DIR / "data"

# Set up the dashboard directory where our HTML interface will live
DASHBOARD_DIR = BASE_DIR / "dashboard"

# Make sure both folders exist on your computer (creates them if missing)
DATA_DIR.mkdir(parents=True, exist_ok=True)
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

# Path to our SQLite database file
DB_PATH = DATA_DIR / "brain.db"


# --------------------------------------------------------------------------- #
#                             2. USER PROFILE & SKILLS                        #
# --------------------------------------------------------------------------- #
# ARGUS compares every opportunity against your personal background so it only
# recommends projects where you have an unfair advantage.

USER_PROFILE = {
    "name": "Staff / Senior AI Platform Engineer",

    # Technologies you already know and write comfortably
    "primary_skills": [
        "Python",
        "FastAPI",
        "AsyncIO",
        "PyTorch",
        "vLLM",
        "Ray Serve",
        "Triton Inference Server",
        "LiteLLM",
        "LangGraph",
        "LlamaIndex",
        "Qdrant",
        "Milvus",
        "Ragas",
        "DeepEval",
        "NeMo Guardrails",
        "TypeScript",
        "React",
        "TailwindCSS",
        "Go",
        "Docker",
        "Kubernetes"
    ],

    # Code you have already built that can be copied and reused in hackathons
    "reusable_assets": [
        "hackathon-launchpad (FastAPI SSE streaming backend + React Tailwind frontend)",
        "Enterprise LLM gateway with semantic caching and smart prompt routing",
        "Multi-agent tracing with Langfuse and OpenTelemetry",
        "Automated evaluation and benchmark suite using Ragas and DeepEval",
        "High-throughput model serving cluster with KV-cache optimization"
    ],

    # The tech areas where you want to hunt for prize money and grants
    "target_focus_areas": [
        "Web3 / Crypto (AI agents, x402 payments, Solana, Base, Monad)",
        "AI / ML infrastructure (verifiable inference, evaluation pipelines)",
        "Open-source and developer tools",
        "Fintech and automated micro-payments",
        "High-prize hackathons, bounties, accelerators, and builder grants"
    ]
}


# --------------------------------------------------------------------------- #
#                       3. HACKSCORE SCORING WEIGHTS (TOTAL: 100)             #
# --------------------------------------------------------------------------- #
# How much each factor matters when deciding if an event is worth your time.

HACKSCORE_WEIGHTS = {
    "reward_quality": 20,              # How big is the total prize pool?
    "competition_attractiveness": 20,  # Is the prize-to-competitor ratio high?
    "skill_fit": 15,                   # Does it match your superpowers?
    "sponsor_history": 10,             # Do we know what the sponsors reward?
    "ecosystem_momentum": 10,          # Is this blockchain/tech heating up?
    "prize_breadth": 10,               # Are there multiple bounty tracks?
    "participation_rewards": 5,        # Do all good submissions get something?
    "startup_potential": 5,            # Can this turn into a funded startup?
    "portfolio_value": 5               # Is it impressive on your resume?
}


# --------------------------------------------------------------------------- #
#                   4. ECOSYSTEM MOMENTUM WEIGHTS (TOTAL: 100)                #
# --------------------------------------------------------------------------- #
# How we measure if a blockchain or developer platform is growing fast.

ECOSYSTEM_MOMENTUM_WEIGHTS = {
    "developer_programs": 20,          # New grants, incubator batches
    "hackathons_and_grants": 20,       # Active prize pools and competitions
    "dev_activity_acceleration": 15,   # More GitHub commits, new repos
    "sdk_product_launches": 10,        # New developer SDKs released
    "sponsor_activity": 10,            # High-profile companies sponsoring
    "social_discussion": 10,           # DevRel buzz and developer chatter
    "funding_activity": 5,             # VC investments in the ecosystem
    "competition_opportunity": 10      # High reward vs builder saturation
}


# --------------------------------------------------------------------------- #
#                             5. ALERT THRESHOLDS                             #
# --------------------------------------------------------------------------- #

# Three alert levels:
# Level 1: Early signal detected before registration is even open
ALERT_LEVEL_1_NAME = "FIRST_SIGNAL"

# Level 2: Official event confirmed and registration is live
ALERT_LEVEL_2_NAME = "CONFIRMED"

# Level 3: Unusually high expected value (Actionable Edge)
ALERT_LEVEL_3_NAME = "ACTIONABLE_EDGE"

# Minimum scores needed to trigger a Level 3 Actionable Edge alert
ACTIONABLE_EDGE_MIN_HACKSCORE = 75.0
ACTIONABLE_EDGE_MIN_SKILL_MATCH = 70.0

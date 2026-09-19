-- ARGUS Persistent Memory Schema (Engine 10)

CREATE TABLE IF NOT EXISTS ecosystems (
    slug TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL, -- L1, L2, Bitcoin L2, Decentralized AI / Compute, AI Agent Infrastructure, etc.
    momentum_score REAL NOT NULL DEFAULT 0.0,
    momentum_trajectory TEXT NOT NULL DEFAULT '→', -- ↑, →, ↓
    breakdown_scores TEXT NOT NULL DEFAULT '{}', -- JSON breakdown
    tracked_repos TEXT NOT NULL DEFAULT '[]', -- JSON array of GitHub repos
    notes TEXT,
    maturity_stage TEXT NOT NULL DEFAULT 'established', -- watchlist, emerging, established
    first_detected TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sponsors (
    slug TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    ecosystem TEXT NOT NULL,
    technology TEXT NOT NULL,
    predictability_score REAL NOT NULL DEFAULT 0.0,
    upcoming_likelihood REAL NOT NULL DEFAULT 0.0,
    previous_hackathons TEXT NOT NULL DEFAULT '[]', -- JSON array of events
    prize_amounts_total REAL DEFAULT 0.0,
    tracks TEXT NOT NULL DEFAULT '[]', -- JSON
    bounties TEXT NOT NULL DEFAULT '[]', -- JSON
    recurring_technologies TEXT NOT NULL DEFAULT '[]', -- JSON
    recurring_bounty_categories TEXT NOT NULL DEFAULT '[]', -- JSON
    common_winning_product_types TEXT NOT NULL DEFAULT '[]', -- JSON
    features_frequently_used TEXT NOT NULL DEFAULT '[]', -- JSON
    features_rarely_used TEXT NOT NULL DEFAULT '[]', -- JSON
    oversaturated_ideas TEXT NOT NULL DEFAULT '[]', -- JSON
    underserved_ideas TEXT NOT NULL DEFAULT '[]', -- JSON
    integration_difficulty TEXT DEFAULT 'Medium', -- Low, Medium, High
    documentation_quality TEXT DEFAULT 'Good', -- Poor, Moderate, Good, Exceptional
    typical_prize_distribution TEXT,
    historical_participation_rewards TEXT,
    repeat_sponsorship_frequency TEXT,
    recommended_preparation TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS opportunities (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL, -- hackathon, bounty, grant, accelerator, ideathon, builder_challenge
    organizer TEXT NOT NULL, -- ETHGlobal, Colosseum, DoraHacks, Devfolio, Devpost, Foundation, etc.
    ecosystem TEXT NOT NULL,
    registration_open INTEGER DEFAULT 1,
    registration_deadline TEXT,
    submission_deadline TEXT,
    total_prize_usd REAL DEFAULT 0.0,
    prize_breakdown TEXT NOT NULL DEFAULT '{}', -- JSON
    tracks TEXT NOT NULL DEFAULT '[]', -- JSON
    sponsors TEXT NOT NULL DEFAULT '[]', -- JSON
    participation_rewards TEXT,
    expected_competitors INTEGER DEFAULT 0,
    prize_to_competitor_ratio REAL DEFAULT 0.0,
    prob_placing REAL DEFAULT 0.0,
    prob_any_reward REAL DEFAULT 0.0,
    hack_score REAL DEFAULT 0.0,
    skill_match_score REAL DEFAULT 0.0,
    score_breakdown TEXT NOT NULL DEFAULT '{}', -- JSON
    alert_level INTEGER DEFAULT 2, -- 1, 2, 3
    status TEXT DEFAULT 'confirmed', -- unconfirmed, confirmed, active, closed
    url TEXT,
    source_tier TEXT DEFAULT 'Tier 2', -- Tier 0, Tier 1, Tier 2
    source_url TEXT,
    tags TEXT NOT NULL DEFAULT '[]', -- JSON
    recommended_build_direction TEXT,
    technologies_to_learn TEXT NOT NULL DEFAULT '[]', -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS winners (
    id TEXT PRIMARY KEY,
    opportunity_id TEXT,
    event_name TEXT NOT NULL,
    project_name TEXT NOT NULL,
    category TEXT NOT NULL,
    problem_solved TEXT,
    product_category TEXT, -- infra, consumer, devtool, defi, ai
    infra_vs_consumer TEXT, -- Infrastructure, Consumer, Hybrid
    frontend_quality TEXT, -- High, Moderate, Basic
    ux_quality TEXT,
    technical_depth TEXT, -- High, Very High, Exceptional, Moderate
    sponsor_integration_depth TEXT, -- Deep, Surface, Standard
    originality TEXT,
    demo_quality TEXT,
    github_quality TEXT,
    number_of_integrations INTEGER DEFAULT 1,
    ai_usage INTEGER DEFAULT 0,
    privacy_usage INTEGER DEFAULT 0,
    financial_use_case INTEGER DEFAULT 0,
    judges TEXT,
    prize_won TEXT,
    repo_url TEXT,
    demo_url TEXT,
    winning_patterns TEXT,
    losing_patterns_identified TEXT,
    oversaturated_category INTEGER DEFAULT 0,
    FOREIGN KEY(opportunity_id) REFERENCES opportunities(id)
);

CREATE TABLE IF NOT EXISTS signals (
    id TEXT PRIMARY KEY,
    signal_type TEXT NOT NULL, -- github_repo, rfc, devrel_teaser, blog, governance
    source_tier TEXT NOT NULL, -- Tier 0, Tier 1, Tier 2
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    raw_content TEXT,
    confidence REAL DEFAULT 0.8,
    why_it_matters TEXT,
    what_to_learn_now TEXT,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed INTEGER DEFAULT 0,
    opportunity_id TEXT
);

CREATE TABLE IF NOT EXISTS alerts (
    id TEXT PRIMARY KEY,
    alert_level INTEGER NOT NULL, -- 1 = First Signal, 2 = Confirmed, 3 = Actionable Edge
    opportunity_id TEXT,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    why_mispriced TEXT,
    action_items TEXT NOT NULL DEFAULT '[]', -- JSON
    what_to_learn_immediately TEXT,
    should_register_immediately INTEGER DEFAULT 0,
    dedupe_hash TEXT UNIQUE NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(opportunity_id) REFERENCES opportunities(id)
);

CREATE TABLE IF NOT EXISTS content_opportunities (
    id TEXT PRIMARY KEY,
    opportunity_id TEXT,
    title TEXT NOT NULL,
    topic TEXT NOT NULL,
    angle TEXT NOT NULL,
    content_potential_score REAL NOT NULL DEFAULT 0.0,
    novelty REAL DEFAULT 0.0,
    timeliness REAL DEFAULT 0.0,
    usefulness REAL DEFAULT 0.0,
    dev_interest REAL DEFAULT 0.0,
    discussion_potential REAL DEFAULT 0.0,
    search_interest REAL DEFAULT 0.0,
    proof_data TEXT,
    x_thread TEXT NOT NULL DEFAULT '[]', -- JSON
    tiktok_reels_script TEXT,
    yt_shorts_script TEXT,
    linkedin_post TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(opportunity_id) REFERENCES opportunities(id)
);

CREATE TABLE IF NOT EXISTS trends (
    id TEXT PRIMARY KEY,
    narrative_name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    discussion_velocity REAL DEFAULT 0.0,
    repository_growth REAL DEFAULT 0.0,
    grants_moving REAL DEFAULT 0.0,
    description TEXT,
    key_ecosystems TEXT NOT NULL DEFAULT '[]', -- JSON
    actionable_implications TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS benefits (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    provider TEXT NOT NULL,
    ecosystem TEXT NOT NULL,
    benefit_type TEXT NOT NULL, -- grant, fellowship, accelerator, retroactive_funding, gas_credit, other
    typical_amount_usd REAL DEFAULT 0.0,
    rolling_or_deadline TEXT NOT NULL DEFAULT 'rolling',
    eligibility_notes TEXT,
    application_url TEXT,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_verified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS job_listings (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    ecosystem_or_category TEXT NOT NULL,
    role_type TEXT NOT NULL, -- internship, entry_level, full_time, fellowship, contract
    location TEXT,
    remote INTEGER DEFAULT 1,
    compensation_notes TEXT,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    application_deadline TEXT,
    url TEXT,
    skill_tags TEXT NOT NULL DEFAULT '[]', -- JSON list
    freshness_alert_sent INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_profiles (
    id TEXT PRIMARY KEY,
    role TEXT NOT NULL,
    skills TEXT NOT NULL DEFAULT '[]',
    reusable_assets TEXT NOT NULL DEFAULT '[]',
    focus_areas TEXT NOT NULL DEFAULT '[]',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indices for rapid querying
CREATE INDEX IF NOT EXISTS idx_opp_hack_score ON opportunities(hack_score DESC);
CREATE INDEX IF NOT EXISTS idx_opp_ecosystem ON opportunities(ecosystem);
CREATE INDEX IF NOT EXISTS idx_opp_status ON opportunities(status);
CREATE INDEX IF NOT EXISTS idx_alerts_level ON alerts(alert_level);
CREATE INDEX IF NOT EXISTS idx_sponsors_pred ON sponsors(predictability_score DESC);
CREATE INDEX IF NOT EXISTS idx_ecosystems_stage ON ecosystems(maturity_stage);
CREATE INDEX IF NOT EXISTS idx_benefits_ecosystem ON benefits(ecosystem);
CREATE INDEX IF NOT EXISTS idx_benefits_type ON benefits(benefit_type);
CREATE INDEX IF NOT EXISTS idx_jobs_role ON job_listings(role_type);
CREATE INDEX IF NOT EXISTS idx_jobs_freshness ON job_listings(freshness_alert_sent, first_seen DESC);

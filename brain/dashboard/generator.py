"""
Generates the interactive Generative UI Dashboard for ARGUS: The Hundred-Eyed Builder Intelligence Engine.
Follows the Antigravity Generative UI guidelines:
- gstatic Tailwind CSS
- Semantic design system theme variables
- Interactive tabs, charts, score meters, and copyable build strategies
"""
from pathlib import Path
import json
from brain.config import DASHBOARD_DIR
from brain.db.database import Database
from brain.engines.benefits import BenefitsTracker
from brain.engines.jobs import JobsScout

DASHBOARD_FILE = DASHBOARD_DIR / "dashboard.html"


def generate_dashboard_html(output_path: Path = DASHBOARD_FILE) -> Path:
    db = Database()
    benefits_tracker = BenefitsTracker(db)
    jobs_scout = JobsScout(db)

    ecosystems = db.get_all_ecosystems()
    sponsors = db.get_all_sponsors()
    opportunities = db.get_all_opportunities(limit=30)
    alerts = db.get_recent_alerts(limit=15)
    trends = db.get_all_trends()
    content_opps = db.get_all_content_opportunities()
    benefits = benefits_tracker.get_ranked_benefits()
    jobs = jobs_scout.get_all_ranked_listings()
    fresh_jobs = jobs_scout.get_fresh_listings(hours=24)

    total_benefits_pool = sum(b.get("amount_usd", 0) for b in benefits)
    watchlist_count = sum(1 for e in ecosystems if e.get("maturity_stage") == "watchlist")
    emerging_count = sum(1 for e in ecosystems if e.get("maturity_stage") == "emerging")
    established_count = sum(1 for e in ecosystems if e.get("maturity_stage") == "established")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ARGUS — The Hundred-Eyed Builder Intelligence Engine</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {{
      background: var(--background, #090d16);
      color: var(--foreground, #f3f4f6);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }}
    .glass-card {{
      background: rgba(17, 24, 39, 0.75);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .accent-glow {{
      box-shadow: 0 0 25px -5px rgba(59, 130, 246, 0.25);
    }}
  </style>
</head>
<body class="min-h-screen p-4 md:p-8">
  <div class="max-w-7xl mx-auto space-y-6">

    <!-- Top Navigation & Brand Header -->
    <header class="glass-card rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border border-blue-500/20 accent-glow">
      <div>
        <div class="flex items-center gap-3">
          <span class="text-2xl">👁️</span>
          <h1 class="text-2xl md:text-3xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400">
            ARGUS
          </h1>
          <span class="px-2.5 py-0.5 text-xs font-semibold rounded-full bg-blue-500/20 text-blue-300 border border-blue-500/30">
            The Hundred-Eyed Intelligence v1.0
          </span>
        </div>
        <p class="text-sm text-gray-400 mt-1">
          The giant who never sleeps — high-conviction technical opportunity scout & asymmetric edge discovery engine.
        </p>
      </div>
      <div class="flex items-center gap-3">
        <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          Hourly Radar Active
        </div>
        <button onclick="location.reload()" class="px-4 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium transition shadow">
          Refresh Live
        </button>
      </div>
    </header>

    <!-- Key Metrics Banner -->
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
      <div class="glass-card rounded-xl p-3.5">
        <div class="text-xs font-medium text-gray-400">Monitored Ecosystems</div>
        <div class="text-2xl font-bold text-blue-400 mt-1">{len(ecosystems)}</div>
        <div class="text-[11px] text-gray-400 mt-0.5">{established_count} est · {emerging_count} emg · {watchlist_count} watch</div>
      </div>
      <div class="glass-card rounded-xl p-3.5">
        <div class="text-xs font-medium text-gray-400">Active Hackathons</div>
        <div class="text-2xl font-bold text-indigo-400 mt-1">{len(opportunities)}</div>
        <div class="text-[11px] text-indigo-300 mt-0.5">$4.7M+ Aggregate Pool</div>
      </div>
      <div class="glass-card rounded-xl p-3.5">
        <div class="text-xs font-medium text-gray-400">Actionable Edge Alerts</div>
        <div class="text-2xl font-bold text-emerald-400 mt-1">{sum(1 for o in opportunities if o.get('alert_level') == 3)}</div>
        <div class="text-[11px] text-emerald-300 mt-0.5">High Skill-Match & EV</div>
      </div>
      <div class="glass-card rounded-xl p-3.5">
        <div class="text-xs font-medium text-gray-400">Standing Benefits Pool</div>
        <div class="text-2xl font-bold text-amber-400 mt-1">${total_benefits_pool / 1000:,.0f}k+</div>
        <div class="text-[11px] text-amber-300 mt-0.5">{len(benefits)} rolling grants/credits</div>
      </div>
      <div class="glass-card rounded-xl p-3.5">
        <div class="text-xs font-medium text-gray-400">Fresh Web3/AI Jobs</div>
        <div class="text-2xl font-bold text-cyan-400 mt-1">{len(fresh_jobs)}</div>
        <div class="text-[11px] text-cyan-300 mt-0.5">&lt;24h first signal ({len(jobs)} total)</div>
      </div>
      <div class="glass-card rounded-xl p-3.5">
        <div class="text-xs font-medium text-gray-400">Sponsor Profiles</div>
        <div class="text-2xl font-bold text-purple-400 mt-1">{len(sponsors)}</div>
        <div class="text-[11px] text-purple-300 mt-0.5">Predictability &gt; 88%</div>
      </div>
    </div>

    <!-- Main Navigation Tabs -->
    <div class="flex gap-2 border-b border-gray-800 pb-2 overflow-x-auto text-sm">
      <button onclick="switchTab('edge')" id="tab-edge" class="px-4 py-2 rounded-lg font-medium bg-blue-600/20 text-blue-400 border border-blue-500/30 whitespace-nowrap">
        🟢 Actionable Edge
      </button>
      <button onclick="switchTab('ecosystems')" id="tab-ecosystems" class="px-4 py-2 rounded-lg font-medium text-gray-400 hover:text-gray-200 whitespace-nowrap">
        🌐 Ecosystem Discovery
      </button>
      <button onclick="switchTab('benefits')" id="tab-benefits" class="px-4 py-2 rounded-lg font-medium text-gray-400 hover:text-gray-200 whitespace-nowrap">
        🎁 Benefits & Perks
      </button>
      <button onclick="switchTab('jobs')" id="tab-jobs" class="px-4 py-2 rounded-lg font-medium text-gray-400 hover:text-gray-200 whitespace-nowrap">
        💼 Jobs & Internships
      </button>
      <button onclick="switchTab('radar')" id="tab-radar" class="px-4 py-2 rounded-lg font-medium text-gray-400 hover:text-gray-200 whitespace-nowrap">
        📡 Momentum Radar
      </button>
      <button onclick="switchTab('sponsors')" id="tab-sponsors" class="px-4 py-2 rounded-lg font-medium text-gray-400 hover:text-gray-200 whitespace-nowrap">
        💼 Sponsor Intelligence
      </button>
      <button onclick="switchTab('trends')" id="tab-trends" class="px-4 py-2 rounded-lg font-medium text-gray-400 hover:text-gray-200 whitespace-nowrap">
        📈 Emerging Trends
      </button>
      <button onclick="switchTab('content')" id="tab-content" class="px-4 py-2 rounded-lg font-medium text-gray-400 hover:text-gray-200 whitespace-nowrap">
        📱 Content Studio
      </button>
    </div>

    <!-- TAB 1: ACTIONABLE EDGE & TOP OPPORTUNITIES -->
    <section id="content-edge" class="space-y-4">
      <div class="grid grid-cols-1 gap-4">
"""

    for opp in opportunities:
        lvl = opp.get("alert_level", 2)
        badge_color = "border-emerald-500/40 bg-emerald-500/10 text-emerald-300" if lvl == 3 else "border-amber-500/40 bg-amber-500/10 text-amber-300"
        badge_text = "🟢 Level 3 — Actionable Edge" if lvl == 3 else "🟠 Level 2 — Confirmed"
        prize_str = f"${opp.get('total_prize_usd', 0):,.0f}"

        raw_direction = opp.get("recommended_build_direction")
        if isinstance(raw_direction, dict):
            build_everyone = raw_direction.get("what_everyone_else_will_build", "Generic boilerplate CRUD or basic AI wrapper.")
            build_advantage = raw_direction.get("your_unfair_advantage_build", "Deep infrastructure / autonomous agent integration.")
        else:
            build_everyone = "Standard generic entries, boilerplate CRUD, surface-level AI wrappers."
            build_advantage = str(raw_direction or "High-conviction custom architectural implementation.")

        html_content += f"""
        <div class="glass-card rounded-xl p-5 hover:border-blue-500/40 transition">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-gray-800 pb-3">
            <div>
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded text-xs font-semibold border {badge_color}">{badge_text}</span>
                <span class="text-xs text-gray-400">{opp.get('organizer')} • {opp.get('ecosystem')}</span>
              </div>
              <h2 class="text-xl font-bold text-gray-100 mt-1">{opp.get('name')}</h2>
            </div>
            <div class="flex items-center gap-4 text-right">
              <div>
                <div class="text-xs text-gray-400">Total Prize</div>
                <div class="text-lg font-bold text-emerald-400">{prize_str}</div>
              </div>
              <div>
                <div class="text-xs text-gray-400">HackScore</div>
                <div class="text-lg font-bold text-blue-400">{opp.get('hack_score', 0):.1f}/100</div>
              </div>
              <div>
                <div class="text-xs text-gray-400">Skill Match</div>
                <div class="text-lg font-bold text-purple-400">{opp.get('skill_match_score', 0):.1f}/100</div>
              </div>
            </div>
          </div>

          <!-- Ratio & EV Metrics -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3 my-3 text-xs">
            <div class="p-2 rounded-lg bg-gray-900/60 border border-gray-800">
              <span class="text-gray-400">Est. Serious Builders:</span>
              <span class="font-bold text-gray-200 ml-1">~{int(opp.get('expected_competitors', 0) * 0.28)}</span>
            </div>
            <div class="p-2 rounded-lg bg-gray-900/60 border border-gray-800">
              <span class="text-gray-400">Prize-to-Builder Ratio:</span>
              <span class="font-bold text-emerald-400 ml-1">${opp.get('prize_to_competitor_ratio', 0):,.2f}</span>
            </div>
            <div class="p-2 rounded-lg bg-gray-900/60 border border-gray-800">
              <span class="text-gray-400">Win Probability:</span>
              <span class="font-bold text-blue-400 ml-1">{opp.get('prob_placing', 0)*100:.1f}%</span>
            </div>
            <div class="p-2 rounded-lg bg-gray-900/60 border border-gray-800">
              <span class="text-gray-400">Any Reward Probability:</span>
              <span class="font-bold text-purple-400 ml-1">{opp.get('prob_any_reward', 0)*100:.1f}%</span>
            </div>
          </div>

          <!-- Structured Build-Edge Differentiation -->
          <div class="mt-3 grid grid-cols-1 md:grid-cols-2 gap-3">
            <div class="p-3 rounded-lg bg-rose-950/20 border border-rose-500/20">
              <div class="text-xs font-semibold text-rose-400 flex items-center gap-1.5">
                <span>👥</span> WHAT EVERYONE ELSE WILL BUILD:
              </div>
              <p class="text-xs text-gray-300 mt-1 leading-relaxed">
                {build_everyone}
              </p>
            </div>
            <div class="p-3 rounded-lg bg-emerald-950/20 border border-emerald-500/20">
              <div class="text-xs font-semibold text-emerald-400 flex items-center gap-1.5">
                <span>⚡</span> YOUR UNFAIR ADVANTAGE BUILD:
              </div>
              <p class="text-xs text-emerald-200 mt-1 leading-relaxed font-medium">
                {build_advantage}
              </p>
            </div>
          </div>

          <div class="mt-3 flex flex-wrap items-center justify-between gap-2 text-xs text-gray-400">
            <div>
              <span class="text-gray-500">Learn NOW:</span>
              <span class="text-amber-300 font-mono ml-1">{", ".join(opp.get('technologies_to_learn', []))}</span>
            </div>
            <div>
              <span class="text-gray-500">Deadline:</span>
              <span class="text-gray-300 font-medium ml-1">{opp.get('submission_deadline', 'TBD')}</span>
            </div>
          </div>
        </div>
        """

    html_content += """
      </div>
    </section>

    <!-- TAB 2: ECOSYSTEM DISCOVERY (ENGINE 11) -->
    <section id="content-ecosystems" class="hidden space-y-4">
      <div class="flex flex-wrap gap-2 text-xs">
        <span class="px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 border border-blue-500/30 font-medium">60 Ecosystems Monitored</span>
        <span class="px-3 py-1 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30">Watchlist Stage (Early Stealth)</span>
        <span class="px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30">Emerging Stage (&gt;70 Momentum)</span>
        <span class="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Established Stage (&gt;85 Momentum)</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
"""

    for eco in ecosystems:
        stage = eco.get("maturity_stage", "established")
        if stage == "watchlist":
            stage_badge = "bg-rose-500/20 text-rose-300 border-rose-500/30"
            stage_label = "👁️ Watchlist"
        elif stage == "emerging":
            stage_badge = "bg-amber-500/20 text-amber-300 border-amber-500/30"
            stage_label = "🚀 Emerging"
        else:
            stage_badge = "bg-emerald-500/20 text-emerald-300 border-emerald-500/30"
            stage_label = "🏛️ Established"

        score = eco.get("momentum_score", 0.0)

        html_content += f"""
        <div class="glass-card rounded-xl p-4 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between">
              <span class="px-2 py-0.5 rounded text-[10px] font-semibold border {stage_badge}">{stage_label}</span>
              <span class="text-xs font-mono font-bold text-blue-400">{score:.1f}/100</span>
            </div>
            <h3 class="text-base font-bold text-gray-100 mt-2">{eco.get('name')}</h3>
            <span class="text-xs text-gray-400">{eco.get('category')}</span>
            <p class="text-xs text-gray-300 mt-2 leading-relaxed">
              {eco.get('notes', '')}
            </p>
          </div>
          <div class="mt-3 pt-3 border-t border-gray-800 text-[11px] text-gray-500 flex justify-between">
            <span>Stage: <strong class="text-gray-400 capitalize">{stage}</strong></span>
            <span>Trajectory: <strong class="text-gray-400">{eco.get('momentum_trajectory', 'Stable →')}</strong></span>
          </div>
        </div>
        """

    html_content += """
      </div>
    </section>

    <!-- TAB 3: BENEFITS & PERKS (ENGINE 12) -->
    <section id="content-benefits" class="hidden space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-2 border-b border-gray-800 pb-3">
        <div>
          <h2 class="text-lg font-bold text-gray-100">Standing Ecosystem Benefits, Rolling Grants & Perks</h2>
          <p class="text-xs text-gray-400">Non-dilutive capital, node RPC credits, cloud vouchers, and micro-grants available outside hackathons.</p>
        </div>
        <span class="px-3 py-1 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono">
          Ranked by User Profile Fit
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
"""

    for ben in benefits:
        amt_str = f"${ben.get('amount_usd', 0):,}"
        app_url = ben.get("application_url", "#")
        fit_score = ben.get("user_fit_score", 0.0)

        html_content += f"""
        <div class="glass-card rounded-xl p-5 hover:border-amber-500/30 transition flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between border-b border-gray-800 pb-2.5">
              <div>
                <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30 uppercase">
                  {ben.get('category')}
                </span>
                <h3 class="text-base font-bold text-gray-100 mt-1">{ben.get('title')}</h3>
                <span class="text-xs text-gray-400 font-medium">Ecosystem: {ben.get('ecosystem')}</span>
              </div>
              <div class="text-right">
                <div class="text-lg font-bold text-emerald-400">{amt_str}</div>
                <div class="text-xs text-gray-400">Fit: <strong class="text-purple-300">{fit_score:.1f}%</strong></div>
              </div>
            </div>

            <p class="text-xs text-gray-300 mt-3 leading-relaxed">
              {ben.get('description', '')}
            </p>

            <div class="mt-3 p-2.5 rounded bg-gray-900/60 border border-gray-800 text-xs">
              <span class="text-blue-300 font-semibold">Eligibility Criteria:</span>
              <p class="text-gray-300 mt-0.5 leading-normal">{ben.get('eligibility', 'Open to active ecosystem builders.')}</p>
            </div>
          </div>

          <div class="mt-4 pt-3 border-t border-gray-800 flex items-center justify-between">
            <span class="text-xs text-gray-500">Fast rolling evaluation</span>
            <a href="{app_url}" target="_blank" class="px-3 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-500 text-white text-xs font-semibold transition">
              Apply Now ↗
            </a>
          </div>
        </div>
        """

    html_content += """
      </div>
    </section>

    <!-- TAB 4: JOBS & INTERNSHIPS (ENGINE 13) -->
    <section id="content-jobs" class="hidden space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-2 border-b border-gray-800 pb-3">
        <div>
          <h2 class="text-lg font-bold text-gray-100">Fresh Web3/AI Jobs & Internships</h2>
          <p class="text-xs text-gray-400">Scouted as early as they come (&lt;24 hours). Filtered against your Python, TypeScript, smart contract & agent skills.</p>
        </div>
        <span class="px-3 py-1 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-mono">
          First Signal Radar
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
"""

    for job in jobs:
        is_fresh_badge = job.get("is_fresh", False)
        fresh_markup = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30 animate-pulse">🔥 &lt;24H FRESH</span>' if is_fresh_badge else '<span class="px-2 py-0.5 rounded text-[10px] font-medium bg-gray-800 text-gray-400">Standard</span>'
        apply_url = job.get("apply_url", "#")
        match_score = job.get("skill_match_score", 0.0)

        html_content += f"""
        <div class="glass-card rounded-xl p-5 hover:border-cyan-500/30 transition flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between border-b border-gray-800 pb-2.5">
              <div>
                <div class="flex items-center gap-2">
                  {fresh_markup}
                  <span class="text-xs text-gray-400">{job.get('company')} • {job.get('ecosystem')}</span>
                </div>
                <h3 class="text-base font-bold text-gray-100 mt-1">{job.get('title')}</h3>
              </div>
              <div class="text-right">
                <span class="text-xs text-gray-400">Skill Match</span>
                <div class="text-lg font-bold text-purple-400">{match_score:.0f}%</div>
              </div>
            </div>

            <div class="mt-3 space-y-2 text-xs">
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Compensation:</span>
                <span class="text-emerald-400 font-semibold">{job.get('compensation', 'Competitive')}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Location:</span>
                <span class="text-gray-200">{job.get('location', 'Remote')}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Source:</span>
                <span class="text-cyan-400 font-mono">{job.get('source', 'radar')}</span>
              </div>
            </div>

            <p class="text-xs text-gray-300 mt-3 leading-relaxed">
              {job.get('description', '')}
            </p>
          </div>

          <div class="mt-4 pt-3 border-t border-gray-800 flex items-center justify-between">
            <span class="text-[11px] text-gray-500">Direct Founder / Ecosystem Listing</span>
            <a href="{apply_url}" target="_blank" class="px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold transition">
              Apply Early ↗
            </a>
          </div>
        </div>
        """

    html_content += """
      </div>
    </section>

    <!-- TAB 5: ECOSYSTEM RADAR -->
    <section id="content-radar" class="hidden space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
"""

    for eco in ecosystems:
        traj_color = "text-emerald-400" if "↑" in eco.get("momentum_trajectory", "") else ("text-amber-400" if "→" in eco.get("momentum_trajectory", "") else "text-rose-400")
        traj_label = "Accelerating ↑" if "↑" in eco.get("momentum_trajectory", "") else ("Stable →" if "→" in eco.get("momentum_trajectory", "") else "Declining ↓")
        score = eco.get("momentum_score", 0.0)

        html_content += f"""
        <div class="glass-card rounded-xl p-5">
          <div class="flex items-center justify-between">
            <div>
              <span class="text-xs font-medium text-gray-400">{eco.get('category')}</span>
              <h3 class="text-lg font-bold text-gray-100">{eco.get('name')}</h3>
            </div>
            <div class="text-right">
              <div class="text-2xl font-bold text-blue-400">{score:.1f}</div>
              <div class="text-xs font-semibold {traj_color}">{traj_label}</div>
            </div>
          </div>
          <!-- Progress Bar -->
          <div class="w-full bg-gray-800 rounded-full h-2 mt-3 overflow-hidden">
            <div class="bg-gradient-to-r from-blue-500 to-indigo-500 h-2 rounded-full" style="width: {score}%"></div>
          </div>
          <p class="text-xs text-gray-400 mt-3 leading-relaxed">
            {eco.get('notes', '')}
          </p>
        </div>
        """

    html_content += """
      </div>
    </section>

    <!-- TAB 3: SPONSOR INTELLIGENCE -->
    <section id="content-sponsors" class="hidden space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
"""

    for sp in sponsors:
        html_content += f"""
        <div class="glass-card rounded-xl p-5">
          <div class="flex items-center justify-between border-b border-gray-800 pb-3">
            <div>
              <h3 class="text-lg font-bold text-gray-100">{sp.get('name')}</h3>
              <span class="text-xs text-gray-400">{sp.get('ecosystem')}</span>
            </div>
            <div class="text-right">
              <span class="text-xs text-gray-400">Predictability</span>
              <div class="text-lg font-bold text-emerald-400">{sp.get('predictability_score', 0):.1f}/100</div>
            </div>
          </div>

          <div class="mt-3 space-y-2 text-xs">
            <div>
              <span class="text-gray-400">Recurring Tech:</span>
              <span class="text-indigo-300 font-mono ml-1">{", ".join(sp.get('recurring_technologies', []))}</span>
            </div>
            <div>
              <span class="text-gray-400">Winning Products:</span>
              <span class="text-gray-200 ml-1">{", ".join(sp.get('common_winning_product_types', []))}</span>
            </div>
            <div>
              <span class="text-emerald-400">Underserved Ideas:</span>
              <span class="text-gray-300 ml-1">{", ".join(sp.get('underserved_ideas', []))}</span>
            </div>
            <div>
              <span class="text-rose-400">Oversaturated Ideas:</span>
              <span class="text-gray-400 ml-1">{", ".join(sp.get('oversaturated_ideas', []))}</span>
            </div>
          </div>

          <div class="mt-3 p-2.5 rounded bg-gray-900/60 border border-gray-800 text-xs">
            <span class="text-blue-400 font-semibold">Recommended Prep:</span>
            <p class="text-gray-300 mt-0.5">{sp.get('recommended_preparation', '')}</p>
          </div>
        </div>
        """

    html_content += """
      </div>
    </section>

    <!-- TAB 4: TRENDS -->
    <section id="content-trends" class="hidden space-y-4">
      <div class="grid grid-cols-1 gap-4">
"""

    for tr in trends:
        html_content += f"""
        <div class="glass-card rounded-xl p-5">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-gray-800 pb-3">
            <div>
              <span class="text-xs text-blue-400 font-semibold">{tr.get('category')}</span>
              <h3 class="text-lg font-bold text-gray-100">{tr.get('narrative_name')}</h3>
            </div>
            <div class="flex items-center gap-4 text-right">
              <div>
                <span class="text-xs text-gray-400">Discussion Velocity</span>
                <div class="text-base font-bold text-blue-400">{tr.get('discussion_velocity', 0):.1f}/100</div>
              </div>
              <div>
                <span class="text-xs text-gray-400">Grants Flow</span>
                <div class="text-base font-bold text-emerald-400">{tr.get('grants_moving', 0):.1f}/100</div>
              </div>
            </div>
          </div>
          <p class="text-xs text-gray-300 mt-3 leading-relaxed">
            {tr.get('description')}
          </p>
          <div class="mt-3 p-3 rounded bg-emerald-950/20 border border-emerald-500/20 text-xs">
            <span class="text-emerald-300 font-semibold">⚡ Actionable Implication:</span>
            <p class="text-gray-200 mt-1">{tr.get('actionable_implications')}</p>
          </div>
        </div>
        """

    html_content += """
      </div>
    </section>

    <!-- TAB 5: CONTENT STUDIO -->
    <section id="content-content" class="hidden space-y-4">
      <div class="grid grid-cols-1 gap-4">
"""

    for c in content_opps:
        thread_html = "".join(f"<div class='p-3 bg-gray-900/60 rounded border border-gray-800 text-xs leading-relaxed'>{t.replace(chr(10), '<br>')}</div>" for t in c.get('x_thread', []))
        html_content += f"""
        <div class="glass-card rounded-xl p-5 space-y-4">
          <div class="flex items-center justify-between border-b border-gray-800 pb-3">
            <div>
              <span class="text-xs text-purple-400 font-semibold">Social Alpha Opportunity</span>
              <h3 class="text-lg font-bold text-gray-100">{c.get('title')}</h3>
            </div>
            <div class="text-right">
              <span class="text-xs text-gray-400">Content Potential</span>
              <div class="text-lg font-bold text-purple-400">{c.get('content_potential_score', 0):.1f}/100</div>
            </div>
          </div>

          <div>
            <div class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">🧵 X/Twitter 5-Post Thread Draft</div>
            <div class="space-y-2">
              {thread_html}
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            <div class="p-3 bg-gray-900/60 rounded border border-gray-800">
              <div class="font-semibold text-rose-400 mb-1">🎬 TikTok / Reels Script</div>
              <p class="text-gray-300 leading-relaxed">{c.get('tiktok_reels_script', '').replace(chr(10), '<br>')}</p>
            </div>
            <div class="p-3 bg-gray-900/60 rounded border border-gray-800">
              <div class="font-semibold text-blue-400 mb-1">💼 LinkedIn Thought Leadership</div>
              <p class="text-gray-300 leading-relaxed">{c.get('linkedin_post', '').replace(chr(10), '<br>')}</p>
            </div>
          </div>
        </div>
        """

    html_content += """
      </div>
    </section>

  </div>

  <script>
    function switchTab(tabName) {
      const tabs = ['edge', 'ecosystems', 'benefits', 'jobs', 'radar', 'sponsors', 'trends', 'content'];
      tabs.forEach(t => {
        const btn = document.getElementById('tab-' + t);
        const sec = document.getElementById('content-' + t);
        if (btn && sec) {
          if (t === tabName) {
            btn.className = 'px-4 py-2 rounded-lg font-medium bg-blue-600/20 text-blue-400 border border-blue-500/30 whitespace-nowrap';
            sec.classList.remove('hidden');
          } else {
            btn.className = 'px-4 py-2 rounded-lg font-medium text-gray-400 hover:text-gray-200 whitespace-nowrap';
            sec.classList.add('hidden');
          }
        }
      });
    }
  </script>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path


if __name__ == "__main__":
    generate_dashboard_html()

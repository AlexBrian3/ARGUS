"""
-------------------------------------------------------------------------------
ARGUS COMMAND LINE INTERFACE (CLI)
-------------------------------------------------------------------------------
The central command center for ARGUS.

Available Commands:
    python -m brain.cli scan                       # Run full intelligence scan
    python -m brain.cli edge                       # Show top Actionable Edge opportunities
    python -m brain.cli radar                      # View Ecosystem Momentum Leaderboard
    python -m brain.cli ecosystems [--stage stage] # View ecosystems by stage (watchlist/emerging/established)
    python -m brain.cli benefits [slug]            # View standing grants, perks, gas credits
    python -m brain.cli jobs [--fresh]             # View fresh Web3/AI engineering jobs & internships
    python -m brain.cli sponsor [slug]             # View Sponsor Intelligence Cards
    python -m brain.cli winners                    # Study winning vs losing patterns
    python -m brain.cli opportunities              # List all scored opportunities
    python -m brain.cli content [slug]             # Generate ready-to-post social content
    python -m brain.cli trends                     # View emerging technical narratives
    python -m brain.cli dashboard                  # Regenerate interactive HTML dashboard
    python -m brain.cli telegram [test|push|summary] # Test or push alerts to Telegram
"""

import sys
import argparse

# Ensure clean UTF-8 text output on Windows Command Prompt / PowerShell
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from brain.db.database import Database
from brain.engines.radar import EcosystemRadar
from brain.engines.sponsor import SponsorIntelligence
from brain.engines.winners import WinnerAnalyzer
from brain.engines.scout import OpportunityScout
from brain.engines.content import SocialContentEngine
from brain.engines.trends import TrendDetector
from brain.engines.benefits import BenefitsTracker
from brain.engines.jobs import JobsScout
from brain.dashboard.generator import generate_dashboard_html


# --------------------------------------------------------------------------- #
#                        COMMAND 1: ECOSYSTEM RADAR                           #
# --------------------------------------------------------------------------- #

def cmd_radar(args):
    """Displays the Ecosystem Momentum Leaderboard and stealth opportunities."""
    db = Database()
    radar = EcosystemRadar(db)
    leaderboard = radar.get_leaderboard()

    print("\n" + "=" * 78)
    print(" 📡 ECOSYSTEM RADAR — MOMENTUM LEADERBOARD")
    print("=" * 78)
    print(f"{'Ecosystem':<22} | {'Category':<20} | {'Score':<6} | {'Trajectory':<10}")
    print("-" * 78)

    for eco in leaderboard:
        traj_str = eco["momentum_trajectory"]
        traj_label = "Accelerating ↑" if "↑" in traj_str else ("Stable →" if "→" in traj_str else "Declining ↓")
        print(f"{eco['name']:<22} | {eco['category']:<20} | {eco['momentum_score']:<6.1f} | {traj_label:<10}")

    stealth = radar.detect_stealth_opportunities()
    if stealth:
        print("\n⚡ STEALTH MOMENTUM DETECTED (Pre-Major Hackathon Signals):")
        for s in stealth:
            print(f"  • {s['name']}: Momentum {s['momentum_score']}/100 — {s['notes']}")

    print("=" * 78 + "\n")


# --------------------------------------------------------------------------- #
#                        COMMAND 2: SPONSOR INTELLIGENCE                      #
# --------------------------------------------------------------------------- #

def cmd_sponsor(args):
    """Displays Sponsor Intelligence Cards showing what sponsors repeatedly reward."""
    db = Database()
    sponsor_engine = SponsorIntelligence(db)

    # If the user asked for a specific sponsor (e.g. "python -m brain.cli sponsor world")
    if args.slug:
        card = sponsor_engine.get_sponsor_card(args.slug)
        if not card:
            print(f"[!] Sponsor '{args.slug}' was not found in database.")
            return

        print("\n" + "=" * 78)
        print(f" 💼 SPONSOR INTELLIGENCE CARD: {card['name'].upper()}")
        print("=" * 78)
        print(f"Ecosystem           : {card['ecosystem']}")
        print(f"Technology          : {card['technology']}")
        print(f"Predictability Score: {card['predictability_score']}/100")
        print(f"Upcoming Likelihood : {card['upcoming_likelihood']}/100")
        print(f"Recurring Tech      : {', '.join(card['recurring_technologies'])}")
        print(f"Frequently Rewarded : {', '.join(card['recurring_bounty_categories'])}")
        print(f"Winning Products    : {', '.join(card['common_winning_product_types'])}")
        print(f"Rarely Used Features: {', '.join(card['features_rarely_used'])}")
        print(f"Oversaturated Ideas : {', '.join(card['oversaturated_ideas'])}")
        print(f"Underserved Niches  : {', '.join(card['underserved_ideas'])}")
        print(f"Documentation       : {card['documentation_quality']} | Integration: {card['integration_difficulty']}")
        print("-" * 78)
        print(f"PROACTIVE PREPARATION ADVISORY:\n{card['recommended_preparation']}")
        print("=" * 78 + "\n")

    # Otherwise, show a summary table of all sponsors
    else:
        sponsors = sponsor_engine.get_all_sponsor_cards()
        print("\n" + "=" * 78)
        print(" 💼 PERSISTENT SPONSOR INTELLIGENCE CARDS")
        print("=" * 78)
        print(f"{'Sponsor':<24} | {'Ecosystem':<24} | {'Predictability':<14} | {'Upcoming Likelihood'}")
        print("-" * 78)
        for s in sponsors:
            print(f"{s['name']:<24} | {s['ecosystem']:<24} | {s['predictability_score']:<14.1f} | {s['upcoming_likelihood']:.1f}/100")
        print("=" * 78 + "\n")


# --------------------------------------------------------------------------- #
#                        COMMAND 3: WINNER ANALYSIS                           #
# --------------------------------------------------------------------------- #

def cmd_winners(args):
    """Surfaces recurring winning patterns, losing mistakes, and underexplored niches."""
    analyzer = WinnerAnalyzer()
    res = analyzer.analyze_event_patterns(args.event)

    print("\n" + "=" * 78)
    print(f" 🏆 HISTORICAL WINNER PATTERN ANALYSIS {f'({args.event})' if args.event else ''}")
    print("=" * 78)
    print(f"Total Projects Analyzed   : {res.get('total_analyzed', '50+')}")
    print(f"AI Usage Rate             : {res.get('ai_integration_rate')}")
    print(f"Financial Use-Case Rate   : {res.get('financial_use_case_rate')}")
    print(f"Average Integrations      : {res.get('average_sponsor_integrations')}")
    print("-" * 78)
    print("🏅 WINNING PATTERNS:")
    for wp in res.get("winner_patterns", []):
        print(f"  ✓ {wp}")
    print("\n❌ COMMON LOSING PATTERNS:")
    for lp in res.get("common_losing_patterns", []):
        print(f"  ✗ {lp}")
    print("\n⚠️ OVERSATURATED IDEAS (AVOID):")
    for osi in res.get("oversaturated_ideas", []):
        print(f"  - {osi}")
    print("\n💎 UNDEREXPLORED IDEAS (UNFAIR EDGE):")
    for uei in res.get("underexplored_ideas", []):
        print(f"  + {uei}")
    print("\n🛠️ TECHNOLOGIES TO LEARN BEFORE ENTERING:")
    for ttl in res.get("technologies_to_learn", []):
        print(f"  → {ttl}")
    print("=" * 78 + "\n")


# --------------------------------------------------------------------------- #
#                        COMMAND 4: ALL OPPORTUNITIES                         #
# --------------------------------------------------------------------------- #

def cmd_opportunities(args):
    """Lists all stored opportunities ranked by HackScore."""
    db = Database()
    opps = db.get_all_opportunities(limit=args.limit)

    print("\n" + "=" * 88)
    print(" 🎯 OPPORTUNITY RADAR (RANKED BY HACKSCORE)")
    print("=" * 88)
    print(f"{'Opportunity':<32} | {'Prize':<12} | {'HackScore':<10} | {'SkillMatch':<10} | {'Alert Level'}")
    print("-" * 88)

    for op in opps:
        lvl = op["alert_level"]
        lvl_badge = "🟢 Level 3 (Edge)" if lvl == 3 else ("🟠 Level 2" if lvl == 2 else "🔴 Level 1")
        prize_str = f"${op['total_prize_usd']:,.0f}"
        print(f"{op['name'][:32]:<32} | {prize_str:<12} | {op['hack_score']:<10.1f} | {op['skill_match_score']:<10.1f} | {lvl_badge}")

    print("=" * 88 + "\n")


# --------------------------------------------------------------------------- #
#                        COMMAND 5: ACTIONABLE EDGE                           #
# --------------------------------------------------------------------------- #

def cmd_edge(args):
    """Displays only Level 3 Actionable Edge opportunities with tailored build directions."""
    db = Database()
    opps = db.get_all_opportunities(limit=50)
    edge_opps = [o for o in opps if o["alert_level"] == 3]

    print("\n" + "=" * 88)
    print(" 🟢 ACTIVE LEVEL 3 ACTIONABLE EDGE OPPORTUNITIES")
    print("=" * 88)

    for op in edge_opps:
        print(f"\n⚡ {op['name'].upper()}")
        print(f"   Organizer: {op['organizer']} | Ecosystem: {op['ecosystem']}")
        print(f"   Total Prize: ${op['total_prize_usd']:,.0f} | Expected Competitors: {op['expected_competitors']}")
        print(f"   Prize-to-Competitor Ratio: ${op['prize_to_competitor_ratio']:,.2f} per serious builder")
        print(f"   Probability of Placing: {op['prob_placing']*100:.1f}% | Probability of Any Reward: {op['prob_any_reward']*100:.1f}%")
        print(f"   HACKSCORE: {op['hack_score']}/100 | SKILL MATCH: {op['skill_match_score']}/100")
        print(f"   Deadline: {op['submission_deadline']}")
        direction = op.get("recommended_build_direction")
        if isinstance(direction, dict):
            print("   Actionable Build Direction:")
            print(f"     • What everyone else will build: {direction.get('what_everyone_else_will_build')}")
            print(f"     • Your unfair advantage build  : {direction.get('your_unfair_advantage_build')}")
        else:
            print(f"   Actionable Build Direction:\n   {direction}")
        print(f"   Technologies to Learn NOW: {', '.join(op['technologies_to_learn'])}")

    print("\n" + "=" * 88 + "\n")


# --------------------------------------------------------------------------- #
#                        COMMAND 6: SOCIAL CONTENT STUDIO                     #
# --------------------------------------------------------------------------- #

def cmd_content(args):
    """Generates viral social media thread and video drafts for an opportunity."""
    db = Database()
    content_engine = SocialContentEngine(db)

    if args.slug:
        opp = db.get_opportunity(args.slug)
        if not opp:
            print(f"[!] Opportunity '{args.slug}' was not found.")
            return

        pkg = content_engine.generate_content_package(opp)
        print("\n" + "=" * 80)
        print(f" 📱 CONTENT OPPORTUNITY STUDIO: {pkg['title']}")
        print("=" * 80)
        print(f"Content Potential Score: {pkg['content_potential_score']}/100")
        print("\n--- [X/TWITTER THREAD DRAFT] ---")
        for tweet in pkg["x_thread"]:
            print(f"\n{tweet}")
        print("\n--- [TIKTOK / REELS SCRIPT] ---")
        print(pkg["tiktok_reels_script"])
        print("\n--- [LINKEDIN POST] ---")
        print(pkg["linkedin_post"])
        print("=" * 80 + "\n")

    else:
        pkgs = content_engine.get_all_content_opportunities()
        print("\n" + "=" * 80)
        print(" 📱 SOCIAL CONTENT INTELLIGENCE OPPORTUNITIES")
        print("=" * 80)
        for p in pkgs:
            print(f"• [{p['content_potential_score']}/100] {p['title']} ({p['topic']})")
        print("=" * 80 + "\n")


# --------------------------------------------------------------------------- #
#                        COMMAND 7: TREND DETECTION                           #
# --------------------------------------------------------------------------- #

def cmd_trends(args):
    """Displays hot emerging technical narratives ranked by discussion velocity."""
    detector = TrendDetector()
    trends = detector.get_narrative_velocity()

    print("\n" + "=" * 80)
    print(" 📈 EMERGING TECHNICAL NARRATIVES & TREND DETECTION")
    print("=" * 80)
    print(f"{'Narrative':<36} | {'Category':<20} | {'Velocity':<8} | {'Grants Flow'}")
    print("-" * 80)

    for t in trends:
        print(f"{t['narrative_name'][:36]:<36} | {t['category'][:20]:<20} | {t['discussion_velocity']:<8.1f} | {t['grants_moving']:.1f}/100")
        print(f"  → Actionable: {t['actionable_implications']}\n")

    print("=" * 80 + "\n")


# --------------------------------------------------------------------------- #
#                        COMMAND 8: FULL INTELLIGENCE SCAN                    #
# --------------------------------------------------------------------------- #

def cmd_scan(args):
    """Runs a complete scan cycle and refreshes the HTML dashboard."""
    scout = OpportunityScout()
    print("[SCAN] Executing ARGUS intelligence scan...")
    result = scout.run_full_scan()
    print(f"[SUCCESS] Scanned {result['total_opportunities_scanned']} opportunities. {result['new_alerts_fired']} new alerts triggered.")
    dashboard_path = generate_dashboard_html()
    print(f"[SUCCESS] Updated Generative UI Dashboard at {dashboard_path}")


# --------------------------------------------------------------------------- #
#                        COMMAND 9: REGENERATE DASHBOARD                      #
# --------------------------------------------------------------------------- #

def cmd_dashboard(args):
    """Regenerates the interactive HTML dashboard."""
    path = generate_dashboard_html()
    print(f"[DASHBOARD] Generated dashboard at: {path}")


# --------------------------------------------------------------------------- #
#                        COMMAND 10: TELEGRAM BOT                             #
# --------------------------------------------------------------------------- #

def cmd_telegram(args):
    """Tests connection or pushes alerts to your Telegram chat."""
    from brain import telegram_bot

    if not telegram_bot.is_configured():
        print("[TELEGRAM] Bot is not configured!")
        print("  1. Message @BotFather on Telegram -> /newbot -> copy your token")
        print("  2. Send any message to your new bot")
        print("  3. Visit https://api.telegram.org/bot<TOKEN>/getUpdates to find your chat_id")
        print("  4. Add them to .env in the project root:")
        print("     TELEGRAM_BOT_TOKEN=your_token")
        print("     TELEGRAM_CHAT_ID=your_chat_id")
        return

    # Test the connection
    if args.action == "test":
        print("[TELEGRAM] Sending test message...")
        ok = telegram_bot.send_message(
            "<b>👁️ ARGUS — CONNECTION TEST</b>\n\n"
            "Your Telegram integration is working.\n"
            "High-conviction alerts will be dispatched here automatically."
        )
        if ok:
            print("[TELEGRAM] Test message sent successfully! Check your Telegram.")
        else:
            print("[TELEGRAM] Failed to send. Check your token and chat ID.")

    # Push all Level 3 Edge opportunities
    elif args.action == "push":
        db = Database()
        opps = db.get_all_opportunities(limit=10)
        edge_opps = [o for o in opps if o.get("alert_level") == 3]

        if not edge_opps:
            print("[TELEGRAM] No Level 3 Actionable Edge opportunities to push.")
            return

        print(f"[TELEGRAM] Pushing {len(edge_opps)} Actionable Edge opportunities...")
        for opp in edge_opps:
            msg = telegram_bot.format_actionable_edge(opp)
            ok = telegram_bot.send_message(msg)
            status = "sent" if ok else "FAILED"
            print(f"  [{status}] {opp.get('name')}")

    # Send a digest summary
    elif args.action == "summary":
        db = Database()
        opps = db.get_all_opportunities(limit=25)
        alerts = db.get_recent_alerts(limit=10)
        edge_count = sum(1 for o in opps if o.get("alert_level") == 3)

        summary = telegram_bot.format_hourly_summary(
            total_scanned=len(opps),
            edge_count=edge_count,
            new_alerts=alerts[:5],
            top_opportunities=opps[:5]
        )
        ok = telegram_bot.send_message(summary)
        if ok:
            print("[TELEGRAM] Summary digest sent!")
        else:
            print("[TELEGRAM] Failed to send summary.")


# --------------------------------------------------------------------------- #
#                        COMMAND 11: ECOSYSTEMS DISCOVERY                     #
# --------------------------------------------------------------------------- #

def cmd_ecosystems(args):
    """Displays ecosystems filtered by maturity stage (watchlist, emerging, established)."""
    db = Database()
    radar = EcosystemRadar(db)
    stage = getattr(args, "stage", None)
    ecosystems = radar.get_ecosystems_by_stage(stage)

    stage_title = stage.upper() if stage else "ALL MATURITY STAGES"
    print("\n" + "=" * 88)
    print(f" 🌐 ECOSYSTEM DISCOVERY RADAR — {stage_title}")
    print("=" * 88)
    print(f"{'Ecosystem':<24} | {'Stage':<12} | {'Category':<20} | {'Momentum':<8}")
    print("-" * 88)

    for eco in ecosystems:
        stage_badge = eco.get("maturity_stage", "established")
        print(f"{eco['name']:<24} | {stage_badge:<12} | {eco['category']:<20} | {eco['momentum_score']:<8.1f}")
        if eco.get("notes"):
            print(f"   ↳ Notes: {eco['notes']}")

    print("=" * 88 + "\n")


# --------------------------------------------------------------------------- #
#                        COMMAND 12: BENEFITS & PERKS                         #
# --------------------------------------------------------------------------- #

def cmd_benefits(args):
    """Displays standing grants, gas credits, and foundation perks ranked by user fit."""
    db = Database()
    tracker = BenefitsTracker(db)

    if getattr(args, "slug", None):
        # Look up specific benefit
        benefit = db.get_benefit(args.slug)
        if not benefit:
            print(f"[!] Benefit '{args.slug}' was not found in database.")
            return

        category = benefit.get('category') or benefit.get('benefit_type', 'grant')
        print("\n" + "=" * 80)
        print(f" 🎁 BENEFIT INTELLIGENCE CARD: {benefit['title'].upper()}")
        print("=" * 80)
        print(f"Ecosystem     : {benefit['ecosystem']}")
        print(f"Category      : {category}")
        print(f"Amount        : ${benefit['amount_usd']:,} USD")
        print(f"Application   : {benefit.get('application_url', 'N/A')}")
        print("-" * 80)
        print(f"Description   :\n{benefit.get('description', 'N/A')}")
        print(f"\nEligibility   :\n{benefit.get('eligibility', 'N/A')}")
        print("=" * 80 + "\n")
    else:
        ranked = tracker.get_ranked_benefits()
        print("\n" + "=" * 88)
        print(" 🎁 STANDING BENEFITS & PERKS (RANKED BY USER FIT)")
        print("=" * 88)
        print(f"{'Title':<30} | {'Ecosystem':<16} | {'Category':<14} | {'Amount':<10} | {'Fit Score'}")
        print("-" * 88)
        for b in ranked:
            amt_str = f"${b.get('amount_usd', 0):,}"
            cat_str = b.get('category') or b.get('benefit_type', 'grant')
            title_str = b.get('title') or b.get('name', 'Benefit')
            eco_str = b.get('ecosystem', 'Web3')
            print(f"{title_str[:30]:<30} | {eco_str[:16]:<16} | {cat_str[:14]:<14} | {amt_str:<10} | {b.get('user_fit_score', 0):.1f}/100")
        print("=" * 88 + "\n")


# --------------------------------------------------------------------------- #
#                        COMMAND 13: JOBS & INTERNSHIPS                       #
# --------------------------------------------------------------------------- #

def cmd_jobs(args):
    """Displays fresh Web3/AI engineering jobs and internships ranked by user skills."""
    db = Database()
    scout = JobsScout(db)
    is_fresh = getattr(args, "fresh", False)

    if is_fresh:
        jobs = scout.get_fresh_listings(hours=24)
        header_title = "FRESH ROLES (LAST 24 HOURS)"
    else:
        jobs = scout.get_all_ranked_listings()
        header_title = "ALL OPEN ROLES (RANKED BY SKILL FIT)"

    print("\n" + "=" * 92)
    print(f" 💼 JOBS & INTERNSHIPS SCOUT — {header_title}")
    print("=" * 92)
    print(f"{'Role':<32} | {'Company':<18} | {'Ecosystem':<14} | {'Match':<8} | {'Source'}")
    print("-" * 92)

    if not jobs:
        print("  No listings found matching your criteria.")
    else:
        for j in jobs:
            match_str = f"{j.get('skill_match_score', 0):.0f}%"
            eco_str = j.get('ecosystem') or j.get('ecosystem_or_category', 'Web3')
            comp_str = j.get('compensation') or j.get('compensation_notes', 'Competitive')
            apply_str = j.get('apply_url') or j.get('url', 'N/A')
            print(f"{j['title'][:32]:<32} | {j['company'][:18]:<18} | {eco_str[:14]:<14} | {match_str:<8} | {j.get('source', 'radar')}")
            print(f"   ↳ Compensation: {comp_str} | Apply: {apply_str}")

    print("=" * 92 + "\n")


# --------------------------------------------------------------------------- #
#                        MAIN ARGPARSE ROUTER                                 #
# --------------------------------------------------------------------------- #

def main():
    """Main CLI entry point that parses user flags and runs the selected command."""
    parser = argparse.ArgumentParser(
        description="ARGUS CLI — The Hundred-Eyed Builder Intelligence Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: radar
    subparsers.add_parser("radar", help="View Ecosystem Momentum Radar")

    # Command: ecosystems
    p_eco = subparsers.add_parser("ecosystems", help="View ecosystems by maturity stage (watchlist, emerging, established)")
    p_eco.add_argument("--stage", choices=["watchlist", "emerging", "established"], help="Filter by maturity stage")

    # Command: benefits
    p_ben = subparsers.add_parser("benefits", help="View standing ecosystem grants, credits, and perks")
    p_ben.add_argument("slug", nargs="?", help="Specific benefit slug to view in detail")

    # Command: jobs
    p_job = subparsers.add_parser("jobs", help="View Web3/AI engineering jobs and internships")
    p_job.add_argument("--fresh", action="store_true", help="Filter for roles posted in the last 24 hours")

    # Command: sponsor
    p_sp = subparsers.add_parser("sponsor", help="View Sponsor Intelligence Cards")
    p_sp.add_argument("slug", nargs="?", help="Specific sponsor slug (e.g. world, dynamic, pyth-network)")

    # Command: winners
    p_win = subparsers.add_parser("winners", help="View historical winner & losing patterns")
    p_win.add_argument("--event", "-e", help="Filter by event name")

    # Command: opportunities
    p_opp = subparsers.add_parser("opportunities", help="List scored opportunities")
    p_opp.add_argument("--limit", "-n", type=int, default=15, help="Number of opportunities to show")

    # Command: edge
    subparsers.add_parser("edge", help="Show active Level 3 Actionable Edge opportunities")

    # Command: content
    p_cnt = subparsers.add_parser("content", help="Generate or view social content opportunities")
    p_cnt.add_argument("slug", nargs="?", help="Opportunity slug to generate content for")

    # Command: trends
    subparsers.add_parser("trends", help="Show technical narrative trend detection")

    # Command: scan
    subparsers.add_parser("scan", help="Run full intelligence ingestion & scoring cycle")

    # Command: dashboard
    subparsers.add_parser("dashboard", help="Regenerate interactive Generative UI dashboard")

    # Command: telegram
    p_tg = subparsers.add_parser("telegram", help="Telegram bot: test connection, push alerts, or send summary")
    p_tg.add_argument(
        "action",
        choices=["test", "push", "summary"],
        help="test = verify connection | push = send all Edge alerts | summary = send digest"
    )

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    commands = {
        "radar": cmd_radar,
        "ecosystems": cmd_ecosystems,
        "benefits": cmd_benefits,
        "jobs": cmd_jobs,
        "sponsor": cmd_sponsor,
        "winners": cmd_winners,
        "opportunities": cmd_opportunities,
        "edge": cmd_edge,
        "content": cmd_content,
        "trends": cmd_trends,
        "scan": cmd_scan,
        "dashboard": cmd_dashboard,
        "telegram": cmd_telegram
    }

    cmd_fn = commands.get(args.command)
    if cmd_fn:
        cmd_fn(args)


if __name__ == "__main__":
    main()

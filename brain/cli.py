"""
Command Line Interface for ARGUS: The Hundred-Eyed Builder Intelligence Engine.
Usage:
    python -m brain.cli scan
    python -m brain.cli radar
    python -m brain.cli sponsor [slug]
    python -m brain.cli winners [event]
    python -m brain.cli opportunities
    python -m brain.cli edge
    python -m brain.cli content [slug]
    python -m brain.cli trends
    python -m brain.cli dashboard
    python -m brain.cli telegram [test|push|summary]
"""
import sys
import argparse
import json

# Ensure UTF-8 output on Windows console
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
from brain.engines.alerts import AlertEngine
from brain.engines.content import SocialContentEngine
from brain.engines.trends import TrendDetector
from brain.dashboard.generator import generate_dashboard_html


def cmd_radar(args):
    db = Database()
    radar = EcosystemRadar(db)
    leaderboard = radar.get_leaderboard()

    print("\n" + "=" * 78)
    print(" 📡 ECOSYSTEM RADAR — MOMENTUM LEADERBOARD")
    print("=" * 78)
    print(f"{'Ecosystem':<22} | {'Category':<20} | {'Score':<6} | {'Trajectory':<10}")
    print("-" * 78)
    for eco in leaderboard:
        traj_str = eco['momentum_trajectory']
        traj_label = "Accelerating ↑" if "↑" in traj_str else ("Stable →" if "→" in traj_str else "Declining ↓")
        print(f"{eco['name']:<22} | {eco['category']:<20} | {eco['momentum_score']:<6.1f} | {traj_label:<10}")

    stealth = radar.detect_stealth_opportunities()
    if stealth:
        print("\n⚡ STEALTH MOMENTUM DETECTED (Pre-Major Hackathon Signals):")
        for s in stealth:
            print(f"  • {s['name']}: Momentum {s['momentum_score']}/100 — {s['notes']}")
    print("=" * 78 + "\n")


def cmd_sponsor(args):
    db = Database()
    sponsor_engine = SponsorIntelligence(db)

    if args.slug:
        card = sponsor_engine.get_sponsor_card(args.slug)
        if not card:
            print(f"[!] Sponsor '{args.slug}' not found.")
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


def cmd_winners(args):
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
    print("\n⚠️ OVERSATURATED IDEAS:")
    for osi in res.get("oversaturated_ideas", []):
        print(f"  - {osi}")
    print("\n💎 UNDEREXPLORED IDEAS (UNFAIR EDGE):")
    for uei in res.get("underexplored_ideas", []):
        print(f"  + {uei}")
    print("\n🛠️ TECHNOLOGIES TO LEARN BEFORE ENTERING:")
    for ttl in res.get("technologies_to_learn", []):
        print(f"  → {ttl}")
    print("=" * 78 + "\n")


def cmd_opportunities(args):
    db = Database()
    opps = db.get_all_opportunities(limit=args.limit)

    print("\n" + "=" * 88)
    print(" 🎯 OPPORTUNITY RADAR (RANKED BY HACKSCORE)")
    print("=" * 88)
    print(f"{'Opportunity':<32} | {'Prize':<12} | {'HackScore':<10} | {'SkillMatch':<10} | {'Alert Level'}")
    print("-" * 88)
    for op in opps:
        lvl = op['alert_level']
        lvl_badge = "🟢 Level 3 (Edge)" if lvl == 3 else ("🟠 Level 2" if lvl == 2 else "🔴 Level 1")
        prize_str = f"${op['total_prize_usd']:,.0f}"
        print(f"{op['name'][:32]:<32} | {prize_str:<12} | {op['hack_score']:<10.1f} | {op['skill_match_score']:<10.1f} | {lvl_badge}")
    print("=" * 88 + "\n")


def cmd_edge(args):
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
        print(f"   Actionable Build Direction:\n   {op['recommended_build_direction']}")
        print(f"   Technologies to Learn NOW: {', '.join(op['technologies_to_learn'])}")
    print("\n" + "=" * 88 + "\n")


def cmd_content(args):
    db = Database()
    content_engine = SocialContentEngine(db)

    if args.slug:
        opp = db.get_opportunity(args.slug)
        if not opp:
            print(f"[!] Opportunity '{args.slug}' not found.")
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


def cmd_trends(args):
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


def cmd_scan(args):
    scout = OpportunityScout()
    print("[SCAN] Executing ARGUS intelligence scan...")
    result = scout.run_full_scan()
    print(f"[SUCCESS] Scanned {result['total_opportunities_scanned']} opportunities. {result['new_alerts_fired']} new alerts triggered.")
    dashboard_path = generate_dashboard_html()
    print(f"[SUCCESS] Updated Generative UI Dashboard at {dashboard_path}")


def cmd_dashboard(args):
    path = generate_dashboard_html()
    print(f"[DASHBOARD] Generated dashboard at: {path}")


def cmd_telegram(args):
    from brain import telegram_bot

    if not telegram_bot.is_configured():
        print("[TELEGRAM] Not configured!")
        print("  1. Message @BotFather on Telegram -> /newbot -> copy your token")
        print("  2. Send any message to your new bot")
        print("  3. Visit https://api.telegram.org/bot<TOKEN>/getUpdates to find your chat_id")
        print("  4. Create .env file in the project root with:")
        print("     TELEGRAM_BOT_TOKEN=your_token")
        print("     TELEGRAM_CHAT_ID=your_chat_id")
        return

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


def main():
    parser = argparse.ArgumentParser(description="ARGUS CLI — The Hundred-Eyed Builder Intelligence Engine")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # radar
    subparsers.add_parser("radar", help="View Ecosystem Momentum Radar")

    # sponsor
    p_sp = subparsers.add_parser("sponsor", help="View Sponsor Intelligence Cards")
    p_sp.add_argument("slug", nargs="?", help="Specific sponsor slug (e.g. world, dynamic, pyth-network)")

    # winners
    p_win = subparsers.add_parser("winners", help="View historical winner & losing patterns")
    p_win.add_argument("--event", "-e", help="Filter by event name")

    # opportunities
    p_opp = subparsers.add_parser("opportunities", help="List scored opportunities")
    p_opp.add_argument("--limit", "-n", type=int, default=15, help="Number of opportunities to show")

    # edge
    subparsers.add_parser("edge", help="Show active Level 3 Actionable Edge opportunities")

    # content
    p_cnt = subparsers.add_parser("content", help="Generate or view social content opportunities")
    p_cnt.add_argument("slug", nargs="?", help="Opportunity slug to generate content for")

    # trends
    subparsers.add_parser("trends", help="Show technical narrative trend detection")

    # scan
    subparsers.add_parser("scan", help="Run full intelligence ingestion & scoring cycle")

    # dashboard
    subparsers.add_parser("dashboard", help="Regenerate interactive Generative UI dashboard")

    # telegram
    p_tg = subparsers.add_parser("telegram", help="Telegram bot: test connection, push alerts, or send summary")
    p_tg.add_argument("action", choices=["test", "push", "summary"],
                       help="test = verify connection | push = send all Edge alerts | summary = send digest")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    commands = {
        "radar": cmd_radar,
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

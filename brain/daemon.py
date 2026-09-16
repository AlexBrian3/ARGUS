"""
Hourly Autonomous Daemon for ARGUS: The Hundred-Eyed Builder Intelligence Engine.
Executes periodic intelligence cycles:
1. Runs OpportunityScout (Tier 0-2 ingestion & normalization)
2. Re-evaluates Ecosystem Radar & Momentum scores
3. Updates Sponsor Intelligence Cards & alerts on recurring appearances
4. Re-scores HackScore and User Fit
5. Evaluates Alert Selectivity (dispatches only genuine Level 1-3 conviction signals)
6. Generates Content Opportunities for high-EV discoveries
7. Updates the Generative UI Dashboard
8. Dispatches high-conviction alerts to Telegram (if configured)
"""
import sys
import time
import datetime

# Ensure UTF-8 output on Windows console
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from brain.db.database import Database
from brain.engines.scout import OpportunityScout
from brain.engines.radar import EcosystemRadar
from brain.engines.alerts import AlertEngine
from brain.engines.content import SocialContentEngine
from brain.dashboard.generator import generate_dashboard_html
from brain import telegram_bot


class ArgusDaemon:
    def __init__(self):
        self.db = Database()
        self.scout = OpportunityScout(self.db)
        self.radar = EcosystemRadar(self.db)
        self.alert_engine = AlertEngine(self.db)
        self.content_engine = SocialContentEngine(self.db)
        self._telegram_ok = telegram_bot.is_configured()
        if self._telegram_ok:
            print("[DAEMON] ARGUS Telegram bot configured. Alerts will be dispatched to your chat.")
        else:
            print("[DAEMON] Telegram not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env to enable.")

    def _dispatch_telegram_alerts(self, new_alerts: list, all_opportunities: list):
        """
        Selective Telegram dispatch — only sends when material signals exist.
        Follows the core philosophy: do NOT notify every hour.
        """
        if not self._telegram_ok:
            return

        sent_something = False

        # 1. Dispatch individual Level 3 Actionable Edge alerts
        for alert in new_alerts:
            level = alert.get("alert_level", 2)
            opp_id = alert.get("opportunity_id")

            if level == 3 and opp_id:
                # Fetch the full opportunity record for rich formatting
                opp = self.db.get_opportunity(opp_id)
                if opp:
                    msg = telegram_bot.format_actionable_edge(opp)
                    if telegram_bot.send_message(msg):
                        print(f"[TELEGRAM] Sent Level 3 Edge: {opp.get('name')}")
                        sent_something = True

            elif level == 1:
                msg = telegram_bot.format_first_signal(alert)
                if telegram_bot.send_message(msg):
                    print(f"[TELEGRAM] Sent Level 1 Signal: {alert.get('title', '')[:60]}")
                    sent_something = True

        # 2. If new alerts were fired but none dispatched individually, send a summary
        if new_alerts and not sent_something:
            edge_count = sum(1 for o in all_opportunities if o.get("alert_level") == 3)
            summary = telegram_bot.format_hourly_summary(
                total_scanned=len(all_opportunities),
                edge_count=edge_count,
                new_alerts=new_alerts,
                top_opportunities=all_opportunities[:5]
            )
            telegram_bot.send_message(summary)
            print("[TELEGRAM] Sent hourly summary digest.")

    def execute_hourly_cycle(self) -> dict:
        cycle_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[DAEMON] Starting Hourly Intelligence Cycle at {cycle_time}")

        # 1. Scout scan (re-ingests, re-scores, re-evaluates all engines)
        scout_result = self.scout.run_full_scan()
        print(f"[DAEMON] Opportunities scanned: {scout_result['total_opportunities_scanned']}")

        # 2. Check for newly fired alerts (these are deduplicated — only truly new ones appear)
        recent_alerts = self.alert_engine.get_recent_alerts(limit=10)
        # Filter to alerts generated within the last 65 minutes (this cycle window)
        new_alerts_this_cycle = []
        cutoff = datetime.datetime.now() - datetime.timedelta(minutes=65)
        for a in recent_alerts:
            try:
                sent_at = datetime.datetime.fromisoformat(a.get("sent_at", "2000-01-01"))
                if sent_at >= cutoff:
                    new_alerts_this_cycle.append(a)
            except (ValueError, TypeError):
                new_alerts_this_cycle.append(a)

        new_level_3 = [a for a in new_alerts_this_cycle if a.get("alert_level") == 3]

        if new_level_3:
            print(f"[ALERT SELECTIVITY] 🟢 {len(new_level_3)} Actionable Edge alerts this cycle!")
            for a in new_level_3:
                print(f"  * {a['title']}: {a['summary']}")
        else:
            print("[ALERT SELECTIVITY] No material shifts requiring high-priority notification.")

        # 3. Dispatch to Telegram (selective — respects alert philosophy)
        all_opps = self.db.get_all_opportunities(limit=25)
        if new_alerts_this_cycle:
            self._dispatch_telegram_alerts(new_alerts_this_cycle, all_opps)
        else:
            print("[TELEGRAM] Silent cycle — no dispatch needed.")

        # 4. Refresh Dashboard
        dashboard_path = generate_dashboard_html()
        print(f"[DAEMON] Generative UI Dashboard refreshed at {dashboard_path}")
        print(f"[DAEMON] Hourly cycle completed successfully.\n")

        return {
            "cycle_time": cycle_time,
            "opportunities_scanned": scout_result['total_opportunities_scanned'],
            "new_alerts_this_cycle": len(new_alerts_this_cycle),
            "actionable_edge_count": len(new_level_3),
            "telegram_dispatched": self._telegram_ok and len(new_alerts_this_cycle) > 0,
            "dashboard_path": str(dashboard_path)
        }

    def run_continuous(self, interval_seconds: int = 3600):
        print(f"[DAEMON] Starting ARGUS continuous runner (Interval: {interval_seconds}s / 1 hour)")
        while True:
            try:
                self.execute_hourly_cycle()
            except Exception as e:
                print(f"[DAEMON ERROR] Exception during cycle: {e}")

            print(f"[DAEMON] Sleeping for {interval_seconds} seconds...")
            time.sleep(interval_seconds)


if __name__ == "__main__":
    daemon = ArgusDaemon()
    # Single execution mode for cron/scheduler or continuous
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        daemon.run_continuous()
    else:
        daemon.execute_hourly_cycle()

"""
-------------------------------------------------------------------------------
ARGUS AUTONOMOUS DAEMON
-------------------------------------------------------------------------------
This daemon runs quietly in the background on an hourly schedule.

During each hourly cycle, it performs 5 simple steps:
1. Scans all opportunities across Tier 0, Tier 1, and Tier 2 sources
2. Re-evaluates Ecosystem Momentum and HackScores
3. Evaluates Alert Selectivity (dispatches ONLY genuine high-conviction signals)
4. Sends Level 3 Actionable Edge cards directly to your Telegram
5. Updates the interactive Generative UI Dashboard (dashboard.html)

No spam policy: If nothing changed, it runs silently!
"""

import sys
import time
import datetime

# Ensure clean UTF-8 text output on Windows Command Prompt / PowerShell
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
    """Runs the periodic intelligence cycle and manages notifications."""

    def __init__(self):
        # Initialize database and all required engines
        self.db = Database()
        self.scout = OpportunityScout(self.db)
        self.radar = EcosystemRadar(self.db)
        self.alert_engine = AlertEngine(self.db)
        self.content_engine = SocialContentEngine(self.db)

        # Check if Telegram credentials are set up
        self.telegram_ready = telegram_bot.is_configured()
        if self.telegram_ready:
            print("[DAEMON] ARGUS Telegram bot connected! Alerts will be sent to your phone.")
        else:
            print("[DAEMON] Telegram not configured. Add credentials to .env to enable phone alerts.")

    def _dispatch_telegram_alerts(self, new_alerts: list, all_opportunities: list):
        """
        Sends alerts to Telegram while strictly respecting your time (no spam).
        """
        if not self.telegram_ready:
            return

        sent_any_individual = False

        # ------------------------------------------------------------------- #
        # Step A: Dispatch Level 3 Actionable Edge opportunities              #
        # ------------------------------------------------------------------- #
        for alert in new_alerts:
            level = alert.get("alert_level", 2)
            opp_id = alert.get("opportunity_id")

            # High-priority Level 3 alert: Send the full rich card!
            if level == 3 and opp_id:
                opportunity = self.db.get_opportunity(opp_id)
                if opportunity:
                    card_message = telegram_bot.format_actionable_edge(opportunity)
                    if telegram_bot.send_message(card_message):
                        print(f"[TELEGRAM] Sent Actionable Edge: {opportunity.get('name')}")
                        sent_any_individual = True

            # Early Level 1 First Signal: Send the preparation advisory!
            elif level == 1:
                signal_message = telegram_bot.format_first_signal(alert)
                if telegram_bot.send_message(signal_message):
                    print(f"[TELEGRAM] Sent First Signal: {alert.get('title', '')[:60]}")
                    sent_any_individual = True

        # ------------------------------------------------------------------- #
        # Step B: If there are general updates, send a summary digest         #
        # ------------------------------------------------------------------- #
        if new_alerts and not sent_any_individual:
            edge_count = sum(1 for opp in all_opportunities if opp.get("alert_level") == 3)
            summary = telegram_bot.format_hourly_summary(
                total_scanned=len(all_opportunities),
                edge_count=edge_count,
                new_alerts=new_alerts,
                top_opportunities=all_opportunities[:5]
            )
            telegram_bot.send_message(summary)
            print("[TELEGRAM] Sent hourly summary digest.")

    def execute_hourly_cycle(self) -> dict:
        """
        Runs one full intelligence cycle from start to finish.
        """
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[DAEMON] Starting ARGUS Hourly Intelligence Cycle at {current_time}")

        # ------------------------------------------------------------------- #
        # Step 1: Run Opportunity Scout across all sources                    #
        # ------------------------------------------------------------------- #
        scout_result = self.scout.run_full_scan()
        print(f"[DAEMON] Opportunities evaluated: {scout_result['total_opportunities_scanned']}")

        # ------------------------------------------------------------------- #
        # Step 2: Check for newly triggered alerts in this cycle              #
        # ------------------------------------------------------------------- #
        recent_alerts = self.alert_engine.get_recent_alerts(limit=10)
        cutoff_time = datetime.datetime.now() - datetime.timedelta(minutes=65)

        alerts_this_cycle = []
        for alert in recent_alerts:
            try:
                alert_time = datetime.datetime.fromisoformat(alert.get("sent_at", "2000-01-01"))
                if alert_time >= cutoff_time:
                    alerts_this_cycle.append(alert)
            except (ValueError, TypeError):
                alerts_this_cycle.append(alert)

        edge_alerts = [a for a in alerts_this_cycle if a.get("alert_level") == 3]

        if edge_alerts:
            print(f"[ALERT SELECTIVITY] 🟢 {len(edge_alerts)} Actionable Edge alerts found this cycle!")
            for alert in edge_alerts:
                print(f"  * {alert['title']}")
        else:
            print("[ALERT SELECTIVITY] No material changes requiring notification this cycle.")

        # ------------------------------------------------------------------- #
        # Step 3: Dispatch to Telegram (High-Priority Cards + Hourly Pulse)   #
        # ------------------------------------------------------------------- #
        all_opportunities = self.db.get_all_opportunities(limit=25)
        top_ecosystems = self.radar.get_leaderboard()
        edge_count = sum(1 for opp in all_opportunities if opp.get("alert_level") == 3)

        if self.telegram_ready:
            # 3A: If brand-new individual alerts were detected, send their cards
            if alerts_this_cycle:
                self._dispatch_telegram_alerts(alerts_this_cycle, all_opportunities)

            # 3B: Always send the Hourly Pulse so you stay updated on your phone!
            pulse_message = telegram_bot.format_hourly_summary(
                total_scanned=scout_result["total_opportunities_scanned"],
                edge_count=edge_count,
                new_alerts=alerts_this_cycle,
                top_opportunities=all_opportunities[:4],
                top_ecosystems=top_ecosystems[:3]
            )
            telegram_bot.send_message(pulse_message)
            print("[TELEGRAM] Hourly Pulse delivered successfully to your phone.")
        else:
            print("[TELEGRAM] Telegram not configured. Skipping phone dispatch.")

        # ------------------------------------------------------------------- #
        # Step 4: Refresh Generative UI Dashboard                             #
        # ------------------------------------------------------------------- #
        dashboard_path = generate_dashboard_html()
        print(f"[DAEMON] Generative UI Dashboard refreshed at {dashboard_path}")
        print(f"[DAEMON] Hourly cycle completed successfully.\n")

        return {
            "cycle_time": current_time,
            "opportunities_scanned": scout_result["total_opportunities_scanned"],
            "new_alerts_this_cycle": len(alerts_this_cycle),
            "actionable_edge_count": len(edge_alerts),
            "telegram_dispatched": self.telegram_ready,
            "dashboard_path": str(dashboard_path)
        }

    def run_continuous(self, interval_seconds: int = 3600):
        """
        Keeps running in an infinite loop, executing every hour (3600 seconds).
        """
        print(f"[DAEMON] Starting ARGUS continuous loop (Interval: {interval_seconds}s / 1 hour)")
        while True:
            try:
                self.execute_hourly_cycle()
            except Exception as error:
                print(f"[DAEMON ERROR] Unexpected error during cycle: {error}")

            print(f"[DAEMON] Sleeping for {interval_seconds} seconds until next scan...")
            time.sleep(interval_seconds)


# When run directly from terminal: python -m brain.daemon
if __name__ == "__main__":
    daemon = ArgusDaemon()
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        daemon.run_continuous()
    else:
        daemon.execute_hourly_cycle()

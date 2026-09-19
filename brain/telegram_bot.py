"""
-------------------------------------------------------------------------------
ARGUS TELEGRAM BOT INTEGRATION
-------------------------------------------------------------------------------
Sends high-conviction alerts directly to your phone via Telegram.

Zero external dependencies! Uses Python's built-in urllib module.

Setup in 3 Steps:
1. Message @BotFather on Telegram -> /newbot -> copy the token
2. Send any message to your new bot
3. Visit https://api.telegram.org/bot<TOKEN>/getUpdates to find your chat_id
4. Add them to your .env file:
   TELEGRAM_BOT_TOKEN=your_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
"""

import os
import json
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from typing import List, Dict, Any

# --------------------------------------------------------------------------- #
#                        1. LOAD ENVIRONMENT VARIABLES                        #
# --------------------------------------------------------------------------- #

# Path to our .env file in the project root
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


def _load_env():
    """Reads .env file and loads keys into os.environ without any third-party packages."""
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as file:
            for line in file:
                cleaned_line = line.strip()
                # Skip blank lines and comments
                if cleaned_line and not cleaned_line.startswith("#") and "=" in cleaned_line:
                    key, _, value = cleaned_line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and value:
                        os.environ.setdefault(key, value)


# Load .env immediately on import
_load_env()

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


# --------------------------------------------------------------------------- #
#                        2. CONNECTION HELPERS                                #
# --------------------------------------------------------------------------- #

def is_configured() -> bool:
    """Returns True if both the bot token and chat ID are present."""
    return bool(BOT_TOKEN) and bool(CHAT_ID)


def send_message(text: str, parse_mode: str = "HTML", disable_preview: bool = True, max_retries: int = 3) -> bool:
    """
    Sends a message to your Telegram chat.
    Splits long messages automatically to fit Telegram's 4,096 character limit.
    Includes automated retries with backoff in case of network blips.
    """
    import time

    if not is_configured():
        print("[TELEGRAM] Bot is not configured. Add credentials to your .env file.")
        return False

    message_chunks = _chunk_message(text, max_len=4000)
    all_succeeded = True

    for chunk in message_chunks:
        payload = {
            "chat_id": CHAT_ID,
            "text": chunk,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_preview
        }
        json_data = json.dumps(payload).encode("utf-8")

        chunk_sent = False
        for attempt in range(1, max_retries + 1):
            try:
                request = urllib.request.Request(
                    f"{TELEGRAM_API_URL}/sendMessage",
                    data=json_data,
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )

                # Generous 30-second timeout to handle slow Wi-Fi
                with urllib.request.urlopen(request, timeout=30) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    if result.get("ok"):
                        chunk_sent = True
                        break
                    else:
                        print(f"[TELEGRAM] API error on attempt {attempt}: {result}")

            except urllib.error.URLError as error:
                print(f"[TELEGRAM] Network warning (attempt {attempt}/{max_retries}): {error}")
            except Exception as error:
                print(f"[TELEGRAM] Unexpected error (attempt {attempt}/{max_retries}): {error}")

            # Brief pause before retrying
            if attempt < max_retries:
                time.sleep(2 * attempt)

        if not chunk_sent:
            all_succeeded = False

    return all_succeeded


def _chunk_message(text: str, max_len: int = 4000) -> List[str]:
    """Splits long text into chunks at line breaks so words aren't cut in half."""
    if len(text) <= max_len:
        return [text]

    chunks = []
    current_chunk = ""

    for line in text.split("\n"):
        if len(current_chunk) + len(line) + 1 > max_len:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = line
        else:
            current_chunk = f"{current_chunk}\n{line}" if current_chunk else line

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


# --------------------------------------------------------------------------- #
#                        3. MESSAGE FORMATTERS                                #
# --------------------------------------------------------------------------- #

def format_actionable_edge(opportunity: Dict[str, Any]) -> str:
    """Formats a Level 3 Actionable Edge opportunity into a beautiful Telegram card."""
    name = opportunity.get("name", "Unknown")
    organizer = opportunity.get("organizer", "")
    ecosystem = opportunity.get("ecosystem", "")
    prize = opportunity.get("total_prize_usd", 0)
    hack_score = opportunity.get("hack_score", 0)
    skill_match = opportunity.get("skill_match_score", 0)
    ratio = opportunity.get("prize_to_competitor_ratio", 0)
    prob_place = opportunity.get("prob_placing", 0)
    prob_any = opportunity.get("prob_any_reward", 0)
    deadline = opportunity.get("submission_deadline", "TBD")
    build_direction = opportunity.get("recommended_build_direction", "")
    techs_to_learn = opportunity.get("technologies_to_learn", [])

    if isinstance(build_direction, dict):
        everyone = build_direction.get("what_everyone_else_will_build", "Generic boilerplate CRUD or basic AI wrapper.")
        advantage = build_direction.get("your_unfair_advantage_build", "Deep infrastructure / autonomous agent integration.")
        build_text = (
            f"<b>👥 What Everyone Else Will Build:</b>\n"
            f"<i>{_esc(everyone[:250])}</i>\n\n"
            f"<b>⚡ Your Unfair Advantage Build:</b>\n"
            f"<i>{_esc(advantage[:350])}</i>"
        )
    else:
        build_text = (
            f"<b>⚡ Unfair Advantage Build:</b>\n"
            f"<i>{_esc(str(build_direction)[:500])}</i>"
        )

    return (
        f"<b>🟢 LEVEL 3 — ACTIONABLE EDGE</b>\n\n"
        f"<b>{_esc(name)}</b>\n"
        f"📍 {_esc(organizer)} · {_esc(ecosystem)}\n\n"
        f"💰 Prize: <b>${prize:,.0f}</b>\n"
        f"🎯 HackScore: <b>{hack_score:.1f}/100</b>\n"
        f"🔧 Skill Match: <b>{skill_match:.1f}/100</b>\n"
        f"📊 $/Serious Builder: <b>${ratio:,.0f}</b>\n"
        f"📈 Win Prob: <b>{prob_place*100:.0f}%</b> · Any Reward: <b>{prob_any*100:.0f}%</b>\n"
        f"⏰ Deadline: <b>{_esc(str(deadline))}</b>\n\n"
        f"{build_text}\n\n"
        f"<b>🛠 Learn NOW:</b> {_esc(', '.join(techs_to_learn))}"
    )


def format_fresh_job_alert(job: Dict[str, Any]) -> str:
    """Formats a Level 1 First Signal alert for ultra-fresh (<24h) high-fit job listings."""
    title = job.get("title", "Unknown Role")
    company = job.get("company", "Web3 Team")
    ecosystem = job.get("ecosystem", "Web3")
    match_score = job.get("skill_match_score", 0.0)
    compensation = job.get("compensation", "Competitive")
    location = job.get("location", "Remote")
    source = job.get("source", "radar")
    apply_url = job.get("apply_url", "#")
    desc = job.get("description", "")

    return (
        f"<b>🔥 LEVEL 1 — FRESH JOB FIRST SIGNAL (&lt;24H)</b>\n\n"
        f"<b>{_esc(title)}</b>\n"
        f"🏢 {_esc(company)} · {_esc(ecosystem)}\n\n"
        f"🎯 Skill Match: <b>{match_score:.0f}%</b>\n"
        f"💰 Compensation: <b>{_esc(compensation)}</b>\n"
        f"📍 Location: {_esc(location)}\n"
        f"🌐 Source: {_esc(source)}\n\n"
        f"<b>Role Overview:</b>\n<i>{_esc(desc[:320])}</i>\n\n"
        f"🔗 <a href='{apply_url}'>Apply Immediately ↗</a>"
    )


def format_first_signal(signal: Dict[str, Any]) -> str:
    """Formats a Level 1 First Signal alert for Telegram."""
    title = signal.get("title", "")
    summary = signal.get("summary", "")
    actions = signal.get("action_items", [])
    learn_now = signal.get("what_to_learn_immediately", "")

    actions_text = "\n".join(f"  → {_esc(action)}" for action in actions) if actions else "  → Monitor closely"

    return (
        f"<b>🔴 LEVEL 1 — FIRST SIGNAL</b>\n\n"
        f"{_esc(title)}\n\n"
        f"{_esc(summary)}\n\n"
        f"<b>Action Items:</b>\n{actions_text}\n\n"
        f"<b>Learn NOW:</b> {_esc(learn_now)}"
    )


def format_hourly_summary(
    total_scanned: int,
    edge_count: int,
    new_alerts: List[Dict[str, Any]],
    top_opportunities: List[Dict[str, Any]],
    top_ecosystems: List[Dict[str, Any]] = None,
    promoted_ecosystems: List[Dict[str, Any]] = None,
    fresh_jobs: List[Dict[str, Any]] = None,
    top_benefits: List[Dict[str, Any]] = None
) -> str:
    """Formats a rich, actionable hourly pulse message for Telegram."""
    import datetime
    current_time = datetime.datetime.now().strftime("%H:%M")

    header = (
        f"<b>👁️ ARGUS — HOURLY PULSE ({current_time})</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔍 Scanned: <b>{total_scanned} opportunities</b>\n"
        f"🟢 Active Edge: <b>{edge_count} high-EV targets</b>\n"
    )

    body = ""

    # Section 1: Any brand-new alerts triggered in this cycle
    if new_alerts:
        body += "\n<b>🚨 New Alerts This Cycle:</b>\n"
        for alert in new_alerts[:3]:
            level = alert.get("alert_level", 2)
            icon = "🟢" if level == 3 else ("🔴" if level == 1 else "🟠")
            body += f"  {icon} <b>{_esc(alert.get('title', '')[:65])}</b>\n"

    # Section 2: Top Active Edge Opportunities with HackScore
    if top_opportunities:
        body += "\n<b>🎯 Top Priority Opportunities:</b>\n"
        for opp in top_opportunities[:3]:
            name = opp.get("name", "")[:32]
            prize = opp.get("total_prize_usd", 0)
            hack_score = opp.get("hack_score", 0)
            skill = opp.get("skill_match_score", 0)
            deadline = opp.get("submission_deadline", "TBD")
            body += (
                f"  • <b>{_esc(name)}</b>\n"
                f"    💰 ${prize:,.0f} | 🎯 HS: {hack_score:.0f} | 🔧 Fit: {skill:.0f}%\n"
                f"    ⏰ Deadline: {_esc(str(deadline))}\n"
            )

    # Section 3: Promoted Ecosystems (Engine 11)
    if promoted_ecosystems:
        body += "\n<b>🚀 Promoted Ecosystems (Engine 11):</b>\n"
        for pe in promoted_ecosystems[:2]:
            body += f"  • <b>{_esc(pe.get('name', ''))}</b>: Promoted to <i>{_esc(pe.get('maturity_stage', ''))}</i> (Momentum {pe.get('momentum_score', 0):.1f})\n"

    # Section 4: Fresh Web3/AI Jobs (Engine 13)
    if fresh_jobs:
        body += "\n<b>🔥 Fresh Roles (&lt;24h) (Engine 13):</b>\n"
        for fj in fresh_jobs[:2]:
            body += f"  • <b>{_esc(fj.get('title', ''))}</b> @ {_esc(fj.get('company', ''))} ({fj.get('skill_match_score', 0):.0f}% fit)\n"

    # Section 5: Top Standing Benefits/Perks (Engine 12)
    if top_benefits:
        body += "\n<b>🎁 Top Benefit / Grant (Engine 12):</b>\n"
        for tb in top_benefits[:1]:
            body += f"  • <b>{_esc(tb.get('title', ''))}</b> (${tb.get('amount_usd', 0):,} USD · {_esc(tb.get('ecosystem', ''))})\n"

    # Section 6: Ecosystem Radar highlights
    if top_ecosystems:
        body += "\n<b>📡 Top Accelerating Ecosystems:</b>\n"
        accel = [e for e in top_ecosystems if "↑" in e.get("momentum_trajectory", "")]
        for eco in (accel[:3] if accel else top_ecosystems[:3]):
            body += f"  • <b>{_esc(eco.get('name', ''))}</b>: {eco.get('momentum_score', 0):.1f} {eco.get('momentum_trajectory', '↑')}\n"

    footer = "\n<i>All systems operational · Dashboard updated</i>"

    return header + body + footer


def _esc(text: str) -> str:
    """Escapes HTML special characters so Telegram renders text without errors."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

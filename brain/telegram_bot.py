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


def send_message(text: str, parse_mode: str = "HTML", disable_preview: bool = True) -> bool:
    """
    Sends a message to your Telegram chat.
    Splits long messages automatically to fit Telegram's 4,096 character limit.
    """
    if not is_configured():
        print("[TELEGRAM] Bot is not configured. Add credentials to your .env file.")
        return False

    message_chunks = _chunk_message(text, max_len=4000)
    all_succeeded = True

    for chunk in message_chunks:
        try:
            payload = {
                "chat_id": CHAT_ID,
                "text": chunk,
                "parse_mode": parse_mode,
                "disable_web_page_preview": disable_preview
            }
            json_data = json.dumps(payload).encode("utf-8")

            request = urllib.request.Request(
                f"{TELEGRAM_API_URL}/sendMessage",
                data=json_data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            with urllib.request.urlopen(request, timeout=15) as response:
                result = json.loads(response.read().decode("utf-8"))
                if not result.get("ok"):
                    print(f"[TELEGRAM] API error: {result}")
                    all_succeeded = False

        except urllib.error.URLError as error:
            print(f"[TELEGRAM] Network error: {error}")
            all_succeeded = False
        except Exception as error:
            print(f"[TELEGRAM] Unexpected error: {error}")
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
        f"<b>⚡ Unfair Advantage Build:</b>\n"
        f"<i>{_esc(build_direction[:500])}</i>\n\n"
        f"<b>🛠 Learn NOW:</b> {_esc(', '.join(techs_to_learn))}"
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
    top_opportunities: List[Dict[str, Any]]
) -> str:
    """Formats a concise digest for the hourly scanner."""
    header = (
        f"<b>👁️ ARGUS — HOURLY INTELLIGENCE</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Scanned: {total_scanned} opportunities\n"
        f"Active Edge Alerts: {edge_count}\n"
    )

    if not new_alerts and not top_opportunities:
        return header + "\nNo material changes this cycle. Standing by."

    body = ""
    if new_alerts:
        body += "\n<b>🆕 New Alerts This Cycle:</b>\n"
        for alert in new_alerts[:5]:
            level = alert.get("alert_level", 2)
            icon = "🟢" if level == 3 else ("🔴" if level == 1 else "🟠")
            body += f"  {icon} {_esc(alert.get('title', '')[:80])}\n"

    if top_opportunities:
        body += "\n<b>🏆 Top Opportunities:</b>\n"
        for opp in top_opportunities[:5]:
            body += (
                f"  • <b>{_esc(opp.get('name', '')[:40])}</b> "
                f"— ${opp.get('total_prize_usd', 0):,.0f} "
                f"(HS: {opp.get('hack_score', 0):.0f})\n"
            )

    return header + body


def _esc(text: str) -> str:
    """Escapes HTML special characters so Telegram renders text without errors."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

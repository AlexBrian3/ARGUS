"""
Telegram Bot integration for ARGUS: The Hundred-Eyed Builder Intelligence Engine.
Sends high-conviction alerts and intelligence summaries to your Telegram chat.
Uses only Python stdlib (urllib) — zero external dependencies.

Setup:
1. Message @BotFather on Telegram → /newbot → copy the token
2. Message your new bot, then visit https://api.telegram.org/bot<TOKEN>/getUpdates to find your chat_id
3. Set environment variables or create .env file:
   TELEGRAM_BOT_TOKEN=your_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
"""
import os
import json
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from typing import Optional, List, Dict, Any

# Try loading from .env file in project root
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


def _load_env():
    """Load .env file if it exists (simple key=value parser, no dependencies)."""
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and value:
                        os.environ.setdefault(key, value)


_load_env()

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def is_configured() -> bool:
    """Check if Telegram credentials are set."""
    return bool(BOT_TOKEN) and bool(CHAT_ID)


def send_message(text: str, parse_mode: str = "HTML", disable_preview: bool = True) -> bool:
    """
    Send a message to the configured Telegram chat.
    Returns True on success, False on failure.
    """
    if not is_configured():
        print("[TELEGRAM] Not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env")
        return False

    # Telegram messages have a 4096 char limit — chunk if needed
    chunks = _chunk_message(text, max_len=4000)

    success = True
    for chunk in chunks:
        try:
            payload = {
                "chat_id": CHAT_ID,
                "text": chunk,
                "parse_mode": parse_mode,
                "disable_web_page_preview": disable_preview
            }
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{TELEGRAM_API}/sendMessage",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                if not result.get("ok"):
                    print(f"[TELEGRAM] API error: {result}")
                    success = False
        except urllib.error.URLError as e:
            print(f"[TELEGRAM] Network error: {e}")
            success = False
        except Exception as e:
            print(f"[TELEGRAM] Unexpected error: {e}")
            success = False

    return success


def _chunk_message(text: str, max_len: int = 4000) -> List[str]:
    """Split long messages into Telegram-safe chunks at line boundaries."""
    if len(text) <= max_len:
        return [text]

    chunks = []
    current = ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 > max_len:
            if current:
                chunks.append(current)
            current = line
        else:
            current = f"{current}\n{line}" if current else line
    if current:
        chunks.append(current)
    return chunks


# ─── Formatted Message Builders ────────────────────────────────────────────

def format_actionable_edge(opp: Dict[str, Any]) -> str:
    """Format a Level 3 Actionable Edge opportunity for Telegram."""
    name = opp.get("name", "Unknown")
    organizer = opp.get("organizer", "")
    ecosystem = opp.get("ecosystem", "")
    prize = opp.get("total_prize_usd", 0)
    hack_score = opp.get("hack_score", 0)
    skill_match = opp.get("skill_match_score", 0)
    ratio = opp.get("prize_to_competitor_ratio", 0)
    prob_place = opp.get("prob_placing", 0)
    prob_any = opp.get("prob_any_reward", 0)
    deadline = opp.get("submission_deadline", "TBD")
    build = opp.get("recommended_build_direction", "")
    techs = opp.get("technologies_to_learn", [])

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
        f"<i>{_esc(build[:500])}</i>\n\n"
        f"<b>🛠 Learn NOW:</b> {_esc(', '.join(techs))}"
    )


def format_first_signal(signal: Dict[str, Any]) -> str:
    """Format a Level 1 First Signal for Telegram."""
    title = signal.get("title", "")
    summary = signal.get("summary", "")
    actions = signal.get("action_items", [])
    learn = signal.get("what_to_learn_immediately", "")

    actions_str = "\n".join(f"  → {_esc(a)}" for a in actions) if actions else "  → Monitor closely"

    return (
        f"<b>🔴 LEVEL 1 — FIRST SIGNAL</b>\n\n"
        f"{_esc(title)}\n\n"
        f"{_esc(summary)}\n\n"
        f"<b>Action Items:</b>\n{actions_str}\n\n"
        f"<b>Learn NOW:</b> {_esc(learn)}"
    )


def format_ecosystem_shift(eco: Dict[str, Any], direction: str = "↑") -> str:
    """Format an ecosystem momentum trajectory change for Telegram."""
    name = eco.get("name", "")
    score = eco.get("momentum_score", 0)
    notes = eco.get("notes", "")

    return (
        f"<b>📡 ECOSYSTEM MOMENTUM SHIFT</b>\n\n"
        f"<b>{_esc(name)}</b> trajectory changed to <b>{direction}</b>\n"
        f"Momentum Score: <b>{score:.1f}/100</b>\n\n"
        f"<i>{_esc(notes[:400])}</i>"
    )


def format_hourly_summary(
    total_scanned: int,
    edge_count: int,
    new_alerts: List[Dict[str, Any]],
    top_opportunities: List[Dict[str, Any]]
) -> str:
    """Format a concise hourly digest (only sent when material changes exist)."""
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
        for a in new_alerts[:5]:
            lvl = a.get("alert_level", 2)
            icon = "🟢" if lvl == 3 else ("🔴" if lvl == 1 else "🟠")
            body += f"  {icon} {_esc(a.get('title', '')[:80])}\n"

    if top_opportunities:
        body += "\n<b>🏆 Top Opportunities:</b>\n"
        for o in top_opportunities[:5]:
            body += (
                f"  • <b>{_esc(o.get('name', '')[:40])}</b> "
                f"— ${o.get('total_prize_usd', 0):,.0f} "
                f"(HS: {o.get('hack_score', 0):.0f})\n"
            )

    return header + body


def format_sponsor_alert(sponsor_name: str, event_name: str, prep: str) -> str:
    """Format a recurring sponsor prediction alert."""
    return (
        f"<b>💼 SPONSOR PATTERN DETECTED</b>\n\n"
        f"<b>{_esc(sponsor_name)}</b> has appeared in multiple recent events.\n"
        f"Likely to sponsor: <b>{_esc(event_name)}</b>\n\n"
        f"<b>Recommended Preparation:</b>\n"
        f"<i>{_esc(prep[:500])}</i>"
    )


def _esc(text: str) -> str:
    """Escape HTML special characters for Telegram."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

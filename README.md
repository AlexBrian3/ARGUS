# ARGUS: The Hundred Eyed Builder Intelligence Engine

ARGUS is a personal intelligence system for builders who compete in hackathons, bounties, and grant programs. Instead of manually tracking dozens of ecosystems and sponsors, ARGUS watches them for you, scores every opportunity by how likely you are to actually win something, and tells you what to build to stand out.

It runs entirely on your machine, keeps its own history in a local database, and can notify you when something worth acting on shows up, whether that's in your terminal, on Telegram, or on a dashboard you open in a browser.

## What ARGUS Does

ARGUS is built from 10 engines, each handling one part of the problem.

**Opportunity Scout** pulls in opportunities from GitHub, foundation blogs, and hackathon platforms like ETHGlobal, Colosseum, DoraHacks, and Devpost.

**Ecosystem Radar** tracks which blockchains and dev ecosystems (Solana, Base, Monad, Ethereum, Sui, and more) are heating up.

**Sponsor Intelligence** builds a profile on each sponsor: what they tend to reward, and what they're likely to run next.

**Historical Winner Analysis** studies past winning and losing projects to find the patterns judges actually reward.

**HackScore** scores each opportunity out of 100 based on prize size, competition, and your odds of placing.

**Skill Match** scores out of 100 how well an opportunity fits your actual skills and reusable projects.

**Early Signal Alerts** flags opportunities early, using three tiers: First Signal, Confirmed, and Actionable Edge.

**Social Content Intelligence** drafts ready to post threads, scripts, and posts about opportunities worth talking about.

**Trend Detection** tracks emerging technical narratives, like x402 payments or verifiable inference, before they're mainstream.

**Persistent Memory** saves everything to a local SQLite database, so ARGUS gets smarter with every scan.

## Getting Started

Requirements: Python 3.10 or newer. No external dependencies. ARGUS is built entirely on the Python standard library.

Clone the repo:

```bash
git clone https://github.com/AlexBrian3/ARGUS.git
cd ARGUS
```

Load some starter data. The first time you run ARGUS, seed the database with example ecosystems, sponsors, and opportunities so the commands below have something to show you:

```bash
python -m brain.db.seed
```

Optionally, install ARGUS as a command so you can type `argus` instead of `python -m brain.cli`:

```bash
pip install -e .
```

You're ready to go. Jump to the Quickstart below.

## Quickstart

Run a full scan. This sweeps every monitored source, re-scores all opportunities, checks for new alerts, and refreshes the dashboard.

```bash
python -m brain.cli scan
```

See your best opportunities right now. This shows only the high conviction, Actionable Edge opportunities, each with a build direction tailored to your skills.

```bash
python -m brain.cli edge
```

Check ecosystem momentum. This ranks tracked ecosystems and flags early "stealth" signals before major hackathons are announced.

```bash
python -m brain.cli radar
```

Look up a sponsor. This shows a sponsor's predictability score, what they usually reward, and how to prepare for their next event. Run the command with no name to see every sponsor tracked.

```bash
python -m brain.cli sponsor world
python -m brain.cli sponsor dynamic
python -m brain.cli sponsor pyth-network
```

Study winning and losing patterns. This surfaces what winning projects tend to have in common, common mistakes that lose, and ideas worth avoiding because everyone's already building them.

```bash
python -m brain.cli winners
```

Generate social content for an opportunity. This drafts an X/Twitter thread, a short form video script, and a LinkedIn post. Run the command with no name to see everything available.

```bash
python -m brain.cli content colosseum-crypto-worlds-fair-2026
```

Open the dashboard. Run this, then open dashboard/dashboard.html in your browser for a visual view of everything above.

```bash
python -m brain.cli dashboard
```

## Telegram Alerts

ARGUS can push alerts straight to your phone. This is optional.

Setup:

Message @BotFather on Telegram, send /newbot, and copy the token it gives you. Send any message to your new bot. Visit api.telegram.org/bot(your token)/getUpdates and find your chat id in the response. Copy .env.example to .env and fill in both values.

Usage:

```bash
python -m brain.cli telegram test
python -m brain.cli telegram push
python -m brain.cli telegram summary
```

test confirms the bot is connected, push sends all current Actionable Edge alerts, and summary sends a digest of everything scanned.

## Running ARGUS Automatically

ARGUS can check for new opportunities on its own, once an hour, without you running anything manually.

```bash
python -m brain.daemon
python -m brain.daemon --continuous
```

The first command runs a single check right now. The second keeps ARGUS running in the background, checking every hour.

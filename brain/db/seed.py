"""
Database seeder for ARGUS: The Hundred-Eyed Builder Intelligence Engine.
Loads baseline ecosystems, sponsors, winners, opportunities, and trends into SQLite.
"""
import sys

# Ensure UTF-8 output on Windows console
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from brain.db.database import Database
from brain.db.seed_data import (
    SEED_ECOSYSTEMS,
    SEED_SPONSORS,
    SEED_WINNERS,
    SEED_OPPORTUNITIES,
    SEED_TRENDS,
    SEED_BENEFITS,
    SEED_JOBS
)


def seed_database(db: Database = None):
    if db is None:
        db = Database()

    # --------- STEP 1: Seed Ecosystems (Engines 2 & 11) --------- #
    print("[SEED] Seeding Monitored Ecosystems (Engine 2 & 11)...")
    for eco in SEED_ECOSYSTEMS:
        db.upsert_ecosystem(eco)

    # --------- STEP 2: Seed Persistent Sponsors (Engine 3) --------- #
    print("[SEED] Seeding Persistent Sponsor Intelligence (Engine 3)...")
    for sp in SEED_SPONSORS:
        db.upsert_sponsor(sp)

    # --------- STEP 3: Seed Opportunities (Engines 1, 5, 6) --------- #
    print("[SEED] Seeding Active & Emerging Opportunities (Engine 1, 5, 6)...")
    for opp in SEED_OPPORTUNITIES:
        db.upsert_opportunity(opp)

    # --------- STEP 4: Seed Historical Winners (Engine 4) --------- #
    print("[SEED] Seeding Historical Winner Analysis (Engine 4)...")
    for w in SEED_WINNERS:
        db.insert_winner(w)

    # --------- STEP 5: Seed Technical Trends (Engine 9) --------- #
    print("[SEED] Seeding Emerging Technical Trends (Engine 9)...")
    for tr in SEED_TRENDS:
        db.upsert_trend(tr)

    # --------- STEP 6: Seed Standing Benefits & Perks (Engine 12) --------- #
    print("[SEED] Seeding Standing Benefits & Perks (Engine 12)...")
    for benefit in SEED_BENEFITS:
        db.upsert_benefit(benefit)

    # --------- STEP 7: Seed High-Relevance Web3/AI Jobs (Engine 13) --------- #
    print("[SEED] Seeding Fresh Job & Internship Opportunities (Engine 13)...")
    for job in SEED_JOBS:
        db.upsert_job_listing(job)

    print("[SUCCESS] Seeding complete!")



if __name__ == "__main__":
    seed_database()

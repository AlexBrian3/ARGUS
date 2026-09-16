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
    SEED_TRENDS
)


def seed_database(db: Database = None):
    if db is None:
        db = Database()

    print("[SEED] Seeding Monitored Ecosystems (Engine 2)...")
    for eco in SEED_ECOSYSTEMS:
        db.upsert_ecosystem(eco)

    print("[SEED] Seeding Persistent Sponsor Intelligence (Engine 3)...")
    for sp in SEED_SPONSORS:
        db.upsert_sponsor(sp)

    print("[SEED] Seeding Active & Emerging Opportunities (Engine 1, 5, 6)...")
    for opp in SEED_OPPORTUNITIES:
        db.upsert_opportunity(opp)

    print("[SEED] Seeding Historical Winner Analysis (Engine 4)...")
    for w in SEED_WINNERS:
        db.insert_winner(w)

    print("[SEED] Seeding Emerging Technical Trends (Engine 9)...")
    for tr in SEED_TRENDS:
        db.upsert_trend(tr)

    print("[SUCCESS] Seeding complete!")



if __name__ == "__main__":
    seed_database()

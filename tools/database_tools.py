import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "tripmate.db"


def save_itinerary(destination: str, days: int, itinerary: str) -> str:
    """Save a travel itinerary in the SQLite database."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itineraries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination TEXT NOT NULL,
            days INTEGER NOT NULL,
            itinerary TEXT NOT NULL
        )
    """)

    cursor.execute("""
        INSERT INTO itineraries (destination, days, itinerary)
        VALUES (?, ?, ?)
    """, (destination, days, itinerary))

    conn.commit()
    conn.close()

    return f"Your {days}-day trip to {destination} has been saved!"


def get_itineraries(destination: str) -> str:
    """Retrieve saved itineraries for a destination."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, destination, days, itinerary
        FROM itineraries
        WHERE destination LIKE ?
    """, (f"%{destination}%",))

    records = cursor.fetchall()
    conn.close()

    if not records:
        return f"No saved itinerary found for {destination}."

    results = []

    for record in records:
        itinerary_id, place, days, itinerary = record

        results.append(
            f"ID: {itinerary_id}\n"
            f"Destination: {place}\n"
            f"Duration: {days} days\n"
            f"Itinerary:\n{itinerary}"
        )

    return "\n\n".join(results)
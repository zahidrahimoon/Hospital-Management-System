# migration_etl.py
# ETL script: Migrates legacy appointment CSV into refactored schema
# Implements 4 transformations to fix data smells from Part E

import csv
import mysql.connector
from datetime import datetime

# ── CONFIG ──────────────────────────────────────────────────────────
DB_CONFIG = {
    'host':     'localhost',
    'user':     'root',
    'password': 'ibraheem3648',
    'database': 'hospital_legacy'
}

CSV_FILE = 'appointments_legacy.csv'

# T4: only these status codes are valid
VALID_STATUSES = {'P', 'C', 'X', 'H', 'R'}


# ── TRANSFORMATION FUNCTIONS ─────────────────────────────────────────

def parse_date(raw):
    """
    T1: Convert date string 'DD/MM/YYYY HH:MM' to Python datetime.
    The legacy system stored dates as plain text — a Data Type smell.
    We convert to proper DATETIME before inserting into new schema.
    """
    raw = raw.strip()
    try:
        # Parse the legacy format DD/MM/YYYY HH:MM
        return datetime.strptime(raw, '%d/%m/%Y %H:%M')
    except ValueError:
        # If format is wrong, return None and let caller handle it
        return None


def split_room(raw):
    """
    T2: Split 'Room 3 Block B' into (3, 'Block B').
    The legacy room column stored two facts in one column —
    an Overloaded Column / Non-Atomic Fields smell.
    We split it into room_number (INT) and building_block (VARCHAR).
    """
    raw = raw.strip()
    parts = raw.split()

    # Expected format: 'Room' NUMBER 'Block' LETTER
    # Example: 'Room 3 Block B' → parts = ['Room','3','Block','B']
    try:
        room_number    = int(parts[1])          # extract the number
        building_block = ' '.join(parts[2:])    # 'Block B'
        return room_number, building_block
    except (IndexError, ValueError):
        # If format unexpected, store None and original string
        return None, raw


# ── MAIN MIGRATION FUNCTION ──────────────────────────────────────────

def migrate():
    # Connect to MySQL database
    conn   = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Tracking counters
    inserted = 0
    skipped  = []

    print("=" * 50)
    print("  LEGACY APPOINTMENT DATA MIGRATION")
    print("=" * 50)
    print(f"Reading from: {CSV_FILE}")
    print()

    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)  # reads header row automatically

        for row in reader:

            appt_id    = row['appt_id'].strip()
            patient_id = row['patient_id'].strip()
            doc_id     = row['doc_id'].strip()
            status     = row['status'].strip()
            fee        = row['fee'].strip()
            discount   = row['discount'].strip()
            room_raw   = row['room'].strip()
            date_raw   = row['appt_date'].strip()

            # ── T4: Validate status code ─────────────────────────
            # If status is not in our reference table values,
            # skip this row and log it. Do NOT insert invalid data.
            if status not in VALID_STATUSES:
                skipped.append({
                    'appt_id': appt_id,
                    'reason':  f"Invalid status '{status}'"
                })
                print(f"  SKIPPED row {appt_id}: invalid status '{status}'")
                continue

            # ── T1: Parse appointment date ───────────────────────
            # Convert text date to proper DATETIME object
            appt_datetime = parse_date(date_raw)
            if appt_datetime is None:
                skipped.append({
                    'appt_id': appt_id,
                    'reason':  f"Invalid date format '{date_raw}'"
                })
                print(f"  SKIPPED row {appt_id}: bad date '{date_raw}'")
                continue

            # ── T2: Split room column ────────────────────────────
            # Extract room number and building block separately
            room_number, building_block = split_room(room_raw)

            # ── T3: Omit redundant columns ───────────────────────
            # patient_nm, patient_ph, doc_name are NOT inserted.
            # These were Duplicate Data smells — after normalisation
            # they are retrieved via JOIN on patient_id and doc_id.
            # net_fee is also omitted — it is a Derived Data smell
            # (always equals fee - discount, computed on read).

            # ── INSERT into refactored table ─────────────────────
            sql = """
                REPLACE INTO appointments_refactored
                (appt_id, patient_id, doc_id, appt_datetime,
                 status, fee, discount, room_number, building_block)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                int(appt_id),
                int(patient_id),
                int(doc_id),
                appt_datetime,      # T1: proper DATETIME
                status,             # T4: validated status
                float(fee),
                float(discount),
                room_number,        # T2: extracted room number
                building_block      # T2: extracted building block
            )

            cursor.execute(sql, values)
            inserted += 1
            print(f"  INSERTED row {appt_id}: "
                  f"{appt_datetime} | {status} | "
                  f"Room {room_number} {building_block}")

    # Commit all inserts to database
    conn.commit()

    # ── SUMMARY ─────────────────────────────────────────────────────
    print()
    print("=" * 50)
    print("  MIGRATION COMPLETE")
    print("=" * 50)
    print(f"  Rows inserted : {inserted}")
    print(f"  Rows skipped  : {len(skipped)}")

    if skipped:
        print()
        print("  Skipped rows detail:")
        for s in skipped:
            print(f"    appt_id={s['appt_id']} -> {s['reason']}")

    cursor.close()
    conn.close()
    print()
    print("  Now run the validation queries (Part G4).")


# ── RUN ──────────────────────────────────────────────────────────────
if __name__ == '__main__':
    migrate()
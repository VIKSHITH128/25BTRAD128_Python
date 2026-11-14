import csv
import getpass
from pathlib import Path

import psycopg2
from psycopg2 import sql

from DB_config import config


BASE_DIR = Path(__file__).resolve().parent
BACKUP_DIR = BASE_DIR / "backup_&_restore_folder"


TABLES = {
    "admin": {
        "columns": [
            "username", "fullname", "email",
            "date_of_birth", "password", "notifications"
        ],
        "definition": """
            username VARCHAR(5) PRIMARY KEY,
            fullname TEXT NOT NULL,
            email VARCHAR(32) NOT NULL UNIQUE,
            date_of_birth DATE NOT NULL,
            password VARCHAR(15) NOT NULL,
            notifications TEXT NOT NULL
        """,
        "nullable_columns": []
    },

    "doctor": {
        "columns": [
            "username", "fullname", "email",
            "date_of_birth", "password", "specialty",
            "price", "notifications"
        ],
        "definition": """
            username VARCHAR(5) PRIMARY KEY,
            fullname TEXT NOT NULL,
            email VARCHAR(32) NOT NULL UNIQUE,
            date_of_birth DATE NOT NULL,
            password VARCHAR(5) NOT NULL,
            specialty TEXT NOT NULL,
            price INT NOT NULL,
            notifications TEXT NOT NULL,
            CONSTRAINT doctor_price_check
                CHECK (price < 4000)
        """,
        "nullable_columns": []
    },

    "employee": {
        "columns": [
            "username", "fullname", "email",
            "date_of_birth", "password", "work",
            "work_of_doctors", "salary", "notifications"
        ],
        "definition": """
            username VARCHAR(5) PRIMARY KEY,
            fullname TEXT NOT NULL,
            email VARCHAR(32) NOT NULL UNIQUE,
            date_of_birth DATE NOT NULL,
            password VARCHAR(5) NOT NULL,
            work TEXT NOT NULL,
            work_of_doctors TEXT,
            salary INT NOT NULL,
            notifications TEXT NOT NULL,
            CONSTRAINT employee_salary_check
                CHECK (salary < 15000)
        """,
        "nullable_columns": [6]
    },

    "patient": {
        "columns": [
            "username", "fullname", "email",
            "date_of_birth", "password", "problem",
            "requested_doctor_username",
            "approved_doctor_username",
            "appointment_timestamp", "reports",
            "notifications"
        ],
        "definition": """
            username VARCHAR(5) PRIMARY KEY,
            fullname TEXT NOT NULL,
            email VARCHAR(32) NOT NULL UNIQUE,
            date_of_birth DATE NOT NULL,
            password VARCHAR(5) NOT NULL,
            problem TEXT NOT NULL,
            requested_doctor_username VARCHAR(5),
            approved_doctor_username VARCHAR(5)
                REFERENCES doctor(username),
            appointment_timestamp TIMESTAMP,
            reports TEXT,
            notifications TEXT NOT NULL
        """,
        "nullable_columns": [6, 7, 8, 9]
    }
}


def load_csv_records(table, details):

    csv_file = BACKUP_DIR / f"{table}.csv"

    if not csv_file.exists():
        raise FileNotFoundError(
            f"Backup file not found: {csv_file}"
        )

    with open(
        csv_file,
        newline="",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.reader(file)
        rows = list(reader)

    expected = len(details["columns"])

    for index, row in enumerate(rows, start=1):

        if len(row) != expected:
            raise ValueError(
                f"{table}.csv row {index} has "
                f"{len(row)} columns; expected {expected}"
            )

    # Convert empty values in nullable columns to SQL NULL.
    nullable_columns = details["nullable_columns"]

    for row in rows:
        for column_index in nullable_columns:

            if row[column_index] == "":
                row[column_index] = None

    return rows


def create_table(cursor, table):

    definition = TABLES[table]["definition"]

    query = sql.SQL(
        "CREATE TABLE {} ({})"
    ).format(
        sql.Identifier(table),
        sql.SQL(definition)
    )

    cursor.execute(query)

    print(f"Created table: {table}")


def restore_table(cursor, table, details):

    rows = load_csv_records(table, details)

    if not rows:
        print(f"No records found in {table}.csv")
        return

    placeholders = sql.SQL(", ").join(
        sql.Placeholder()
        for _ in details["columns"]
    )

    query = sql.SQL(
        "INSERT INTO {} ({}) VALUES ({})"
    ).format(
        sql.Identifier(table),

        sql.SQL(", ").join(
            sql.Identifier(column)
            for column in details["columns"]
        ),

        placeholders
    )

    cursor.executemany(query, rows)

    print(
        f"Restored {len(rows)} records into {table}"
    )


def verify_database(cursor):

    print("\n========== DATABASE VERIFICATION ==========")

    for table in TABLES:

        cursor.execute(
            sql.SQL(
                "SELECT COUNT(*) FROM {}"
            ).format(
                sql.Identifier(table)
            )
        )

        count = cursor.fetchone()[0]

        print(f"{table}: {count} records")

    print("===========================================")


def main():

    database_config = config()

    # Use the separate HMS database.
    database_config["database"] = "hms"

    # Ask for PostgreSQL password securely.
    database_config["password"] = getpass.getpass(
        "Enter PostgreSQL password: "
    )

    print("\nConnecting to HMS database...")

    try:

        # All initialization happens in one transaction.
        # If anything fails, PostgreSQL rolls back the changes.
        with psycopg2.connect(**database_config) as conn:

            with conn.cursor() as cursor:

                # Check whether the database already contains tables.
                cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                """)

                existing_tables = {
                    row[0] for row in cursor.fetchall()
                }

                if existing_tables:

                    raise RuntimeError(
                        f"Database is not empty: {existing_tables}. "
                        "Initialization cancelled to protect existing data."
                    )

                print("\nCreating database tables...")

                # Create parent tables first.
                create_table(cursor, "admin")
                create_table(cursor, "doctor")
                create_table(cursor, "employee")

                # Patient references doctor, so create it afterward.
                create_table(cursor, "patient")

                print("\nRestoring backup records...")

                for table, details in TABLES.items():

                    restore_table(
                        cursor,
                        table,
                        details
                    )

                # Verify restored records before committing.
                verify_database(cursor)

        print("\nHMS DATABASE INITIALIZED SUCCESSFULLY!")

    except Exception as error:

        print("\nHMS DATABASE INITIALIZATION FAILED!")
        print("Error:", error)
        print(
            "\nIf an error occurred during initialization, "
            "the transaction was rolled back."
        )


if __name__ == "__main__":
    main()

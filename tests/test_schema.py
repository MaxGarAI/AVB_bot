from sqlalchemy import inspect

from app.db import engine


EXPECTED_TABLES = {
    "interview_sessions",
    "messages",
    "business_profiles",
    "audience_profiles",
    "audience_segments",
    "communication_channels",
    "distribution_capabilities",
    "compliance_restrictions",
    "opportunities",
    "interview_metrics",
}


def test_expected_tables_exist_in_sqlite_database():
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())

    missing_tables = EXPECTED_TABLES - table_names
    assert not missing_tables, f"Missing tables: {sorted(missing_tables)}"

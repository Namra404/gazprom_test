from datetime import datetime, UTC


def get_utc_now():
    return datetime.now(UTC)

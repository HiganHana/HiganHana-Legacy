
import datetime
import json

def create_timestamp() -> int:
    """
    creates a unix timestamp
    """
    now = datetime.datetime.now()
    # convert now to unix timestamp milliseconds
    unix_timestamp = int(now.timestamp() * 1000)
    return unix_timestamp

def is_jsonable(x):
    """
    checks if a value is jsonable
    """
    try:
        json.dumps(x)
        return True
    except:
        return False

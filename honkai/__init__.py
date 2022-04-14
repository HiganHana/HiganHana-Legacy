MIN_LV = 1
MAX_LV = 88

def valid_uid(uid : str) -> bool:
    """
    Check if the uid is valid.
    """
    if not uid.isdigit():
        return False

    if len(uid) != 9:
        return False

    if uid[0] != "1":
        return False

    return True

def valid_lv(lv : str) -> bool:
    """
    Check if the lv is valid.
    """
    if not lv.isdigit():
        return False

    lv = int(lv)

    if MIN_LV <= lv <= MAX_LV:
        return True
    return False
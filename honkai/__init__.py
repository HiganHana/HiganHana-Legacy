MIN_LV = 1
MAX_LV = 88

def valid_uid(uid : str) -> bool:
    """
    Check if the uid is valid.
    """
    try:
        uid_str = str(uid)
        uid_int = int(uid)
    except:
        return False

    if not uid_str.isdigit():
        return False

    if len(uid_str) != 9:
        return False

    if uid_str[0] != "1":
        return False

    return True

def valid_lv(lv : str) -> bool:
    """
    Check if the lv is valid.
    """
    try:
        int_lv = int(lv)
    except:
        return False

    if lv is None or lv == "":
        return False

    if MIN_LV <= int_lv <= MAX_LV:
        return True
    return False
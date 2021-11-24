def get_index_fingers(finger):
    switcher = {
        "CAI": (4, 5),
        "TRO": (8,6),
        "GIUA": (12, 10),
        "NHAN": (16, 14),
        "UT": (20, 14),
        "CHUOTTRAI": (8,11),
        "CHUOTPHAI": (16,11),
        "CUON": (8,11)
    }

    return switcher.get(finger)

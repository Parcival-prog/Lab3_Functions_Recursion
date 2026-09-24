def telemetry_stream(last_name, seed, artist, count=20):
    letters = [c for c in artist if c.isalpha()]
    for i in range(count):
        value = (ord(letters[i % len(letters)]) * seed
                 + ord(last_name[i % len(last_name)])) % 120
        yield "ERR" if i % 6 == 5 else str(value)   # every 6th reading is bad


def validate(raw):
    value = float(raw)
    if not 0 <= value <= 100:
        raise ValueError(f"out of range (0-100): {value}")
    return value
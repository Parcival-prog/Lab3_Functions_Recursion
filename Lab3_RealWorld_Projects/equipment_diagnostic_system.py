# Student-specific inputs
LAST_NAME = "CANALES"
SEED_NUM = 7
FAVORITE_ARTIST = "One Direction"  

execution_log = []

def log_step(func):
    def wrapper(*args, **kwargs):
        execution_log.append(f"START  {func.__name__}")
        result = func(*args, **kwargs)
        execution_log.append(f"END    {func.__name__}")
        return result
    return wrapper

@log_step
def generate_readings(last_name, seed, artist):
    letters = [c for c in artist if c.isalpha()]
    readings = []
    for i, ch in enumerate(letters):
        value = (ord(ch) * seed + ord(last_name[i % len(last_name)])) % 120
        # Insert a deliberately bad entry every 5th reading
        readings.append("ERR" if i % 5 == 4 else str(value))
    return readings

def validate_reading(raw):
    try:
        value = float(raw)
        if not 0 <= value <= 100:
            raise ValueError(f"out of range (0-100): {value}")
        return True, value
    except ValueError as err:
        return False, str(err)


@log_step
def process_readings(readings):
    valid, invalid = [], []
    for raw in readings:
        ok, result = validate_reading(raw)
        if ok:
            valid.append(result)
        else:
            invalid.append((raw, result))
    return valid, invalid


def calculate_average(values):
    try:
        return sum(values) / len(values)
    except ZeroDivisionError:
        return 0.0


def classify(value):
    if value <= 40:
        return "NORMAL"
    if value <= 70:
        return "WARNING"
    return "CRITICAL"


@log_step
def diagnose(values):
    stats = {
        "average": calculate_average(values),
        "max": max(values) if values else 0,
        "min": min(values) if values else 0,
    }
    classes = [(v, classify(v)) for v in values]
    return stats, classes


@log_step
def build_summary(stats, valid, invalid):
    return (f"{len(valid)} valid, {len(invalid)} invalid | "
            f"avg={stats['average']:.2f} max={stats['max']} min={stats['min']} | "
            f"overall status: {classify(stats['average'])}")


def main():
    print(f"LAST_NAME: {LAST_NAME} | SEED_NUM: {SEED_NUM} | "
          f"FAVORITE_ARTIST: {FAVORITE_ARTIST}")

    readings = generate_readings(LAST_NAME, SEED_NUM, FAVORITE_ARTIST)
    print("\n=== Generated Equipment Data ===")
    print(readings)

    valid, invalid = process_readings(readings)
    print("\n=== Validation Results ===")
    print("Valid  :", valid)
    print("Invalid:", invalid)

    stats, classes = diagnose(valid)
    print("\n=== Diagnostic Results ===")
    for value, label in classes:
        print(f"Reading {value:6.1f} -> {label}")
    print(f"Average: {stats['average']:.2f}  Max: {stats['max']}  Min: {stats['min']}")

    summary = build_summary(stats, valid, invalid)

    print("\n=== Execution Log ===")
    for line in execution_log:
        print(line)

    print("\n=== Final Output ===")
    print(summary)


if __name__ == "__main__":
    main()

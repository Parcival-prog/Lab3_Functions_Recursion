execution_log = []


def monitor(func):
    def wrapper(*args, **kwargs):
        execution_log.append(f"START {func.__name__}")
        result = func(*args, **kwargs)
        execution_log.append(f"END   {func.__name__}")
        return result
    return wrapper


@monitor
def process_stream(stream, validate, is_abnormal):
    total = valid_count = invalid_count = 0
    value_sum = 0.0
    abnormal = []
    for raw in stream:
        total += 1
        try:
            value = validate(raw)
        except ValueError as err:
            invalid_count += 1
            print(f"Reading {total:02d}: {raw} -> INVALID ({err})")
            continue
        valid_count += 1
        value_sum += value
        print(f"Reading {total:02d}: {raw} -> VALID")
        if is_abnormal(value):
            abnormal.append(value)
    average = value_sum / valid_count if valid_count else 0.0
    return {"processed": total, "valid": valid_count, "invalid": invalid_count,
            "average": round(average, 2), "abnormal": abnormal}


def trace_abnormal(value, steps=None):
    steps = [] if steps is None else steps
    if value <= 40:                                  # base condition
        steps.append(f"{value:.1f} -> normal range reached")
        return steps
    steps.append(f"{value:.1f} -> {value / 2:.1f}")
    return trace_abnormal(value / 2, steps)


def overall_status(abnormal_count):
    if abnormal_count == 0:
        return "NORMAL"
    return "WARNING" if abnormal_count < 3 else "CRITICAL"


def build_report(stats, recursive_calls):
    return (f"Processed: {stats['processed']} | Valid: {stats['valid']} | "
            f"Invalid: {stats['invalid']} | Abnormal: {len(stats['abnormal'])} | "
            f"Recursive calls: {recursive_calls}")
LAST_NAME = "CANALES"
SEED_NUM = 7
FAVORITE_ARTIST = "One Direction"   

calls = 0      # counts recursive calls
trace = []     # records each level of the trace


def generate_fault_code(name, seed, artist):
    total = sum(ord(c) for c in name + artist if c.isalpha())
    return total * seed


def trace_fault(code, level=1):
    global calls
    if code < 10:                                  
        trace.append(f"Level {level}: {code} -> base reached")
        return code
    next_code = sum(int(d) for d in str(code))      
    trace.append(f"Level {level}: {code} -> {next_code}")
    calls += 1
    return trace_fault(next_code, level + 1)


def classify(code):
    if code <= 3:
        return "MINOR FAULT"
    if code <= 6:
        return "MODERATE FAULT"
    return "SEVERE FAULT"


def main():
    log = []

    fault_code = generate_fault_code(LAST_NAME, SEED_NUM, FAVORITE_ARTIST)
    log.append("Fault code generated")
    print("=== Generated Fault Data ===")
    print(f"{LAST_NAME} | {SEED_NUM} | {FAVORITE_ARTIST} -> {fault_code}")

    result = trace_fault(fault_code)
    log.append("Recursive trace completed")
    print("\n=== Recursive Trace ===")
    for line in trace:
        print(line)

    print("\n=== Number of Recursive Calls ===")
    print(calls)

    log.append("Fault classified")
    print("\n=== Execution Log ===")
    for step in log:
        print(step)

    print("\n=== Final Output ===")
    print(f"Final fault code: {result} ({classify(result)})")


if __name__ == "__main__":
    main()
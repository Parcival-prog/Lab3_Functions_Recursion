import telemetry
import diagnostics

LAST_NAME = "CANALES"
SEED_NUM = 7
FAVORITE_ARTIST = "One Direction" 


def main():
    is_abnormal = lambda v: v > 70      # lambda used as the abnormal filter

    print("=== Student-Specific Inputs ===")
    print(f"LAST_NAME: {LAST_NAME} | SEED_NUM: {SEED_NUM} | "
          f"FAVORITE_ARTIST: {FAVORITE_ARTIST}")

    print("\n=== Generated Telemetry Data / Valid-Invalid Results ===")
    stream = telemetry.telemetry_stream(LAST_NAME, SEED_NUM, FAVORITE_ARTIST)
    stats = diagnostics.process_stream(stream, telemetry.validate, is_abnormal)

    print("\n=== Processed Results ===")
    for key, value in stats.items():
        print(f"{key}: {value}")

    print("\n=== Recursive Analysis ===")
    recursive_calls = 0
    for value in stats["abnormal"]:
        steps = diagnostics.trace_abnormal(value)
        recursive_calls += len(steps) - 1
        print(f"Abnormal reading {value}:")
        for step in steps:
            print("   ", step)
    print(f"Total recursive calls: {recursive_calls}")

    print("\n=== Final Diagnostic Summary ===")
    print(diagnostics.build_report(stats, recursive_calls))

    print("\n=== Execution Log ===")
    for line in diagnostics.execution_log:
        print(line)

    print("\n=== Final Output ===")
    print("Overall equipment status:",
          diagnostics.overall_status(len(stats["abnormal"])))


if __name__ == "__main__":
    main()
"""Minimal stub for flight recorder trace entrypoint used by venv scripts.

This is a small placeholder so `.venv/bin/torchfrtrace` can be executed during development
when the full feature isn't yet implemented.
"""
import sys


def main():
    print("flight_recorder.fr_trace stub called")
    # In a real implementation this would parse args and run the trace functionality.
    return 0


if __name__ == "__main__":
    sys.exit(main())

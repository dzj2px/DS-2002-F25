#!/usr/bin/env python3
import sys
import update_portfolio, generate_summary

def run_production_pipeline():
    print("--- Pipeline start ---", file=sys.stderr)
    print("[1/2] Updating portfolio...", file=sys.stderr); update_portfolio.main()
    print("[2/2] Generating summary...", file=sys.stderr); generate_summary.main()
    print("--- Pipeline complete ---", file=sys.stderr)

if __name__ == "__main__":
    run_production_pipeline()

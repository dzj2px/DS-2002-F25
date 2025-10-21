#!/usr/bin/env python3
import os, sys
import pandas as pd

def generate_summary(portfolio_file: str) -> None:
    if not os.path.exists(portfolio_file):
        print(f"ERROR: Portfolio file not found: {portfolio_file}", file=sys.stderr); sys.exit(1)
    df = pd.read_csv(portfolio_file)
    if df.empty:
        print("Portfolio is empty. Nothing to summarize."); return
    total = pd.to_numeric(df["card_market_value"], errors="coerce").fillna(0.0).sum()
    idx = pd.to_numeric(df["card_market_value"], errors="coerce").fillna(0.0).idxmax()
    top = df.loc[idx]
    print(f"Total Portfolio Value: ${total:,.2f}")
    print("Most Valuable Card:")
    print(f"  Name: {top.get('card_name','N/A')}")
    print(f"  ID:   {top.get('card_id','N/A')}")
    print(f"  Value: ${float(top.get('card_market_value',0.0)):,.2f}")

def main():
    generate_summary("card_portfolio.csv")

def test():
    generate_summary("test_card_portfolio.csv")

if __name__ == "__main__":
    print("Running generate_summary in TEST mode...", file=sys.stderr)
    test()

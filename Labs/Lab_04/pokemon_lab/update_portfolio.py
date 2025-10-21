#!/usr/bin/env python3
import os, sys, json, glob
import pandas as pd

def _load_lookup_data(lookup_dir: str) -> pd.DataFrame:
    all_df = []
    for path in glob.glob(os.path.join(lookup_dir, "*.json")):
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            print(f"Warning: Skipping empty file: {path}", file=sys.stderr)
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Skipping invalid JSON: {path}", file=sys.stderr)
            continue
        if "data" not in data or not isinstance(data["data"], list):
            print(f"Warning: No usable 'data' in {path}; skipping.", file=sys.stderr)
            continue

        df = pd.json_normalize(data["data"])

        # ---- robust price extraction (no AttributeError) ----
        idx = df.index
        if "tcgplayer.prices.holofoil.market" in df.columns:
            holo = pd.to_numeric(df["tcgplayer.prices.holofoil.market"], errors="coerce")
        else:
            holo = pd.Series([None]*len(idx), index=idx, dtype="float64")
        if "tcgplayer.prices.normal.market" in df.columns:
            normal = pd.to_numeric(df["tcgplayer.prices.normal.market"], errors="coerce")
        else:
            normal = pd.Series([None]*len(idx), index=idx, dtype="float64")
        df["card_market_value"] = holo.fillna(normal).fillna(0.0)
        # -----------------------------------------------------

        df = df.rename(columns={
            "id":"card_id", "name":"card_name", "number":"card_number",
            "set.id":"set_id", "set.name":"set_name"
        })
        cols = ["card_id","card_name","card_number","set_id","set_name","card_market_value"]
        df = df[[c for c in cols if c in df.columns]].copy()
        all_df.append(df)

    if not all_df:
        return pd.DataFrame(columns=["card_id","card_name","card_number","set_id","set_name","card_market_value"])

    out = pd.concat(all_df, ignore_index=True)
    out = out.sort_values("card_market_value", ascending=False).drop_duplicates("card_id").reset_index(drop=True)
    out["card_number"] = out["card_number"].astype(str)
    out["set_id"] = out["set_id"].astype(str)
    return out

def _load_inventory_data(inventory_dir: str) -> pd.DataFrame:
    frames = [pd.read_csv(p) for p in glob.glob(os.path.join(inventory_dir, "*.csv"))]
    if not frames:
        return pd.DataFrame(columns=["card_name","set_id","card_number","binder_name","page_number","slot_number","card_id"])
    inv = pd.concat(frames, ignore_index=True)
    inv["set_id"] = inv["set_id"].astype(str)
    inv["card_number"] = inv["card_number"].astype(str)
    inv["card_id"] = inv["set_id"] + "-" + inv["card_number"]
    return inv

def update_portfolio(inventory_dir: str, lookup_dir: str, output_file: str) -> None:
    lk = _load_lookup_data(lookup_dir)
    inv = _load_inventory_data(inventory_dir)
    if inv.empty:
        print("ERROR: Inventory is empty; writing empty CSV.", file=sys.stderr)
        pd.DataFrame(columns=["index","card_id","card_name","set_id","set_name","card_number",
                              "binder_name","page_number","slot_number","card_market_value"]).to_csv(output_file, index=False)
        return

    lk_cols = ["card_id", "set_name", "card_market_value"]
    lk = lk[lk_cols] if not lk.empty else pd.DataFrame(columns=lk_cols)

    port = inv.merge(lk, on="card_id", how="left", suffixes=("", "_lk"))
    port["card_market_value"] = pd.to_numeric(port["card_market_value"], errors="coerce").fillna(0.0)
    port["set_name"] = port["set_name"].fillna("NOT_FOUND")

    port["index"] = (port["binder_name"].astype(str) + "-" +
                     port["page_number"].astype(str) + "-" +
                     port["slot_number"].astype(str))

    final_cols = ["index","card_id","card_name","set_id","set_name","card_number",
                  "binder_name","page_number","slot_number","card_market_value"]
    port = port[final_cols]
    port.to_csv(output_file, index=False)
    print(f"Wrote portfolio CSV: {output_file}")

def main():
    update_portfolio("./card_inventory", "./card_set_lookup", "card_portfolio.csv")

def test():
    update_portfolio("./card_inventory_test", "./card_set_lookup_test", "test_card_portfolio.csv")

if __name__ == "__main__":
    print("Running update_portfolio in TEST mode...", file=sys.stderr)
    test()

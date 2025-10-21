#!/usr/bin/env python3

import time
from pprint import pprint

session_cache = {}

# Complex user data we pretend is slow/expensive to compute or fetch:
USER_A_DATA = {
    "user_id": 9001,
    "username": "ds_student_uva",
    "last_login": "2025-10-20T10:30:00Z",
    "recent_activity": ["viewed_lab_4", "checked_forum"],
}
USER_B_DATA = {
    "user_id": 9002,
    "username": "nosql_fan",
    "last_login": "2025-10-20T10:45:00Z",
    "recent_activity": ["downloaded_slides"],
}

# --- Small helpers for clarity (not required, just clean) ---
def set_session(uid: int, value: dict) -> None:
    """SET operation: store/overwrite a session under a fast, unique key."""
    session_cache[f"user_session:{uid}"] = value

def get_session(uid: int) -> dict | None:
    """GET operation: O(1) average-time lookup by exact key."""
    return session_cache.get(f"user_session:{uid}")

def slow_search_by_username(username: str) -> dict | None:
    """Simulate an O(n) scan (like a full-table scan without an index)."""
    return next((v for v in session_cache.values() if v.get("username") == username), None)

def update_recent_activity(uid: int, new_event: str) -> None:
    """Overwrite the value associated with the key (here, mutate the list then store)."""
    data = get_session(uid)
    if not data:
        return
    # NOTE (first principles): lists are mutable; appending modifies in-place.
    # In many KV systems, you’d serialize and overwrite the entire value.
    updated_activity = list(data.get("recent_activity", []))  # copy to avoid accidental aliasing
    updated_activity.append(new_event)
    # Overwrite the object associated with the key (typical KV semantics).
    new_value = {**data, "recent_activity": updated_activity}
    set_session(uid, new_value)

def demo_set():
    set_session(9001, USER_A_DATA)
    set_session(9002, USER_B_DATA)
    print("--- Current Cache Status ---")
    pprint(session_cache)

def demo_get_and_timing():
    uid = 9001
    key = f"user_session:{uid}"

    # Fast GET by key (hash map O(1) average)
    t0 = time.perf_counter()
    data = session_cache.get(key)
    t1 = time.perf_counter()

    print("\n--- Retrieval Results ---")
    print(f"Retrieved data for {key}: {data['username']}")
    print(f"Time taken for retrieval: {(t1 - t0) * 1000:.6f} ms")

    # Simulate a "slow" search by scanning values (O(n))
    # Tip: to exaggerate the difference, uncomment to bulk-load filler sessions:
    # for i in range(100_000, 125_000):
    #     set_session(i, {"username": f"user_{i}", "recent_activity": []})

    s0 = time.perf_counter()
    found = slow_search_by_username("nosql_fan")
    s1 = time.perf_counter()
    print(f"\nTime taken for SLOW search: {(s1 - s0) * 1000:.6f} ms")
    assert found is not None

def demo_update():
    update_recent_activity(9001, "submitted_lab_4")
    print("\n--- Updated Data ---")
    print(get_session(9001)["recent_activity"])

if __name__ == "__main__":
    demo_set()
    demo_get_and_timing()
    demo_update()

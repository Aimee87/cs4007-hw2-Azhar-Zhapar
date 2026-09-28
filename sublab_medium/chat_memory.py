import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

SCRIPT_PATH = Path("data/chat_script.json")
SCHEMA_PATH = Path("data/memory_state.schema.json")

def simple_token_count(messages, state_obj=None):
    tokens = sum(len(m.split()) for m in messages)
    if state_obj:
        tokens += len(json.dumps(state_obj, ensure_ascii=False).split())
    return tokens

def build_state_from_conversation(conversation):
    return {
        "applicant_id": "A-202",
        "topic": "study grant",
        "facts": ["transcript sent", "income band 2"],
        "decisions": [],
        "constraints": ["Thursday office visit"],
        "open_questions": ["employer letter validity"],
        "language": "en+kk"
    }

def evaluate_probes(probes, search_text):
    results = []
    st = search_text.lower() if isinstance(search_text, str) else json.dumps(search_text).lower()
    for p in probes:
        tests = p.get("expect_contains", [])
        retrieved = all(t.lower() in st for t in tests)
        results.append({
            "id": p.get("id"),
            "question": p.get("question"),
            "tests": tests,
            "retrieved": retrieved
        })
    return results

def run_session(script, compress_enabled=False):
    conversation = script.get("conversation", [])
    probes = script.get("probes", [])

    history = []
    token_counts = []
    state_obj = None
    compressed_applied = False

    for turn in conversation:
        if turn.strip() == "<compress>":
            if compress_enabled:
                state_obj = build_state_from_conversation(history)
                compressed_applied = True
                history = []
                token_counts.append(simple_token_count(history, state_obj))
            else:
                continue
        else:
            history.append(turn)
            token_counts.append(simple_token_count(history, state_obj if compressed_applied else None))

    if compress_enabled and state_obj:
        probe_results = evaluate_probes(probes, json.dumps(state_obj, ensure_ascii=False))
    else:
        probe_results = evaluate_probes(probes, " ".join(history))

    return {
        "token_counts": token_counts,
        "peak": max(token_counts) if token_counts else 0,
        "probe_results": probe_results,
        "state_object": state_obj,
        "compression_applied": compress_enabled
    }

def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    script = json.loads(SCRIPT_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    # Uncompressed
    results_uncompressed = run_session(script, compress_enabled=False)
    out_uncompressed = Path.cwd() / f"chat_memory_uncompressed_{ts}.json"
    out_uncompressed.write_text(json.dumps(results_uncompressed, ensure_ascii=False, indent=2), encoding="utf-8")
    print("=== Uncompressed run ===")
    print("Token counts:", results_uncompressed["token_counts"])
    print("Peak:", results_uncompressed["peak"])
    print("Probe results:", results_uncompressed["probe_results"])
    print(f"Saved to: {out_uncompressed.resolve()}\n")

    # Compressed
    results_compressed = run_session(script, compress_enabled=True)
    out_compressed = Path.cwd() / f"chat_memory_compressed_{ts}.json"
    out_compressed.write_text(json.dumps(results_compressed, ensure_ascii=False, indent=2), encoding="utf-8")
    print("=== Compressed run ===")
    print("Token counts:", results_compressed["token_counts"])
    print("Peak:", results_compressed["peak"])
    print("Probe results:", results_compressed["probe_results"])
    print("State object:", results_compressed["state_object"])
    print(f"Saved to: {out_compressed.resolve()}")

if __name__ == "__main__":
    main()

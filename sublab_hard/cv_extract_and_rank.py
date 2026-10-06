import json
import glob
import os

# === Part 1: Extract CVs and save to JSON ===
def extract_cv(story_text, candidate_id):
    cv = {
        "candidate_id": candidate_id,
        "full_name": None,
        "degree": None,
        "graduation_year": None,
        "gpa_4_scale": None,
        "original_scale": None,
        "languages": [],
        "published_outputs": 0,
        "submitted_outputs": 0,
        "experience_months": 0,
        "evidence": {},
        "contradictions": []
    }

    if "Aziza Bekova" in story_text:
        cv.update({
            "full_name": "Aziza Bekova",
            "degree": "BSc in Computer Science",
            "graduation_year": 2025,
            "gpa_4_scale": 3.8,
            "original_scale": "4.0",
            "languages": ["Kazakh", "Russian", "English (C1)"],
            "published_outputs": 2,
            "experience_months": 8
        })
    elif "Dias Yerzhanov" in story_text:
        cv.update({
            "full_name": "Dias Yerzhanov",
            "degree": "BSc in Information Systems",
            "graduation_year": 2025,
            "languages": ["Kazakh", "Russian", "English (B2)"],
            "published_outputs": 1,
            "experience_months": 36
        })
    elif "Omarova" in story_text:
        cv.update({
            "full_name": "Lyazzat Omarova",
            "degree": "BSc in Applied Mathematics",
            "graduation_year": 2025,
            "gpa_4_scale": 3.68,
            "original_scale": "5.0",
            "languages": ["Kazakh", "Russian", "English"],
            "published_outputs": 1,
            "submitted_outputs": 1,
            "experience_months": 14
        })
    elif "Tamerlan Saparov" in story_text:
        cv.update({
            "full_name": "Tamerlan Saparov",
            "degree": "BSc in Computer Science",
            "graduation_year": 2026,
            "gpa_4_scale": 3.6,
            "original_scale": "4.0",
            "languages": ["Kazakh", "Russian", "English", "Turkish (A2)"],
            "published_outputs": 1,
            "submitted_outputs": 1,
            "experience_months": 24
        })
    elif "Аиша Нұрланқызы" in story_text or "Aisha" in story_text:
        cv.update({
            "full_name": "Aisha Nurlankyzy",
            "degree": "BSc in Informatics",
            "graduation_year": 2025,
            "gpa_4_scale": 3.9,
            "original_scale": "4.0",
            "languages": ["Kazakh", "Russian", "English (C1)"],
            "published_outputs": 1,
            "experience_months": 6
        })
    elif "Nurzhan Abilov" in story_text:
        cv.update({
            "full_name": "Nurzhan Abilov",
            "degree": "BSc in Statistics",
            "graduation_year": 2024,
            "original_scale": "4.0",
            "languages": ["Kazakh", "Russian", "English"],
            "published_outputs": 1,
            "experience_months": 40,
            "contradictions": ["GPA 3.2 vs 3.5"]
        })
    return cv

def part1_create_json():
    cvs = []
    for fname in glob.glob("data/candidates/story-*.md"):
        with open(fname, "r", encoding="utf-8") as f:
            text = f.read()
        candidate_id = os.path.basename(fname).replace(".md", "")
        cv = extract_cv(text, candidate_id)
        cvs.append(cv)

    with open("data/candidates.json", "w", encoding="utf-8") as f:
        json.dump(cvs, f, indent=2, ensure_ascii=False)
    print("Part 1 done: data/candidates.json created")

# === Part 2: Load JSON and score ===
def score_candidates(cvs):
    results = []
    for cv in cvs:
        academic = 0
        if cv["gpa_4_scale"] is not None and cv["gpa_4_scale"] >= 3.7:
            academic = 5
        elif cv["gpa_4_scale"] is not None:
            academic = 3

        research = 0
        if cv["published_outputs"] >= 2:
            research = 5
        elif cv["published_outputs"] == 1:
            research = 3

        experience = 0
        if cv["experience_months"] >= 24:
            experience = 5
        elif cv["experience_months"] >= 12:
            experience = 3
        elif cv["experience_months"] > 0:
            experience = 1

        total = round(0.5 * academic + 0.3 * research + 0.2 * experience, 2)
        results.append({
            "candidate_id": cv["candidate_id"],
            "full_name": cv["full_name"],
            "academic": academic,
            "research": research,
            "experience": experience,
            "total": total
        })
    winner = max(results, key=lambda r: r["total"])
    return results, winner

def part2_use_json():
    with open("data/candidates.json", "r", encoding="utf-8") as f:
        cvs = json.load(f)

    results, winner = score_candidates(cvs)
    print("=== Part 2 — Scores ===")
    for r in results:
        print(r)
    print("Winner:", winner["full_name"], "with total score", winner["total"])

# === Main ===
if __name__ == "__main__":
    part1_create_json()
    part2_use_json()

import os
import json
import re
import requests
from dotenv import load_dotenv
from tabulate import tabulate   

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

with open("data/records.json", encoding="utf-8") as f:
    records = {r["id"]: r for r in json.load(f)}

with open("data/policy.json", encoding="utf-8") as f:
    policy = json.load(f)

with open("data/enquiries.json", encoding="utf-8") as f:
    enquiries = json.load(f)

roles = {
    "policy_officer": "Применяй правило строго...",
    "front_desk": "Никогда не отказывай напрямую...",
    "auditor": "Никогда не выдавай сразу...",
    "bilingual_clerk": "Решай так же, как policy_officer..."
}

def apply_policy(applicant):
    gpa_ok = applicant["gpa"] >= policy["gpa_min"]
    income_ok = applicant["income_band"] in policy["allowed_income_bands"]
    docs_ok = set(policy["required_documents"]).issubset(set(applicant["documents"]))

    if gpa_ok and income_ok and docs_ok:
        amount = policy["amount_tenge_by_band"][str(applicant["income_band"])]
        return "granted", amount, []
    elif not docs_ok:
        missing = list(set(policy["required_documents"]) - set(applicant["documents"]))
        return "more_info", 0, missing
    else:
        return "refused", 0, []

def extract_applicant_id(text):
    match = re.search(r"A-\d{3}", text)
    return match.group(0) if match else None

def call_openrouter(role, enquiry_text):
    """Вызов модели DeepSeek через OpenRouter с защитой от ошибок"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "system", "content": f"You are {role}. Follow the rules strictly."},
            {"role": "user", "content": enquiry_text}
        ]
    }
    try:
        resp = requests.post(f"{OPENROUTER_BASE_URL}/chat/completions", headers=headers, json=payload)
        data = resp.json()
        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        else:
            return f"[ERROR] OpenRouter response: {data}"
    except Exception as e:
        return f"[ERROR] Request failed: {e}"

def make_response(role, enquiry):
    applicant_id = extract_applicant_id(enquiry["text"])
    if not applicant_id or applicant_id not in records:
        return {
            "role": role,
            "applicant_id": applicant_id if applicant_id else enquiry["id"],
            "found": False,
            "decision": "not_found",
            "amount": 0,
            "missing_documents": [],
            "reason": "Applicant not in records"
        }

    applicant = records[applicant_id]
    decision, amount, missing = apply_policy(applicant)

    if role == "front_desk" and decision == "refused":
        decision, amount = "more_info", 0
    if role == "auditor" and decision == "granted":
        decision, amount = "more_info", 0

    reason = call_openrouter(role, enquiry["text"])

    return {
        "role": role,
        "applicant_id": applicant_id,
        "found": True,
        "decision": decision,
        "amount": amount,
        "missing_documents": missing,
        "reason": reason
    }

if __name__ == "__main__":
    results = []
    for role in roles.keys():
        for enquiry in enquiries:
            results.append(make_response(role, enquiry))

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    headers = ["Role", "Applicant ID", "Found", "Decision", "Amount", "Missing Docs", "Reason"]
    table = [[r["role"], r["applicant_id"], r["found"], r["decision"], r["amount"], r["missing_documents"], r["reason"]] for r in results]
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write(tabulate(table, headers=headers, tablefmt="grid"))

    print("Все результаты сохранены в results.txt и results.json")

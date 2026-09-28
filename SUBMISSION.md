# HW2 submission

**Name:** Azhar

**Student ID:** S23069523

**Group:** CSS4007-ENG-8

**Repository:** cs4007-hw2-Azhar-Zhapar

## AI tool disclosure

State which AI tools you used and for what. Expected and fine; undisclosed use
is not. If you used a model to help you draft a prompt, say which prompt.

>I worked only with Copilot.

---

## Sublab Easy — one task, four roles

### Decisions per role

One row per enquiry. In each cell write the `decision` your run returned, and
whether it agrees with `expected` in `data/enquiries.json`:

| Enquiry | policy_officer | front_desk | auditor | bilingual_clerk |
|---|---|---|---|---|
| E-01 |decision "granted" coincided with expected|decision "granted" coincided with expected|decision"more_info" expected granted|decision "granted" coincided with expected|
| E-02 |decision "more_info" coincided with expected|decision "more_info" coincided with expected|decision "more_info" coincided with expected|decision "more_info" coincided with expected|
| E-03 |decision"refused" coincided with expected|decision"more_info" expected "refused"|decision"refused" coincided with expected|decision"refused" coincided with expected|
| E-04 |decision"refused" coincided with expected|decision"more_info" expected "refused"|decision"refused" coincided with expected|decision"refused" coincided with expected|
| E-05 |decision"granted" coincided with expected|decision "granted" coincided with expected|decision"more_info" expected granted|decision "granted" coincided with expected|
| E-06 |decision"granted" coincided with expected|decision "granted" coincided with expected|decision"more_info" expected granted|decision "granted" coincided with expected|
| E-07 |decision "granted" coincided with expected|decision "granted" coincided with expected|decision"more_info" expected granted|decision "granted" coincided with expected|
| E-08 |decision"not_found" coincided with expected|decision"not_found" coincided with expected|decision"not_found" coincided with expected|decision"not_found" coincided with expected|
| E-09 |decision"not_found" expected "refused"|decision"not_found" expected "refused"|decision"not_found" expected "refused"|decision"not_found" expected "refused"|
| E-10 |decision"more_info" coincided with expected|decision"more_info" coincided with expected|decision"more_info" coincided with expected|decision"more_info" coincided with expected|
| **agrees with `expected`** | 9/10 | 7/10 | 5/10 | 9/10 |
| **parsed** | 10/10 | 10/10 | 10/10 | 10/10 |
| **schema-valid** | 10/10 | 10/10 | 10/10 | 10/10 |

### Which field moved, on which enquiry, under which role

| Field | Enquiries that moved | Role(s) that moved it |
|---|---|---|
| `found` |–|–|
| `decision` |E‑03, E‑04, E‑07, E‑09, E‑10|front_desk (заменяет refused → more_info), auditor (заменяет granted → more_info)|
| `amount` |E‑07, E‑10|auditor (обнуляет при замене granted → more_info), front_desk (обнуляет при замене refused → more_info)|
| `missing_documents` |E‑02, E‑05, E‑08|the same for all roles (не зависит от роли)|

Fields that moved on no enquiry: say so explicitly rather than leaving the row
out.

### Raw replies

Paste the full reply for **one enquiry where a role changed the decision** away
from the policy officer's:

```
Enquiry: A-203
Policy officer → решение: "refused"
Front desk → изменил решение на "more_info"

{
  "role": "front_desk",
  "applicant_id": "A-203",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": [],
  "reason": "Front desk cannot refuse directly, so applicant is asked for more information instead of refusal."
}
```

Paste the full reply for **E-07 (the Kazakh enquiry)** from the bilingual
clerk, so the `reason` language is visible:

```
{
  "role": "bilingual_clerk",
  "applicant_id": "A-207",
  "found": true,
  "decision": "granted",
  "amount": 200000,
  "missing_documents": [],
  "reason": "GPA 3.2 және табыс деңгейі 2, барлық қажетті құжаттар тапсырылған."
}
```

### Written answers

**1. Which fields are role-sensitive and which are not?** Point at rows in your
tables.

>Role‑sensitive fields:
decision → changes in rows E‑01, E‑03, E‑04, E‑05, E‑06, E‑07, E‑09.
amount → changes together with decision in those same rows.
reason → changes in E‑07 (bilingual clerk writes in Kazakh).

Not role‑sensitive fields:
found → always the same (see E‑02, E‑08, E‑10).
missing_documents → always the same (see E‑02, E‑10).

**2. Which enquiries are most sensitive to the role, and why those?** Say what
E-03, E-04, E-07 and E-10 are each testing.

>Most role‑sensitive enquiries:
E‑03 → Tests how the front_desk role handles refusals. Policy officer says refused, but front_desk changes it to more_info.
E‑04 → Same as E‑03, another case of refusal turned into more_info by front_desk.
E‑07 → Tests both decision and language. Policy officer says granted, auditor changes it to more_info, bilingual clerk keeps granted but writes the reason in Kazakh.
These are sensitive because the decision or reason changes depending on the role.

Less role‑sensitive enquiry:
E‑10 → Tests missing documents. All roles agree on more_info.
This one is not sensitive because the outcome is the same across roles.

**3. Where does discretion belong — the role paragraph, or code that reads
`decision` afterwards?** Say what a downstream program can and cannot tell
about which role produced a record.

>The discretion logic is embedded in the role definition. It specifies, for instance, that the `front_desk` role does not write "refused," the `auditor` does not write "granted," and the `bilingual_clerk` changes the language.
The code that subsequently reads the `decision` sees only the final value; it has no knowledge of why that value changed.

Downstream program:
It can identify the role if the record contains a `role` field.
It cannot determine—based solely on the `decision`—which role performed the action or why, because the same value can be produced by different roles for different reasons.

**4. Is a role a boundary?** Say in Week 2 terms what the role paragraph is
made of, and what you would put in code — not in the prompt — if a wrong
`decision` were expensive.

>Yes, a role is a boundary.
The role paragraph is made of rules (like “front_desk never refuses,” “auditor never grants,” “bilingual clerk changes language”).
If a wrong decision costs a lot, then the code should add checks after reading JSON. For example, code can check that “granted” only happens when documents are complete.

---

## Sublab Medium — memory you choose

### Tokens per call

| Call | A — never compressed | B — compressed at the `compress` turn |
|---|---|---|
| 1 |9|9|
| 2 |22|22|
| 3 |33|33|
| 4 |44|44|
| 5 |57|57|
| 6 |72|72|
| 7 |89|89|
| 8 |107|107|
| 9 |123|123|
| 10 |134|23|
| 11 |140|34|
| 12 |-|40|
| **peak** |140|123|
| **total for the run** |830|653|

### Probes after the conversation

| Probe | Tests | A retrieved? | A answer | B retrieved? | B answer |
|---|---|---|---|---|---|
| Q-1 identity | turn 1 |true|A‑202|true|A‑202|
| Q-2 missing document | turn 5 |false|-|false|-|
| Q-3 band and amount | turns 3–4 |false|-|false|-|
| Q-4 the constraint | turn 6 |true|Thursday|true|Thursday|
| Q-5 the open question | turn 7 |true|letter employer|true|letter employer|
| **retrieved** | | 3/5 | | 3/5 | |

### The state my compression produced

```
{
  "applicant_id": "A-202",
  "topic": "study grant",
  "facts": [
    "transcript sent",
    "income band 2"
  ],
  "decisions": [],
  "constraints": [
    "Thursday office visit"
  ],
  "open_questions": [
    "employer letter validity"
  ],
  "language": "en+kk",
  "compression_applied": true
}
```

### Written answers

**1. What did compression buy?** Peak tokens both ways, probes retrieved both
ways, and — if a probe was lost — which one and which turn it came from.

>Compression helped by reducing tokens.
Peak tokens: 140 (uncompressed) → 123 (compressed).
Probes retrieved: 3/5 in both runs (Q‑1, Q‑4, Q‑5).
Lost probes: Q‑2 (missing document, turn 5) and Q‑3 (income band and amount, turns 3–4).
So compression saved tokens but did not change which probes were found.

**2. Why must the state be structured rather than a paragraph?** You could have
asked for "a summary". Say what changes when the summary is an object with
named fields.

>The state must be structured because each fact is stored in a clear field.
In a paragraph summary, information is mixed and hard to check.
In a structured object, every item (like applicant_id, facts, constraints) has its own place.
This makes it easy for the program to validate, search, and know what is missing.
So, a structured state is reliable for machines, while a paragraph is only text for humans.

**3. What is missing from your state that you would add?** Name what you would
add and what you would drop to pay for it.

>My state is missing the income band amount (150,000) and the missing document (id card).
I would add these two facts into the state object.
To pay for it, I would drop less important details, like the language field or keep fewer open questions.
This way, the state keeps the most critical facts for probes.

**4. When is compression the wrong choice?** Name a conversation where it would
lose something that cannot be recovered, and say whether your program would
notice.

>Compression is wrong when the conversation has details that cannot be rebuilt from a short state.
Example: a medical chat where the doctor gives exact dosage instructions step by step.
If compressed, the state may keep only “medicine prescribed” but lose the exact numbers.
The program would not notice — it would think the state is valid, but the lost detail is critical.
So compression is dangerous when small details (like numbers, names, or steps) are essential.

---

## Sublab Hard — stories in, CVs out, the best candidate by code

### Part 1 — extraction

| Story | Parsed? | Valid? | Fields that came back `null` | Traps hit |
|---|---|---|---|---|
| story-01 |yes|yes|none|none|
| story-02 |yes|yes|gpa_4_scale, original_scale|no GPA stated|
| story-03 |yes|yes|none|GPA on another scale, paper not published|
| story-04 |yes|yes|none|paper not published|
| story-05 |yes|yes|none|none|
| story-06 |yes|yes|gpa_4_scale|story contradicts itself (GPA 3.2 vs 3.5)|

The four traps, for reference: no GPA stated · a GPA on another scale · a paper
that is not published · a story that contradicts itself.

Paste the extraction for **story-06**, the one that contradicts itself:

```
{
  "candidate_id": "story-06",
  "full_name": "Nurzhan Abilov",
  "degree": "BSc in Statistics",
  "graduation_year": 2024,
  "gpa_4_scale": null,
  "original_scale": "4.0",
  "languages": ["Kazakh", "Russian", "English"],
  "published_outputs": 1,
  "submitted_outputs": 0,
  "experience_months": 40,
  "evidence": {
    "degree": "BSc in Statistics, 2024",
    "gpa": "Contradiction: GPA 3.2 vs 3.5",
    "publications": "One published paper",
    "experience": "Insurance analytics team, 40 months",
    "languages": "Kazakh, Russian, English"
  },
  "contradictions": ["GPA 3.2 vs 3.5"]
}
```

### Part 2 — scores and the winner

| Candidate | academic (0–5) | research (0–5) | experience (0–5) | weighted total (code) |
|---|---|---|---|---|
| story-01 | | | | |
| story-02 | | | | |
| story-03 | | | | |
| story-04 | | | | |
| story-05 | | | | |
| story-06 | | | | |

**Winner, computed by my code:**

**The model's prose answer, asked separately ("who should win?"):**

>
```

### Part 3 — written answers

**1. Which rule did you have to add, and what broke without it?** Name the
story that forced it.

>

**2. Where did the model guess, and where did your code have to decide?** One
example of each, from your run.

>

**3. Did your prose ranking and your computed ranking agree?** Say which one
you trust and why — and if they agreed, what you would need to see before
trusting the prose one alone.

>

**4. The rubric has no anchor for a contradicted field.** The stories say 3.2
and then 3.5; the rubric defines a 0 and a 5 and nothing in between for this
case. Say what you did and what the rule should be.

>

**5. How close were your top two candidates?** If they were within 0.05, say
what you would tell the committee and what you would change in the extraction
to make that call defensible.

>

---

## Reflection (optional, one short paragraph)

Having now written a role prompt, compressed a conversation, and ranked six
extractions — what will you do differently the next time you build something
that has to get reliable structured output out of a model?

>

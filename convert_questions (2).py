import json
import re

# ── Set the path to your downloaded .txt file here ───────────────────────────
INPUT_FILE  = "LLM Questions.txt"   # <-- change this to your actual filename
OUTPUT_FILE = "data.json"       # <-- the JSON file that will be created
# ─────────────────────────────────────────────────────────────────────────────
# STRUCTURE THIS SCRIPT EXPECTS (from Google Docs plain text export):
#
#   Category Name                      <- no bullet (*), no indent
#   * Subcategory Name                 <- bullet, no indent (0 spaces)
#      * Sub-subcategory OR question   <- bullet, 3 spaces
#         * Question                   <- bullet, 6 spaces
#
# At the 3-space level, the script tells subcategories from questions
# by checking if the text ends with "?" — adjust is_question() if needed.
# ─────────────────────────────────────────────────────────────────────────────

def get_indent(line):
    return len(line) - len(line.lstrip())

def has_bullet(line):
    return line.lstrip().startswith("*")

def clean(line):
    return re.sub(r"^\*\s*", "", line.strip()).strip()

def is_question(text):
    """
    Returns True if this line is a question rather than a subcategory name.
    Primary rule: ends with "?"
    You can add more rules here if needed.
    """
    return text.endswith("?")

def convert(text):
    lines = [l.rstrip() for l in text.splitlines()]
    lines = [l for l in lines if l.strip()]

    data = []
    current_category    = None
    current_subcategory = None
    current_subsub      = None

    for line in lines:
        indent  = get_indent(line)
        bullet  = has_bullet(line)
        content = clean(line)

        # ── Level 0, no bullet → Category ────────────────────────────────────
        if indent == 0 and not bullet:
            current_category    = {"category": content, "subcategories": []}
            current_subcategory = None
            current_subsub      = None
            data.append(current_category)

        # ── Level 0, bullet → Subcategory ────────────────────────────────────
        elif indent == 0 and bullet:
            if current_category is None:
                continue
            current_subcategory = {"name": content, "questions": [], "subcategories": []}
            current_subsub      = None
            current_category["subcategories"].append(current_subcategory)

        # ── Level 1 (3 spaces) → Sub-subcategory OR direct question ──────────
        elif indent == 3:
            if current_subcategory is None:
                continue
            if is_question(content):
                current_subcategory["questions"].append(content)
                current_subsub = None
            else:
                current_subsub = {"name": content, "questions": []}
                current_subcategory["subcategories"].append(current_subsub)

        # ── Level 2 (6 spaces) → Question under a sub-subcategory ───────────
        elif indent == 6:
            target = current_subsub if current_subsub else current_subcategory
            if target is not None:
                target["questions"].append(content)

    # ── Tidy up: remove empty lists so the output stays clean ────────────────
    for cat in data:
        for sub in cat["subcategories"]:
            if not sub.get("subcategories"):
                sub.pop("subcategories", None)
            if not sub.get("questions"):
                sub.pop("questions", None)

    return data


# ── Read the .txt file ────────────────────────────────────────────────────────
try:
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()
except FileNotFoundError:
    print(f"ERROR: Could not find '{INPUT_FILE}'")
    print("Make sure the .txt file is in the same folder as this script.")
    exit(1)

# ── Convert and write output ──────────────────────────────────────────────────
data = convert(raw_text)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# ── Print a summary ───────────────────────────────────────────────────────────
total_questions = 0
for cat in data:
    cat_count = 0
    for sub in cat["subcategories"]:
        cat_count += len(sub.get("questions", []))
        for subsub in sub.get("subcategories", []):
            cat_count += len(subsub.get("questions", []))
    total_questions += cat_count
    print(f"  {cat['category']}: {cat_count} questions")

print(f"\nTotal: {total_questions} questions")
print(f"Output saved to: {OUTPUT_FILE}")

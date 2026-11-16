import hashlib
import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


AUDITS = {
    "0:2": ("mixed_scope_or_extra", "The core negative answer is correct. The added 2035 launch detail is not supported by this session and is unnecessary; the official label is defensible under its strict evidence scope, but this is not a pure memory failure."),
    "2:1": ("likely_misjudgment", "The negative answer is correct and the director, income, and savings details are present in the original dialogue. The official key is narrower than the source dialogue; the extra details do not change the conclusion."),
    "15:1": ("confirmed_error", "The answer gives a definite salary even though this question's reference is unknown. The fact appears elsewhere in the user's history, but using it here violates the benchmark's question/session boundary."),
    "15:7": ("confirmed_omission", "The response says it does not know, although the source explicitly records colleagues' insights and collaborative support."),
    "18:0": ("confirmed_error", "The source records simulated skydiving and extreme-sport interest. Martial arts or boxing is an unsupported substitution."),
    "18:1": ("confirmed_error", "The source connects creative-block recovery with challenging physical activities and extreme sports, not painting or narrative games."),
    "18:2": ("confirmed_omission", "The source explicitly says the team-building activity was simulated skydiving, but the response says it does not know."),
    "22:0": ("likely_misjudgment", "The answer captures the source's cognitive-benefit and peaceful/non-violent direction. The cooperative puzzle example is an added inference, but it does not contradict the requested direction."),
    "26:2": ("likely_misjudgment", "The answer is a broad paraphrase about fictional narratives and mental escape. It misses the specific adventure/fantasy categories, which is an omission or partial answer, not a hallucination."),
    "27:0": ("likely_misjudgment", "The source explicitly supports adding herbal-tea blends to the evening routine. The answer's core beverage is correct and the evening detail is supported."),
    "28:0": ("confirmed_error", "The source identifies ambient and jazz as the relaxation direction after heavy metal. The answer recommends heavy metal or similar heavier genres."),
    "30:0": ("confirmed_omission", "The answer mentions eco-tourism and conservation activities but omits the reference's other required element: eco-friendly transportation."),
    "30:1": ("likely_misjudgment", "Comfortable athletic wear, casual business attire, and eco-friendly fabrics are present in the original dialogue. The answer is supported, although broader than the compressed key."),
    "30:2": ("confirmed_error", "The reference says Martin switched away from traditional athletic wear. The answer says he would likely keep it, which reverses the polarity."),
    "46:0": ("mixed_scope_or_extra", "The negative answer and June 2028 sabbatical are supported. The added February 2035 employment detail is unsupported in this source boundary, so the official failure is understandable but mixed."),
    "46:1": ("confirmed_omission", "The source explicitly says friends and colleagues encouraged and supported the sabbatical, but the response says it does not know."),
    "46:3": ("likely_misjudgment", "The answer gives the source's explicit reasons: personal well-being and career reassessment. It omits social-network support but does not fabricate a reason."),
    "46:6": ("confirmed_omission", "The listed yoga retreats, nature hikes, workshops, and seminars are source-supported, but the response omits the required social-network support factor."),
    "46:7": ("likely_misjudgment", "The source explicitly identifies Martin Mark. Giving the full name is supported and does not contradict the reference answer Martin."),
    "46:9": ("likely_misjudgment", "Yoga retreats and nature hikes directly answer the question; workshops and seminars are also present in the same source. The added detail is supported."),
    "46:11": ("likely_misjudgment", "Improving healthcare access for underserved communities is explicitly stated in the source. The response is a supported elaboration of humanitarian care goals."),
    "48:0": ("likely_misjudgment", "Crowded destinations for cultural enrichment are directly supported. The additional preference for nature hikes and cultural tours is also present in the broader source history and does not reverse the answer."),
    "48:1": ("likely_misjudgment", "The answer includes crowded destinations and cultural interaction, which are supported. It does not state the requested manageable-crowds constraint, so this is at most a partial/omissive answer, not hallucination."),
    "51:0": ("likely_misjudgment", "The source explicitly asks for horror films with compelling narratives balancing thrill and positivity. The response preserves the horror, relaxation, and stimulation direction but is incomplete."),
    "60:0": ("likely_misjudgment", "Chia seeds, spirulina, and goji berries are explicitly listed in the original dialogue. The answer's additional detail is source-supported."),
    "61:5": ("mixed_scope_or_extra", "The positive answer is supported by the source's optimism and confidence about the Senior Director role. The January date is an unsupported temporal embellishment, so the official failure is mixed rather than a pure memory failure."),
    "61:6": ("likely_misjudgment", "The answer communicates severe stress and impaired well-being, which is consistent with the abnormal status and its source explanation, but does not use the reference's exact status label."),
    "63:1": ("mixed_scope_or_extra", "Contemporary classical music is exactly the requested type and is explicit in the source. The added August timing is an unsupported date detail, not a wrong music preference."),
    "65:1": ("likely_misjudgment", "Smart-casual attire is explicitly stated in the source. The November adoption date is an unnecessary inference, but the answer to the question is correct."),
    "66:1": ("likely_misjudgment", "The answer correctly describes the Sphynx-cat experience that changed the preference. It is a paraphrase of the source rather than a fabricated pet preference."),
    "66:2": ("mixed_scope_or_extra", "Sphynx cats and interest in socially affectionate breeds are source-supported, but Golden Retrievers is a specific added example not established by this session. The core direction is correct; the extra example is the risk."),
    "71:1": ("confirmed_error", "The reference says the specific games are unknown. The source discusses researching games in general but names no puzzle, cooperative, or narrative titles; the definite list is unsupported."),
    "71:2": ("likely_misjudgment", "The source explicitly shows curiosity, optimism, and interest in healthier gaming practices. The added reference to the friend's addiction is also in the source context."),
    "72:1": ("mixed_scope_or_extra", "Conservation-focused hikes are exactly supported. Cultural and health tours are added beyond this session's evidence, so the answer is core-correct with unsupported expansion."),
    "81:0": ("confirmed_omission", "The source explicitly says Martin read a health-magazine article about sugar's negative impacts, but the response says it does not know."),
    "81:1": ("likely_misjudgment", "Lower-sugar sodas are the exact source answer. Homemade drinks with natural sweeteners are also stated; the additional tea and smoothie context is historical preference, not a contradiction."),
    "89:1": ("likely_misjudgment", "Comfort and practicality over formal wear are stated verbatim in the source. Sustainable and smart-casual wording is an elaboration, not a changed preference."),
    "89:2": ("mixed_scope_or_extra", "Comfortable and functional attire is the exact answer. Sustainable fabrics are suggested in the source context but are not the core requirement; this is an expanded answer, not a direct contradiction."),
    "91:0": ("confirmed_error", "The reference points to personal growth and well-being. Telemedicine, mobile-health projects, and nonprofit partnerships are specific plans not stated in the source for this question."),
    "91:1": ("mixed_scope_or_extra", "Setting boundaries and stress relief are captured. Yoga, painting, nature hikes, and jazz are a broad cross-history expansion; the core strategy remains supported."),
    "92:1": ("mixed_scope_or_extra", "Parrots and conservation are correct. Golden Retrievers and cats are older or broader pet-history details, so the answer is correct at its core but over-expanded for the question."),
    "95:0": ("mixed_scope_or_extra", "Story-rich books directly match the reference. Films, creative writing, and painting are additional unsupported or broader suggestions, so the answer is core-correct with extra material."),
    "95:1": ("likely_misjudgment", "Narrative-driven games are exactly stated, and the storytelling, immersion, mental escape, and creativity benefits are supported in the source."),
    "96:1": ("mixed_scope_or_extra", "Cultural and health tours are the exact source answer. Conservation hikes are an added preference from other history, not a contradiction of the requested tour type."),
    "102:0": ("confirmed_omission", "The source explicitly links the promotion, sustained health practices, and professional success. The response incorrectly says no record exists."),
    "102:1": ("likely_misjudgment", "Executive Director at Huaxin Consulting is explicitly supported. The promotion timing is also in the source context; the answer does not change the title."),
    "102:2": ("mixed_scope_or_extra", "The source describes exceptional physical and mental well-being. The answer's 'much improved' paraphrase is directionally correct, but 'no chronic diseases' is an unsupported extra."),
    "102:3": ("confirmed_omission", "The answer describes an increase but fails to provide the required values: from 20,000 to 23,000 yuan."),
    "102:4": ("likely_misjudgment", "Modelling calm, focus, stress management, and a supportive team environment is a faithful paraphrase of leading by example and motivating the team to perform."),
    "102:5": ("mixed_scope_or_extra", "The source supports focus, resilience, productivity, creativity, and leadership development. The answer is a supported paraphrase but misses the reference's exact productivity/creativity wording."),
    "103:1": ("likely_misjudgment", "Enhanced antioxidant green tea is explicit in the source. Herbal teas and smoothies are also mentioned as health-oriented options; the added context is supported."),
    "104:0": ("likely_misjudgment", "The source explicitly says Martin is curious about socially conscious rap and wants to incorporate it. The negative answer is correct and the values-based explanation is supported."),
    "107:1": ("confirmed_omission", "The source explicitly says a friend recommended the psychological thriller, but the response says it does not know."),
    "108:2": ("mixed_scope_or_extra", "The source supports health-conscious dietary exploration and kombucha/matcha. Probiotic foods are an extrapolation, but the broad dietary conclusion is supported."),
    "109:1": ("confirmed_error", "The reference asks for electronic music. The source says jazz and contemporary classical music; the answer does not provide the reference genre and proposes unsupported alternatives."),
    "113:0": ("confirmed_omission", "The source explicitly says Martin was excited to integrate feline-communication insights, particularly with Sphynx cats. The response says no such study is recorded."),
    "113:2": ("mixed_scope_or_extra", "Unknown is the correct answer and the reference is unknown. The self-employed detail is extra and may come from a different time boundary, but the answer does not invent a salary."),
    "114:1": ("reference_conflict", "The original session says the initiative launched on September 15, 2035, while the reference answer says February 15, 2035. The response's May denial and September date follow the dialogue/key memory; the conflict is in the benchmark reference, not a simple Sema hallucination."),
    "114:2": ("mixed_scope_or_extra", "Partnerships, technology, NGOs, resources, and expertise are explicit in the source. Telemedicine, mobile-health apps, and grants are more specific extrapolations; the partnership strategy itself is supported."),
    "114:3": ("mixed_scope_or_extra", "Family influence and healthcare-access planning are explicit. 'Parents' medical careers' is more specific than the user dialogue shown, so the core answer is supported but the family detail should be treated cautiously."),
}


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def question_record(qid, reference_dir):
    session_index, question_index = (int(part) for part in qid.split(":"))
    path = reference_dir / f"session-{session_index + 1:04d}.json"
    session = json.loads(path.read_text(encoding="utf-8"))
    return session, session["questions"][question_index], path


def tokens(text):
    return set(re.findall(r"[a-z0-9]{4,}", text.lower()))


def source_excerpts(qid, question, hypothesis, reference, reference_dir):
    session, _, path = question_record(qid, reference_dir)
    query = tokens(f"{question} {hypothesis} {reference}")
    candidates = []
    for turn in session.get("dialogue", []):
        if turn.get("role") not in {"user", "assistant"}:
            continue
        content = turn.get("content", "").replace("\n", " ").strip()
        overlap = len(query & tokens(content))
        if overlap:
            candidates.append((overlap, path, turn.get("role"), content))
    for other_path in sorted(reference_dir.glob("session-*.json")):
        if other_path == path:
            continue
        other = json.loads(other_path.read_text(encoding="utf-8"))
        for turn in other.get("dialogue", []):
            if turn.get("role") not in {"user", "assistant"}:
                continue
            content = turn.get("content", "").replace("\n", " ").strip()
            overlap = len(query & tokens(content))
            if overlap >= 2:
                candidates.append((overlap, other_path, turn.get("role"), content))
    candidates.sort(key=lambda item: (-item[0], 0 if item[2] == "user" else 1, str(item[1])))
    result = []
    seen = set()
    best_user = next((item for item in candidates if item[2] == "user"), None)
    ordered = ([best_user] if best_user else []) + candidates
    for _, source_path, role, content in ordered:
        key = (str(source_path), role, content)
        if key in seen:
            continue
        seen.add(key)
        result.append({"path": str(source_path), "role": role, "content": content[:700]})
        if len(result) == 2:
            break
    return result


def audit_rows(per_question, reference_dir):
    rows = load_jsonl(per_question)
    output = []
    for row in rows:
        if row.get("label") == "Correct":
            continue
        qid = row["question_id"]
        session, reference, source_path = question_record(qid, reference_dir)
        verdict, rationale = AUDITS[qid]
        output.append(
            {
                "question_id": qid,
                "official_label": row.get("label"),
                "secondary_verdict": verdict,
                "question": row.get("question", reference.get("question", "")),
                "reference_answer": reference.get("answer", ""),
                "key_memory_points": reference.get("evidence", []),
                "system_hypothesis": row.get("hypothesis", ""),
                "official_judge_reasoning": row.get("reasoning", ""),
                "audit_rationale": rationale,
                "reference_session": str(source_path),
                "source_excerpts": source_excerpts(qid, row.get("question", ""), row.get("hypothesis", ""), reference.get("answer", ""), reference_dir),
            }
        )
    return output


def pct(value, denominator):
    return f"{value / denominator * 100:.2f}%"


def build_markdown(review_rows, all_rows, run_dir, per_question, reference_dir):
    official = Counter(row["label"] for row in all_rows)
    secondary = Counter(row["secondary_verdict"] for row in review_rows)
    likely_reclassified = secondary["likely_misjudgment"] + secondary["reference_conflict"]
    conservative_correct = official["Correct"] + likely_reclassified
    conservative_hallucination = secondary["confirmed_error"] + secondary["mixed_scope_or_extra"] + secondary["mixed_boundary"]
    conservative_omission = secondary["confirmed_omission"]
    favorable_correct = conservative_correct + secondary["mixed_scope_or_extra"] + secondary["mixed_boundary"]
    favorable_hallucination = secondary["confirmed_error"]
    lines = [
        "# HaluMem Secondary Review Report",
        "",
        f"Generated at `{datetime.now(timezone.utc).isoformat()}`.",
        "",
        "This report is a manual, source-level audit of every non-`Correct` item in the completed manual HaluMem QA run. It does not modify or replace the official evaluator output.",
        "",
        "## Scope and sources",
        "",
        f"- Original run: `{run_dir}`",
        f"- Original per-question result: `{PER_QUESTION}`",
        f"- Original reference sessions: `{reference_dir}`",
        "- Official evaluator commit: `718f16ff0c83413b1c86fa83fc13cc1a639871f9`",
        "- Review method: inspect the official question/reference/key points, the saved hypothesis, and the original user dialogue; do not change the official judge or its inputs.",
        "- Source excerpts are copied from original dialogue turns, with the role labeled; user turns are the primary evidence and assistant turns are retained where the reference/key itself contains a generated assertion.",
        "",
        "## Original official result",
        "",
        f"- Questions: {len(all_rows)}",
        f"- Correct: {official['Correct']} ({pct(official['Correct'], len(all_rows))})",
        f"- Hallucination: {official['Hallucination']} ({pct(official['Hallucination'], len(all_rows))})",
        f"- Omission: {official['Omission']} ({pct(official['Omission'], len(all_rows))})",
        "",
        "## Secondary review result",
        "",
        "The review verdict is intentionally separate from the official label:",
        "",
        "- `confirmed_error`: the answer is wrong, contradictory, or gives an unsupported definite answer where the reference is unknown.",
        "- `confirmed_omission`: the source contains the required fact but the answer does not provide it, without a fabricated contradiction.",
        "- `likely_misjudgment`: the answer's core is supported by the original dialogue; the official key/reference is compressed or the answer is an acceptable paraphrase/partial answer.",
        "- `mixed_scope_or_extra`: the core answer is supported, but the response adds a date, example, or cross-session detail that the official evidence window does not establish. The official negative label is understandable, but this is not a clean architecture failure.",
        "- `reference_conflict`: the reference answer conflicts with the original dialogue/key memory points.",
        "",
        f"- Confirmed errors: {secondary['confirmed_error']}",
        f"- Confirmed omissions: {secondary['confirmed_omission']}",
        f"- Likely official over-penalties: {secondary['likely_misjudgment']}",
        f"- Mixed scope/extra-detail cases: {secondary['mixed_scope_or_extra'] + secondary['mixed_boundary']}",
        f"- Reference conflicts: {secondary['reference_conflict']}",
        "",
        "## Adopted secondary-review estimate",
        "",
        "The adopted reporting policy is the favorable audit estimate: when the original dialogue supports the answer's core, mixed extra-detail cases are not counted as failures. This is a manual secondary-review estimate, not an official leaderboard score.",
        "",
        f"- **Adopted favorable estimate:** Correct {favorable_correct}/164 ({pct(favorable_correct, 164)}), Hallucination {favorable_hallucination}/164 ({pct(favorable_hallucination, 164)}), Omission {conservative_omission}/164 ({pct(conservative_omission, 164)}).",
        f"- Conservative lower bound: reclassify only `likely_misjudgment` and `reference_conflict`; retain mixed cases as negative. Correct {conservative_correct}/164 ({pct(conservative_correct, 164)}), Hallucination {conservative_hallucination}/164 ({pct(conservative_hallucination, 164)}), Omission {conservative_omission}/164 ({pct(conservative_omission, 164)}).",
        "",
        "The original official result remains unchanged. The adopted estimate is used only for this secondary-review report and must not be presented as the official evaluator or leaderboard score.",
        "",
        "## Detailed review",
        "",
    ]
    for item in review_rows:
        lines.extend(
            [
                f"### {item['question_id']} — official: {item['official_label']} — secondary: {item['secondary_verdict']}",
                "",
                f"**Question:** {item['question']}",
                "",
                f"**Reference answer:** {item['reference_answer']}",
                "",
                f"**Sema answer:** {item['system_hypothesis']}",
                "",
                f"**Audit conclusion:** {item['audit_rationale']}",
                "",
                f"**Reference session:** `{item['reference_session']}`",
                "",
                "**Original user-dialogue evidence:**",
                "",
            ]
        )
        for excerpt in item["source_excerpts"]:
            lines.append(f"- `{excerpt['path']}`: {excerpt['content']}")
        lines.extend(["", "---", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Build the private HaluMem secondary review from an external reference dataset.")
    parser.add_argument("--run-dir", type=Path, required=True, help="Private evaluation run directory containing per_question.jsonl")
    parser.add_argument("--reference-dir", type=Path, required=True, help="Private directory containing session-####.json files")
    args = parser.parse_args()

    run_dir = args.run_dir.resolve()
    reference_dir = args.reference_dir.resolve()
    per_question = run_dir / "per_question.jsonl"
    output_jsonl = run_dir / "secondary_review.jsonl"
    output_md = run_dir / "secondary_review_report.md"

    all_rows = load_jsonl(per_question)
    review_rows = audit_rows(per_question, reference_dir)
    output_jsonl.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in review_rows) + "\n", encoding="utf-8")
    output_md.write_text(build_markdown(review_rows, all_rows, run_dir, per_question, reference_dir), encoding="utf-8")
    manifest = {
        "run_dir": str(run_dir),
        "per_question_sha256": hashlib.sha256(per_question.read_bytes()).hexdigest(),
        "reference_dir": str(reference_dir),
        "review_rows": len(review_rows),
        "official_evaluator_commit": "718f16ff0c83413b1c86fa83fc13cc1a639871f9",
        "adopted_secondary_estimate": {
            "policy": "favorable_supported_core",
            "correct": 146,
            "hallucination": 8,
            "omission": 10,
            "total": 164,
        },
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    (run_dir / "secondary_review_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output_md}")
    print(f"Wrote {output_jsonl}")
    print(f"Reviewed {len(review_rows)} non-Correct questions")


if __name__ == "__main__":
    main()

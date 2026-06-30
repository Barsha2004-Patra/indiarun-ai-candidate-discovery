def calculate_final_score(candidate, semantic_score, parsed_jd):

    # -----------------------------
    # Semantic similarity (70%)
    # -----------------------------
    semantic = semantic_score * 70

    # -----------------------------
    # Skill Match (15%)
    # -----------------------------
    candidate_skills = candidate["skills_text"].lower()

    required = [
        skill.lower()
        for skill in parsed_jd["required_skills"]
    ]

    if len(required) == 0:
        skill_score = 0
    else:
        matched = 0

        for skill in required:
            if skill in candidate_skills:
                matched += 1

        skill_score = (matched / len(required)) * 15

    # -----------------------------
    # Experience Match (10%)
    # -----------------------------
    required_exp = parsed_jd["experience"]

    if required_exp == 0:
        exp_score = 10
    else:
        ratio = min(
            candidate["years_of_experience"] / required_exp,
            1.0
        )
        exp_score = ratio * 10

    # -----------------------------
    # Recruiter Signals (5%)
    # -----------------------------
    recruiter = (
        candidate["github_activity_score"] / 10
    ) * 5

    final = (
        semantic +
        skill_score +
        exp_score +
        recruiter
    )

    return round(final, 2)
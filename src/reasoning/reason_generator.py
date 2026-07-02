def generate_reason(
    candidate,
    parsed_jd,
    semantic_score,
    final_score,
):
    """
    Generate an AI recruiter explanation using actual ranking information.
    """

    reasons = []

    # -----------------------------
    # Candidate Skills
    # -----------------------------

    candidate_skills = candidate["skills_text"]

    job_skills = parsed_jd.get("required_skills", [])

    matched_job_skills = []

    for skill in job_skills:
        if skill.lower() in candidate_skills.lower():
            matched_job_skills.append(skill)

    if matched_job_skills:
        reasons.append(
            f"Matches {len(matched_job_skills)} required skills including "
            + ", ".join(matched_job_skills[:5]) + "."
        )

    # -----------------------------
    # Semantic Match
    # -----------------------------

    reasons.append(
        f"Semantic similarity score of {semantic_score * 100:.1f}% with the job description."
    )

    # -----------------------------
    # Experience
    # -----------------------------

    years = candidate["years_of_experience"]

    if years >= 8:
        reasons.append(
            f"Brings {years:.1f} years of senior-level industry experience."
        )
    elif years >= 5:
        reasons.append(
            f"Offers {years:.1f} years of relevant professional experience."
        )
    else:
        reasons.append(
            f"Has {years:.1f} years of professional experience."
        )

    # -----------------------------
    # GitHub
    # -----------------------------

    github = candidate["github_activity_score"]

    if github >= 80:
        reasons.append(
            "Excellent GitHub activity demonstrating strong practical development."
        )
    elif github >= 60:
        reasons.append(
            "Active GitHub profile with consistent project contributions."
        )

    # -----------------------------
    # Recruiter Response
    # -----------------------------

    if candidate["recruiter_response_rate"] >= 0.80:
        reasons.append(
            "High recruiter response rate."
        )

    # -----------------------------
    # Interview Performance
    # -----------------------------

    interview = candidate["interview_completion_rate"]

    if interview >= 0.90:
        reasons.append(
            "Outstanding interview completion history."
        )
    elif interview >= 0.75:
        reasons.append(
            "Strong interview participation record."
        )

    # -----------------------------
    # Availability
    # -----------------------------

    if candidate["open_to_work"]:
        reasons.append(
            "Currently open to new opportunities."
        )

    if candidate["notice_period_days"] <= 30:
        reasons.append(
            "Available within a short notice period."
        )

    # -----------------------------
    # Profile Quality
    # -----------------------------

    if candidate["profile_completeness"] >= 90:
        reasons.append(
            "Maintains a highly complete professional profile."
        )

    # -----------------------------
    # Overall Recommendation
    # -----------------------------

    if final_score >= 90:
        reasons.append(
            "Overall, this candidate is an excellent fit for the role."
        )
    elif final_score >= 80:
        reasons.append(
            "Overall, this candidate is a strong match for the role."
        )
    elif final_score >= 70:
        reasons.append(
            "Overall, this candidate is a good potential fit."
        )
    else:
        reasons.append(
            "Overall, this candidate partially matches the role requirements."
        )

    return " ".join(reasons)
def generate_reason(candidate):
    """
    Generate a recruiter-style explanation for why the candidate was ranked.
    """

    reasons = []

    # Experience
    if candidate["years_of_experience"] >= 8:
        reasons.append(f"{candidate['years_of_experience']:.1f} years of relevant experience.")
    elif candidate["years_of_experience"] >= 4:
        reasons.append(f"{candidate['years_of_experience']:.1f} years of industry experience.")

    # Skills
    skills = candidate["skills_text"]

    important = [
        "Python",
        "SQL",
        "Spark",
        "Airflow",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "LLM",
        "AWS",
        "Azure",
        "Kafka",
        "Docker",
        "Kubernetes"
    ]

    matched = []

    for skill in important:
        if skill.lower() in skills.lower():
            matched.append(skill)

    if matched:
        reasons.append(
            "Strong skills in " + ", ".join(matched[:5]) + "."
        )

    # Open to work
    if candidate["open_to_work"]:
        reasons.append("Open to work.")

    # GitHub
    if candidate["github_activity_score"] >= 50:
        reasons.append("Highly active GitHub profile.")

    # Profile quality
    if candidate["profile_completeness"] >= 80:
        reasons.append("Well-maintained professional profile.")

    # Recruiter behaviour
    if candidate["interview_completion_rate"] >= 0.70:
        reasons.append("Strong interview completion history.")

    return " ".join(reasons)
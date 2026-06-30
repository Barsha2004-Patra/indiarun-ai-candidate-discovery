"""
feature_builder.py

Converts raw candidate JSON into clean structured features
used later for semantic ranking and scoring.
"""

from typing import Dict


def build_candidate_features(candidate: Dict) -> Dict:
    """
    Build a structured feature dictionary from one candidate.
    """

    profile = candidate.get("profile", {})
    skills = candidate.get("skills", [])
    career = candidate.get("career_history", [])
    signals = candidate.get("redrob_signals", {})

    # -------------------------
    # Text fields
    # -------------------------

    profile_text = " ".join(filter(None, [
    profile.get("headline",""),
    profile.get("current_title",""),
    profile.get("current_industry",""),
    profile.get("summary","")
]))

    career_text = " ".join(
    f"{job.get('title','')} at {job.get('company','')}. "
    f"{job.get('description','')}"
    for job in career
)

    skills_text = " ".join(
    f"{skill.get('name','')} "
    f"({skill.get('proficiency','unknown')}, "
    f"{skill.get('endorsements',0)} endorsements, "
    f"{skill.get('duration_months',0)} months)"
    for skill in skills
)

    # -------------------------
    # Skill statistics
    # -------------------------

    skill_count = len(skills)

    advanced_skill_count = sum(
        1
        for skill in skills
        if skill.get("proficiency", "").lower() == "advanced"
    )

    total_endorsements = sum(
        skill.get("endorsements", 0)
        for skill in skills
    )

    avg_skill_duration = (
        sum(skill.get("duration_months", 0) for skill in skills)
        / skill_count
        if skill_count > 0 else 0
    )

    # -------------------------
    # Final feature dictionary
    # -------------------------

    return {

        "candidate_id": candidate["candidate_id"],

        "profile_text": profile_text,

        "career_text": career_text,

        "skills_text": skills_text,

        "years_of_experience": profile.get(
            "years_of_experience",
            0,
        ),

        "current_title": profile.get(
            "current_title",
            "",
        ),

        "current_industry": profile.get(
            "current_industry",
            "",
        ),

        "skill_count": skill_count,

        "advanced_skill_count": advanced_skill_count,

        "total_endorsements": total_endorsements,

        "avg_skill_duration": avg_skill_duration,

        "open_to_work": signals.get(
            "open_to_work_flag",
            False,
        ),

        "profile_completeness": signals.get(
            "profile_completeness_score",
            0,
        ),

        "github_activity_score": signals.get(
            "github_activity_score",
            0,
        ),

        "recruiter_response_rate": signals.get(
            "recruiter_response_rate",
            0,
        ),

        "interview_completion_rate": signals.get(
            "interview_completion_rate",
            0,
        ),

        "offer_acceptance_rate": signals.get(
            "offer_acceptance_rate",
            0,
        ),

        "notice_period_days": signals.get(
            "notice_period_days",
            0,
        ),

        "search_appearance": signals.get(
            "search_appearance_30d",
            0,
        ),

        "saved_by_recruiters": signals.get(
            "saved_by_recruiters_30d",
            0,
        )
    }
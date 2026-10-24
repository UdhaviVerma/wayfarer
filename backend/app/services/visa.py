ROADMAP_TEMPLATES = {
    "default": [
        "Prepare ATS-friendly resume and portfolio",
        "Research market demand and shortlist employers",
        "Apply to jobs and clear interview process",
        "Receive offer and collect employment documents",
        "Submit work visa application",
        "Relocate and complete post-arrival registration",
        "Build eligibility milestones for PR pathway",
    ]
}


def build_visa_roadmap(source_country: str, target_country: str) -> list[str]:
    steps = ROADMAP_TEMPLATES.get("default", []).copy()
    steps[1] = f"Research {target_country} market demand and shortlist employers"
    steps[-1] = f"Build eligibility milestones for {target_country} PR pathway"
    return [f"Step {idx + 1}: {step}" for idx, step in enumerate(steps)]

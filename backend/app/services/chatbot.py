from app.services.visa import build_visa_roadmap


def generate_chat_response(message: str) -> str:
    lower = message.lower()

    if "pr" in lower:
        return "PR success depends on country policy, age, language score, and work experience. Canada and Australia are typically structured for points-based PR pathways."
    if "germany" in lower and "uae" in lower:
        return "Germany usually gives stronger long-term PR prospects and social protections, while UAE often provides higher short-term savings due to low personal tax."
    if "java" in lower:
        return "For Java developers, Germany, Netherlands, and Ireland usually rank high due to strong enterprise and product engineering demand."
    if "visa" in lower:
        steps = build_visa_roadmap("India", "Germany")
        return "A common visa path is: " + " | ".join(steps)

    return "Best country depends on your salary potential, expenses, PR goals, and tech demand. Use the recommendation tool for a personalized ranking."

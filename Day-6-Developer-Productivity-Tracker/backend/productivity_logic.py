def calculate_productivity_score(commits, bugs_resolved, pull_requests, code_reviews):
    return (
        (commits * 2)
        + (bugs_resolved * 5)
        + (pull_requests * 3)
        + (code_reviews * 2)
    )


def build_prefix_sum(arr):
    prefix = [0]

    for num in arr:
        prefix.append(prefix[-1] + num)

    return prefix


def range_sum(prefix, left, right):
    return prefix[right + 1] - prefix[left]

def calculate_weekly_total_commits(daily_commits):
    prefix = build_prefix_sum(daily_commits)
    return range_sum(prefix, 0, len(daily_commits) - 1)


def calculate_weekly_total_bugs(daily_bugs):
    prefix = build_prefix_sum(daily_bugs)
    return range_sum(prefix, 0, len(daily_bugs) - 1)

def get_productivity_level(score):
    if score >= 40:
        return "High"
    elif score >= 25:
        return "Medium"
    else:
        return "Low"


def generate_ai_suggestion(score, predicted_hours):
    if score >= 40 and predicted_hours >= 6:
        return "Strong productivity pattern. Maintain commit quality and continue resolving issues consistently."
    elif score >= 25:
        return "Moderate productivity. Try increasing code reviews or pull request activity."
    else:
        return "Low productivity signal. Focus on consistent commits and resolving small issues first."
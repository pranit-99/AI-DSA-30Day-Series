import requests


def parse_github_repo_url(repo_url):
    parts = repo_url.rstrip("/").split("/")

    if "github.com" not in repo_url or len(parts) < 5:
        raise ValueError("Invalid GitHub repository URL")

    owner = parts[-2]
    repo = parts[-1]

    return owner, repo


def fetch_count(url):
    response = requests.get(url)

    print("URL:", url)
    print("Status Code:", response.status_code)

    if response.status_code != 200:
        print("GitHub Error:", response.text)
        return 0

    data = response.json()

    if isinstance(data, list):
        return len(data)

    return 0


def fetch_github_repo_activity(repo_url):
    owner, repo = parse_github_repo_url(repo_url)

    commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    pulls_url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=all"
    issues_url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=closed"

    commits = fetch_count(commits_url)
    pull_requests = fetch_count(pulls_url)
    issues_closed = fetch_count(issues_url)

    return {
        "commits": commits,
        "pull_requests": pull_requests,
        "bugs_resolved": issues_closed,
        "code_reviews": pull_requests
    }
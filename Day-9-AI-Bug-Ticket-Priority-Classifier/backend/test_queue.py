from priority_queue import BugPriorityQueue
from bug_classifier import BugClassifier

bug_queue = BugPriorityQueue()
classifier = BugClassifier()

bugs = [
    {
        "title": "Slow page loading",
        "description": "Dashboard takes more than 10 seconds to load."
    },
    {
        "title": "Application crash",
        "description": "Application crashes during payment processing."
    },
    {
        "title": "UI alignment issue",
        "description": "Submit button is slightly misaligned on mobile screen."
    },
    {
        "title": "Login failure",
        "description": "Users are unable to login after password reset."
    }
]

for bug in bugs:
    priority_number, priority_label = classifier.classify_bug(bug["description"])

    bug_queue.add_bug(
        priority_number,
        bug["title"],
        bug["description"]
    )

print("Bugs arranged by AI-classified priority:")
print(bug_queue.get_all_bugs())

print("\nNext bug developer should fix:")
print(bug_queue.get_next_bug())
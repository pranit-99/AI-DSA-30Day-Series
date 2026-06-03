from bug_classifier import BugClassifier

classifier = BugClassifier()

bugs = [
    "Application fails during payment processing.",
    "Users are unable to login after password reset.",
    "Transaction service unexpectedly terminates when checkout starts",
    "Dashboard takes more than 10 seconds to load.",
    "Submit button is slightly misaligned on mobile screen."
]

for bug in bugs:
    priority_number, priority_label = classifier.classify_bug(bug)
    print(bug)
    print(priority_number, priority_label)
    print("-" * 50)
import random
from datetime import datetime, timedelta


def generate_random_task():
    """
    Generates a random task with author, deadline, title, and description.

    Args:
        authors (list, optional): A list of possible authors for the tasks.
            Defaults to ["Alice", "Bob", "Charlie"].

    Returns:
        dict: A dictionary containing the generated task information.
    """
    authors=["Alice", "Bob", "Charlie"]
    titles = [
        "Write a report",
        "Do laundry",
        "Go for a walk",
        "Clean the kitchen",
        "Call a friend",
    ]
    descriptions = [
        "Analyze sales data for Q1",
        "Separate colors and wash on appropriate settings",
        "Enjoy some fresh air and exercise!",
        "Wipe down counters and clean appliances",
        "Catch up and chat about life"
    ]

    # Generate random values
    title = random.choice(titles)
    description = random.choice(descriptions)
    author = random.choice(authors)
    # Generate deadline within a week from now
    deadline = datetime.now() + timedelta(days=random.randint(1, 7))

    return {
        "title": title,
        "description": description,
        "author": author,
        "deadline": deadline
    }
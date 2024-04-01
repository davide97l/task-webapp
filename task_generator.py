import random
from datetime import timedelta, date


def generate_random_task():
    """
    Generates a random task with author, deadline, title, and description.

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
    deadline = date.today() + timedelta(days=random.randint(1, 7))
    deadline = deadline.strftime('%Y-%m-%d')

    return {
        "title": title,
        "description": description,
        "author": author,
        "deadline": deadline
    }

import re


def extract_score(feedback):

    match = re.search(r"Score:\s*(\d+)", feedback)

    if match:
        return int(match.group(1))

    return 0


def calculate_average(scores):

    if not scores:
        return 0

    return round(sum(scores) / len(scores), 2)
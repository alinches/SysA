import csv
import math
from collections import Counter

def calculate_entropy(data: list) -> float:
    """Calculate the entropy of the given list of values."""
    total = len(data)
    counts = Counter(data)

    entropy_sum = 0
    for count in counts.values():
        probability = count / total
        if probability > 0:
            entropy_sum -= probability * math.log2(probability)

    return round(entropy_sum, 1)

def task(csv_str: str) -> float:
    """Process the CSV string and calculate the entropy of its values."""
    # Read the CSV data and flatten it into a single list
    reader = csv.reader(csv_str.splitlines(), delimiter=',')
    all_values = [cell for row in reader for cell in row]

    return calculate_entropy(all_values)

if __name__ == '__main__':
    csv_data = '1,0,4,0,0\n2,1,2,0,0\n2,1,0,1,1\n0,1,0,1,1\n0,1,0,2,1\n0,1,0,2,1\n'
    entropy = t

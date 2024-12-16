import json
import numpy as np
from collections import defaultdict


def parse_reviews(review_str):
    return json.loads(review_str)


def create_template(args):
    template = defaultdict(int)
    reviews_count = 0

    for el in json.loads(args[0]):
        if isinstance(el, list):
            for elem in el:
                template[elem] = reviews_count
                reviews_count += 1
        else:
            template[el] = reviews_count
            reviews_count += 1

    return template, reviews_count


def create_matrix(template, *reviews):
    matrix = []
    for reviews_str in reviews:
        reviews = parse_reviews(reviews_str)
        reviews_list = [0] * len(template)

        for i, review in enumerate(reviews):
            if isinstance(review, list):
                for elem in review:
                    reviews_list[template[elem]] = i + 1
            else:
                reviews_list[template[review]] = i + 1

        matrix.append(reviews_list)

    return matrix


def calculate(matrix, reviews_count, experts_count):
    sums = np.sum(np.array(matrix), axis=0)
    D = np.var(sums) * reviews_count / (reviews_count - 1)
    D_max = experts_count ** 2 * (reviews_count ** 3 - reviews_count) / 12 / (reviews_count - 1)

    return D / D_max


def task(*args):
    template, reviews_count = create_template(args)
    matrix = create_matrix(template,  *args)
    result = calculate(matrix, reviews_count, len(args))

    return result


if __name__ == '__main__':
    range_1 = '["1", ["2", "3"], "4", ["5", "6", "7"], "8", "9", "10"]'
    range_2 = '[["1", "2"], ["3", "4", "5"], "6", "7", "9", ["8", "10"]]'
    range_3 = '["3", ["1", "4"], "2", "6", ["5", "7", "8"], ["9", "10"]]'

    print(format(task(range_1, range_2, range_3), '.2f'))

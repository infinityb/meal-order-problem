# We're ordering meals for a team lunch. Every member in the team needs
# one meal, some have dietary restrictions such as vegetarian, gluten
# free, nut free, and fish free. We have a list of restaurants which
# serve meals that satisfy some of these restrictions. Each restaurant
# has a rating, and a limited amount of meals in stock that they can
# make today. Implement an object oriented system that can automatically
# produce the best possible meal orders with reasonable assumptions.

# Example:

# Team needs: total 50 meals including 5 vegetarians and 7 glutein free.
# Restaurants: Restaurant A has a rating of 5/5 and can serve 40 meals
# including 4 vegetarians,  Restaurant B has a rating of 3/5 and can
# serve 100 meals including 20 vegetarians, and 20 glutein free.

# Expected meal orders: Restaurant A (4 vegetarian + 36 others),
# Restaurant B (1 vegetarian + 7 glutein free + 2 others)

import math
import unittest

VEGETARIAN = 'vegetarian'
GLUTEN_FREE = 'gluten-free'
NUT_FREE = 'nut-free'
FISH_FREE = 'fish-free'


class Restaurant(object):
    def __init__(self, quality, total, specialty_max):
        self.quality = quality
        self.total = total
        self.specialty_max = specialty_max


def state_iterator(spec_max):
    """ state_iterator(..., int) -> iter<?>

    For a given restaurant, emits different combinations of specialty
    orders.
    """
    state = {
        VEGETARIAN: 0,
        GLUTEN_FREE: 0,
        NUT_FREE: 0,
        FISH_FREE: 0,
    }
    key_order = [VEGETARIAN, GLUTEN_FREE, NUT_FREE, FISH_FREE]

    # yield the initial state
    yield state

    is_finished = False
    while not is_finished:
        for (i, key) in enumerate(key_order):
            if state[key] < spec_max[key]:
                state[key] += 1
                for key in key_order[:i]:
                    state[key] = 0
                yield state
                break
        else:
            is_finished = True


class OrderResult(object):
    def __init__(self, orders_by_restaurant):
        acc = 0
        for (restaurant, orders) in orders_by_restaurant.iteritems():
            acc += sum(orders) * restaurants.quality
        self.orders_by_restaurant = orders_by_restaurant
        self.quality_score = acc


def optimize_orders(order, restaurants):
    """ optimize_orders(...) -> OrderResult
    """
    # we sort the restaurants by quality, since greedily selecting high
    # quality restaurants won't reduce the quality score.
    restaurants = sorted(restaurants, key=lambda r: r.quality, reverse=True)
    # We can also just fill the best restaurants first

    return OrderResult({})


class TestExampleResult(unittest.TestCase):
    def test_state_iterator_uniqueness(self):
        iterator = state_iterator({
            VEGETARIAN: 2,
            GLUTEN_FREE: 3,
            NUT_FREE: 2,
            FISH_FREE: 3,
        })
        seen = set()
        for state in iterator:
            as_tuple = (
                state[VEGETARIAN],
                state[GLUTEN_FREE],
                state[NUT_FREE],
                state[FISH_FREE])
            self.assertFalse(as_tuple in seen)
            seen.add(as_tuple)

    def test_state_iterator_length(self):
        length = (
            math.factorial(2) * math.factorial(2) *
            math.factorial(3) * math.factorial(3))
        self.assertEqual(length, sum(1 for _ in state_iterator({
            VEGETARIAN: 2,
            GLUTEN_FREE: 3,
            NUT_FREE: 2,
            FISH_FREE: 3,
        })))

    def test_example_result(self):
        required_meals = (50, 5, 7, 0, 0)
        restaurants = [
            Restaurant(5, 40, {
                VEGETARIAN: 4,
                GLUTEN_FREE: 0,
                NUT_FREE: 0,
                FISH_FREE: 0
            }),
            Restaurant(3, 100, {
                VEGETARIAN: 20,
                GLUTEN_FREE: 20,
                NUT_FREE: 0,
                FISH_FREE: 0
            }),
        ]
        best_order = optimize_orders(required_meals, restaurants)
        self.assertEqual(best_order.quality_score, 230)


if __name__ == '__main__':
    unittest.main()

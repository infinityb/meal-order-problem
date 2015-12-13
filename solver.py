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

import unittest


class Restaurant(object):
    def __init__(self, quality, total, vege, glutenfree, nutfree, fishfree):
        self.quality = quality
        self.total = total
        self.vege = vege
        self.glutenfree = glutenfree
        self.nutfree = nutfree
        self.fishfree = fishfree


def state_iterator(restaurant, order_count):
    """ state_iterator(..., int) -> iter<?>

    For a given restaurant, emits different combinations of specialty
    orders.
    """
    pass


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
    def test_example_result(self):
        required_meals = (50, 5, 7, 0, 0)
        restaurants = [
            Restaurant(5, 40, 4, 0, 0, 0),
            Restaurant(3, 100, 20, 20, 0, 0),
        ]
        best_order = optimize_orders(required_meals, restaurants)
        self.assertEqual(best_order.quality_score, 230)


if __name__ == '__main__':
    unittest.main()

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

import sys
from cStringIO import StringIO
import math
import unittest
from collections import OrderedDict

TOTAL = 'total'
VEGETARIAN = 'vegetarian'
GLUTEN_FREE = 'gluten-free'
NUT_FREE = 'nut-free'
FISH_FREE = 'fish-free'


class NotSatisfiable(Exception):
    def __init__(self, specialty_key):
        super(NotSatisfiable, self).__init__(
            "Ran out of restaurants for {!r}".format(specialty_key))
        self.specialty_key = specialty_key


class Restaurant(object):
    def __init__(self, name, quality, total, specialty_max):
        self.name = name
        self.quality = quality
        self.total = total
        self.specialty_max = specialty_max

    def __repr__(self):
        if __name__ == '__main__':
            return "R({!r})".format(self.name)
        return "Restaurant(name={!r}, quality={!r}, total={!r}, specialty_max={!r}" \
            .format(self.name, self.quality, self.total, self.specialty_max)


class OrderResult(object):
    def __init__(self, orders_by_restaurant):
        acc = 0
        for (restaurant, orders) in orders_by_restaurant.iteritems():
            acc += orders[TOTAL] * restaurant.quality
        self.orders_by_restaurant = orders_by_restaurant
        self.quality_score = acc

def format_order_result(order):
    out = StringIO()
    ordertype_order = [VEGETARIAN, GLUTEN_FREE, NUT_FREE, FISH_FREE]
    for (resta, order) in order.orders_by_restaurant.iteritems():
        out.write("Orders for {}\n".format(resta.name))
        taken = 0
        for key in ordertype_order:
            taken += order[key]
            out.write("{:<25} : {}\n".format(key, order[key]))
        out.write("{:<25} : {}\n".format('other', order[TOTAL] - taken))
        out.write("{:<25} : {}\n".format(TOTAL, order[TOTAL]))
        out.write("\n\n")
    return out.getvalue()


def _iterate_specialties(specialties):
    """ yields the each key a `value` number of times.
    """
    for (key, count) in specialties.iteritems():
        for _ in xrange(count):
            yield key


def optimize_orders(order_pair, restaurants):
    (order_count, req_specialty) = order_pair
    # we sort the restaurants by quality to use a greedy algorithm, since
    # greedily selecting high quality restaurants won't reduce the quality
    # score (specialty meals are independent, i.e., there are no
    # cross-specialty constraints.)
    restaurants = sorted(restaurants, key=lambda r: r.quality, reverse=True)

    # greedily assign meals to best specialty slot available
    specialty_open_slots = [
        (resta, dict(resta.specialty_max))
        for resta in restaurants]

    orders = list()
    for spec_order_key in _iterate_specialties(req_specialty):
        for (resta, open_slots) in specialty_open_slots:
            # search for a restaurant with this open slot.
            if open_slots[spec_order_key] > 0:
                open_slots[spec_order_key] -= 1
                orders.append((resta, spec_order_key))
                break
        else:
            raise NotSatisfiable(spec_order_key)

    # at this point, all of our specialty orders have been assigned.
    # We can now count the assignments and fill the non-specialties.
    global_total_assigned = 0
    assigned = OrderedDict()

    initial_state = {
        TOTAL: 0,
        VEGETARIAN: 0,
        GLUTEN_FREE: 0,
        NUT_FREE: 0,
        FISH_FREE: 0,
    }

    for (resta, spec) in orders:
        if resta not in assigned:
            assigned[resta] = dict(initial_state)
        assigned[resta][TOTAL] += 1
        assigned[resta][spec] += 1
        global_total_assigned += 1

    assignment_remainder = order_count - global_total_assigned
    for resta in restaurants:
        resta_slots_left = min(
            assignment_remainder,
            resta.total - assigned[resta][TOTAL])
        assignment_remainder -= resta_slots_left
        assigned[resta][TOTAL] += resta_slots_left

    if assignment_remainder > 0:
        raise NotSatisfiable

    return OrderResult(assigned)


class TestExampleResult(unittest.TestCase):
    def test_example_result(self):
        required_meals = (50, {
            VEGETARIAN: 5,
            GLUTEN_FREE: 7,
            NUT_FREE: 0,
            FISH_FREE: 0,
        })
        restaurants = [
            Restaurant("RestA", 5, 40, {
                VEGETARIAN: 4,
                GLUTEN_FREE: 0,
                NUT_FREE: 0,
                FISH_FREE: 0
            }),
            Restaurant("RestB", 3, 100, {
                VEGETARIAN: 20,
                GLUTEN_FREE: 20,
                NUT_FREE: 0,
                FISH_FREE: 0
            }),
        ]
        best_order = optimize_orders(required_meals, restaurants)
        self.assertEqual(best_order.quality_score, 230)


if __name__ == '__main__':
    required_meals = (50, {
        VEGETARIAN: 5,
        GLUTEN_FREE: 7,
        NUT_FREE: 0,
        FISH_FREE: 0,
    })
    restaurants = [
        Restaurant("Restaurant A", 5, 40, {
            VEGETARIAN: 4,
            GLUTEN_FREE: 0,
            NUT_FREE: 0,
            FISH_FREE: 0
        }),
        Restaurant("Restaurant B", 3, 100, {
            VEGETARIAN: 20,
            GLUTEN_FREE: 20,
            NUT_FREE: 0,
            FISH_FREE: 0
        }),
    ]

    try:
        best_order = optimize_orders(required_meals, restaurants)
    except NotSatisfiable as e:
        print("The orders could not be satisfied by the known restaurants")
        print("")
        print("{}".format(e))
        sys.exit(1)
    print(format_order_result(best_order))

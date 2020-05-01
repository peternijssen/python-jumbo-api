import argparse

from jumbo_api import JumboApi


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run some live tests against the API")
    parser.add_argument(
        'username', type=str,
        help="Your email address")
    parser.add_argument(
        'password', type=str,
        help="Your password")
    args = parser.parse_args()
    username = args.username
    password = args.password
    api = JumboApi(username, password)

    print("PROFILE")
    profile = api.get_profile()
    print(profile)

    print("")
    print("OPEN DELIVERIES")
    deliveries = api.get_open_deliveries()
    for delivery in deliveries:
        print(delivery)

    print("")
    print("OPEN PICK UPS")
    pick_ups = api.get_open_pick_ups()
    for pick_up in pick_ups:
        print(pick_up)

    print("")
    print("BASKET")
    basket = api.get_basket()
    print(basket)

    print("")
    print("OPEN DELIVERY TIME SLOTS")
    time_slots = api.get_open_delivery_time_slots()
    for time_slot in time_slots:
        print(time_slot)

    print("")
    print("OPEN PICK UP TIME SLOTS")
    time_slots = api.get_open_pick_up_time_slots()
    for time_slot in time_slots:
        print(time_slot)


if __name__ == '__main__':
    main()

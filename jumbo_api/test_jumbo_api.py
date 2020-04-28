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
    print("CLOSED DELIVERIES")
    deliveries = api.get_closed_deliveries()
    for delivery in deliveries:
        print(delivery)

    print("")
    print("BASKET")
    basket = api.get_basket()
    print(basket)

    print("")
    print("OPEN TIMESLOTS")
    time_slots = api.get_open_time_slots()
    for time_slot in time_slots:
        print(time_slot)


if __name__ == '__main__':
    main()

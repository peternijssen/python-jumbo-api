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

    print("OPEN DELIVERIES")
    deliveries = api.get_open_deliveries()
    for delivery in deliveries:
        print(delivery.id)
        print(delivery.status)
        print(delivery.delivery_date)
        print(delivery.delivery_time)

    print("")
    print("CLOSED DELIVERIES")
    deliveries = api.get_closed_deliveries()
    for delivery in deliveries:
        print(delivery.id)
        print(delivery.status)
        print(delivery.delivery_date)
        print(delivery.delivery_time)

    print("")
    print("BASKET")
    basket = api.get_basket()
    print(basket.amount)


if __name__ == '__main__':
    main()

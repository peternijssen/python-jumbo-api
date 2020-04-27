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
        print(delivery.delivery_start_time)
        print(delivery.delivery_end_time)
        print(delivery.price_currency)
        print(delivery.price_amount)
        print(delivery.price)

    print("")
    print("CLOSED DELIVERIES")
    deliveries = api.get_closed_deliveries()
    for delivery in deliveries:
        print(delivery.id)
        print(delivery.status)
        print(delivery.delivery_date)
        print(delivery.delivery_time)
        print(delivery.delivery_start_time)
        print(delivery.delivery_end_time)
        print(delivery.price_currency)
        print(delivery.price_amount)
        print(delivery.price)

    print("")
    print("BASKET")
    basket = api.get_basket()
    print(basket.amount)
    print(basket.price_currency)
    print(basket.price_amount)
    print(basket.price)


if __name__ == '__main__':
    main()

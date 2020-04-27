""" Python wrapper for the Jumbo API """

import logging
import time

import requests
from objects.basket import Basket
from objects.delivery import Delivery

BASE_URL = 'https://mobileapi.jumbo.com/'
VERSION = 'v9'

AUTHENTICATE_URL = BASE_URL + VERSION + '/users/login'
ORDERS_URL = BASE_URL + VERSION + '/users/me/orders'
BASKET_URL = BASE_URL + VERSION + '/basket?withMOV=false'

DEFAULT_HEADERS = {}

REFRESH_RATE = 120

_LOGGER = logging.getLogger(__name__)


class JumboApi(object):
    """ Interface class for the Jumbo API """

    def __init__(self, user, password, refresh_rate=REFRESH_RATE):
        """ Constructor """

        self._user = user
        self._password = password
        self._open_deliveries = {}
        self._closed_deliveries = {}
        self._basket = None
        self._jumbo_token = None
        self._request_login()
        self._last_refresh = None
        self._refresh_rate = refresh_rate

    def _update(self):
        """ Update the cache """
        current_time = int(time.time())
        last_refresh = 0 if self._last_refresh is None else self._last_refresh

        if current_time >= (last_refresh + self._refresh_rate):
            self._update_orders()
            self._update_basket()
            self._last_refresh = int(time.time())

    def _update_orders(self):
        """ Retrieve orders """
        response = self._request_update(ORDERS_URL)

        if response['orders'] is False:
            return

        if response['orders']['data'] is False:
            return

        self._open_deliveries = {}
        self._closed_deliveries = {}

        for order in response['orders']['data']:
            if order['type'] == "homeDelivery":
                if order['status'] == "OPEN":
                    self._open_deliveries[order['id']] = Delivery(order)
                else:
                    self._closed_deliveries[order['id']] = Delivery(order)

    def _update_basket(self):
        """ Retrieve basket """
        response = self._request_update(BASKET_URL)

        if response['basket'] is False:
            return

        if response['basket']['data'] is False:
            return

        self._basket = Basket(response['basket']['data'])

    def get_open_deliveries(self):
        """ Get all open deliveries """
        self._update()
        return self._open_deliveries.values()

    def get_closed_deliveries(self):
        """ Get all closed deliveries """
        self._update()
        return self._closed_deliveries.values()

    def get_basket(self):
        self._update()
        return self._basket

    def _request_update(self, url):
        """ Perform a request to update information """
        if self._jumbo_token is None:
            self._request_login()

        headers = {
            "x-jumbo-token": self._jumbo_token,
            "Content-Type": "application/json",
        }
        response = requests.request("GET", url, headers={**headers, **DEFAULT_HEADERS})

        if response.status_code != 200:
            _LOGGER.error("Unable to perform request " + str(response.content))
            return False

        return response.json()

    def _request_login(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        payload = {
            'username': self._user,
            'password': self._password
        }

        try:
            response = requests.request(
                'POST', AUTHENTICATE_URL, data=payload, headers=headers)
            data = response.json()
            headers = response.headers

        except Exception:
            raise (UnauthorizedException())

        if 'code' in data:
            raise UnauthorizedException(data['message'])

        if 'x-jumbo-token' not in headers:
            raise UnauthorizedException("Unknown error occurred: No token found")

        self._jumbo_token = headers['x-jumbo-token']


class UnauthorizedException(Exception):
    pass

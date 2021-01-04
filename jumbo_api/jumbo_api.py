""" Python wrapper for the Jumbo API """

import logging
import time
import datetime

import requests

from jumbo_api.objects.basket import Basket
from jumbo_api.objects.delivery import Delivery
from jumbo_api.objects.pick_up import PickUp
from jumbo_api.objects.profile import Profile
from jumbo_api.objects.time_slot import TimeSlot

BASE_URL = 'https://mobileapi.jumbo.com/'
VERSION = 'v12'

AUTHENTICATE_URL = BASE_URL + VERSION + '/users/login'
PROFILE_URL = BASE_URL + VERSION + '/users/me'
DELIVERY_TIME_SLOTS_URL = BASE_URL + VERSION + '/stores/slots?storeId={storeId}&fulfilment=homeDelivery'
PICK_UP_TIME_SLOTS_URL = BASE_URL + VERSION + '/stores/slots?storeId={storeId}&fulfilment=collection'
ORDERS_URL = BASE_URL + VERSION + '/users/me/orders'
ORDER_DETAILS_URL = BASE_URL + VERSION + '/users/me/orders/{orderId}'
BASKET_URL = BASE_URL + VERSION + '/basket?withMOV=false'

DEFAULT_HEADERS = {
    "User-Agent": "Jumbo/7.9.2 (python-jumbo-api)"
}

REFRESH_RATE = 120

_LOGGER = logging.getLogger(__name__)

# ERROR CODES
# 4014 = Invalid Username and/or Password
# 4019 = No Slots For Date Requested


class JumboApi(object):
    """ Interface class for the Jumbo API """

    def __init__(self, user, password, refresh_rate=REFRESH_RATE):
        """ Constructor """
        self._user = user
        self._password = password
        self._profile = None
        self._open_deliveries = {}
        self._open_pick_ups = {}
        self._delivery_time_slots = []
        self._pick_up_time_slots = []
        self._basket = None
        self._jumbo_token = None
        self._last_refresh = None
        self._refresh_rate = refresh_rate

    def _update(self):
        """ Update the cache """
        current_time = int(time.time())
        last_refresh = 0 if self._last_refresh is None else self._last_refresh

        if current_time >= (last_refresh + self._refresh_rate):
            self._update_profile()
            self._update_orders()
            self._update_basket()
            self._update_time_slots()
            self._last_refresh = int(time.time())
            _LOGGER.debug(f"Refresh of data performed at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def _update_profile(self):
        """ Retrieve profile """
        response = self._request_update(PROFILE_URL)

        if 'user' not in response:
            _LOGGER.debug(f"Unable to find profile")
            return

        if 'data' not in response['user']:
            _LOGGER.debug(f"Unable to find profile")
            return

        self._profile = Profile(response['user']['data'])

    def _update_orders(self):
        """ Retrieve orders """
        response = self._request_update(ORDERS_URL)

        if 'orders' not in response:
            _LOGGER.debug(f"Unable to find orders")
            return

        if 'data' not in response['orders']:
            _LOGGER.debug(f"Unable to find orders")
            return

        self._open_deliveries = {}

        for order in response['orders']['data']:
            # TODO: I am not sure if "READY_TO_PICK_UP" is a status for pick ups
            # Status "PICKED_UP" confirms both deliveries and pick ups as done
            if order['status'] in ["OPEN", "PROCESSING", "READY_TO_DELIVER", "READY_TO_PICK_UP"]:
                _LOGGER.debug(f"Processing {order['type']} with id {order['id']} and status {order['status']}")
                details = self._get_order_details(order['id'])
                # DELIVERIES
                if order['type'] == "homeDelivery":
                    self._open_deliveries[order['id']] = Delivery(order, details)
                # PICK UPS
                elif order['type'] == "collection":
                    self._open_pick_ups[order['id']] = PickUp(order, details)

    def _update_basket(self):
        """ Retrieve basket """
        response = self._request_update(BASKET_URL)

        if 'basket' not in response:
            _LOGGER.debug(f"Unable to find basket")
            return

        if 'data' not in response['basket']:
            _LOGGER.debug(f"Unable to find basket")
            return

        self._basket = Basket(response['basket']['data'])

    def _update_time_slots(self):
        """ Update all time slots """
        self._update_delivery_time_slots()
        self._update_pick_up_time_slots()

    def _update_delivery_time_slots(self):
        """ Retrieve delivery time slots """
        response = self._request_update(DELIVERY_TIME_SLOTS_URL.format(storeId=self._profile.store.id))

        if 'timeSlots' not in response:
            _LOGGER.debug(f"Unable to find delivery time slots")
            return

        if 'data' not in response['timeSlots']:
            _LOGGER.debug(f"Unable to find delivery time slots")
            return

        self._delivery_time_slots = []

        for day in response['timeSlots']['data']:
            for time_slot in day['timeSlots']:
                self._delivery_time_slots.append(TimeSlot(time_slot))

    def _update_pick_up_time_slots(self):
        """ Retrieve pick up time slots """
        response = self._request_update(PICK_UP_TIME_SLOTS_URL.format(storeId=self._profile.store.id))

        if 'timeSlots' not in response:
            _LOGGER.debug(f"Unable to find pick up time slots")
            return

        if 'data' not in response['timeSlots']:
            _LOGGER.debug(f"Unable to find pick up time slots")
            return

        self._pick_up_time_slots = []

        for day in response['timeSlots']['data']:
            for time_slot in day['timeSlots']:
                self._pick_up_time_slots.append(TimeSlot(time_slot))

    def _get_order_details(self, order_id):
        """ Get details for your order """
        response = self._request_update(ORDER_DETAILS_URL.format(orderId=order_id))

        if 'order' not in response:
            _LOGGER.debug(f"Unable to find details for {order_id}")
            return

        if 'data' not in response['order']:
            _LOGGER.debug(f"Unable to find details for {order_id}")
            return

        return response['order']['data']

    def get_profile(self):
        """ Get your personal profile """
        self._update()
        return self._profile

    def get_open_deliveries(self):
        """ Get all open deliveries """
        self._update()
        return self._open_deliveries.values()

    def get_open_pick_ups(self):
        """ Get all open pick ups """
        self._update()
        return self._open_pick_ups.values()

    def get_basket(self):
        """ Get your current basket """
        self._update()
        return self._basket

    def get_open_delivery_time_slots(self):
        """" Get current open delivery time slots """
        self._update()

        return [
            ts
            for ts in self._delivery_time_slots
            if ts.is_available
        ]

    def get_open_pick_up_time_slots(self):
        """" Get current open pick up time slots """
        self._update()

        return [
            ts
            for ts in self._pick_up_time_slots
            if ts.is_available
        ]

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
            data = response.json()
            if 'code' in data:
                _LOGGER.error("Error code: " + data['code'])
                _LOGGER.error("Reason: " + data['message'])
            else:
                _LOGGER.error("Unable to perform request. Response: " + data)
            return {}

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
                'POST', AUTHENTICATE_URL, data=payload, headers={**headers, **DEFAULT_HEADERS})
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

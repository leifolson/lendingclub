"""
api.py
Copyright (C) 2017 Clinton Olson (clint.olson2@gmail.com) and contributors

This module is part of lendingclub and is released under
the MIT License: https://opensource.org/licenses/MIT
"""

import requests


# TODO: error handling
# TODO: more robustness etc...probably implement classes that use this api
class API(object):
    base_url = 'https://api.lendingclub.com/api/investor/'

    def __init__(self, account_id=None, token=None, version='v1'):
        self.__account_id = account_id
        self.__token = token
        self.__version = version
        self.accounts_url = self.base_url + self.__version + '/accounts/' + self.__account_id
        self.loans_url = self.base_url + self.__version + '/loans'
        self.header = {'Authorization': self.__token, 'Content-Type': 'application/json'}

    def get_account_summary(self):
        """

        :return:
        """
        r = requests.get(self.accounts_url + '/summary', headers=self.header)
        return r.json()

    # TODO: convert to proper types?
    def get_available_cash(self):
        r = requests.get(self.accounts_url + '/availablecash', headers=self.header)
        return r.json().get('availableCash')

    def add_funds(self, amount, transfer_frequency):
        payload = { 'transferFrequency': transfer_frequency,
                    'amount': amount}
        r = requests.post(self.accounts_url + '/funds/add', json=payload, headers=self.header)
        return r.json()

    # TODO: test
    def withdraw_funds(self, amount):
        payload = { 'amount': amount}
        r = requests.post(self.accounts_url + '/funds/withdraw', json=payload, headers=self.header)
        return r.json()

    def get_pending_transfers(self):
        r = requests.get(self.accounts_url + '/funds/pending', headers=self.header)
        return r.json()

    def cancel_tranfers(self, transfer_ids):
        payload = { 'transferIds': transfer_ids}
        r = requests.post(self.accounts_url + '/funds/cancel', json=payload, headers=self.header)
        return r.json()

    # TODO: test
    def get_notes_owned(self, detailed=False):
        if detailed:
            url = self.accounts_url + '/detailednotes'
        else:
            url = self.accounts_url + '/notes'

        r = requests.get(url, headers=self.header)
        return r.json()

    def get_portfolios_owned(self):
        r = requests.get(self.accounts_url + '/portfolios', headers=self.header)
        return r.json()

    def create_portfolio(self, name, description):
        payload = { 'actorId': self.__account_id,
                    'portfolioName': name,
                    'portfolioDescription': description}

        r = requests.post(self.accounts_url + '/portfolios', json=payload, headers=self.header)
        return r.json()

    # TODO: test
    def submit_order(self, orders):
        payload = { 'aid': self.__account_id,
                    'orders': orders}
        r = requests.post(self.accounts_url + '/orders', json=payload, headers=self.header)
        return r.json()

    # TODO: test
    def get_filters(self):
        r = requests.get(self.accounts_url + '/filters', headers=self.header)
        return r.json()

    def get_listed_loans(self, show_all=True, filter_id=None):
        if show_all:
            data = {'showAll': 'true',
                    'filterId': filter_id}
        else:
            data = {'showAll': 'false',
                    'filterId': filter_id}

        r = requests.get(self.loans_url + '/listing', headers=self.header, params=data)
        return r.json()

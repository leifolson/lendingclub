"""
api.py
Copyright (C) 2017 Clinton Olson (clint.olson2@gmail.com) and contributors

This module is part of lendingclub and is released under
the MIT License: https://opensource.org/licenses/MIT
"""

import requests

# TODO: error handling
# TODO: keep args named "payload"?
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
        r = requests.get(self.accounts_url + '/summary', headers=self.header)
        return r.json()

    # TODO: convert to proper types?
    def get_available_cash(self):
        r = requests.get(self.accounts_url + '/availablecash', headers=self.header)
        return r.json().get('availableCash')

    def add_funds(self, payload):
        r = requests.post(self.accounts_url + '/funds/add', data=payload, headers=self.header)
        return r.json()

    def withdraw_funds(self, payload):
        r = requests.post(self.accounts_url + '/funds/withdraw', data=payload, headers=self.header)
        return r.json()

    def get_pending_transfers(self):
        r = requests.get(self.accounts_url + '/funds/pending', headers=self.header)
        return r.json()

    def cancel_tranfers(self, payload):
        r = requests.post(self.accounts_url + '/funds/cancel', data=payload, headers=self.header)
        return r.json()

    def get_notes_owned(self, detailed=False):
        if detailed == True:
            url = self.accounts_url + '/detailednotes'
        else:
            url = self.accounts_url + '/notes'

        r = requests.get(url, headers=self.header)
        return r.json()

    def get_portfolios_owned(self):
        r = requests.get(self.accounts_url + '/portfolios', headers=self.header)
        return r.json()

    def create_portfolio(self, payload):
        r = requests.post(self.accounts_url + '/portfolios', data=payload, headers=self.header)
        return r.json()

    def submit_order(self, payload):
        r = requests.post(self.accounts_url + '/orders', data=payload, headers=self.header)
        return r.json()

    def get_filters(self):
        r = requests.get(self.accounts_url + '/filters', headers=self.header)
        return r.json()

    def get_listed_loans(self, show_all=True, filter_id=None):
        if show_all == True:
            data = { 'showAll': 'true',
                     'filterId': filter_id}
        else:
            data = {'showAll': 'false',
                    'filterId': filter_id}

        r = requests.get(self.loans_url + '/listing', headers=self.header, params=data)
        return r.json()

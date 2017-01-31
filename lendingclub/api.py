"""
api.py
Copyright (C) 2017 Clinton Olson (clint.olson2@gmail.com) and contributors

This module is part of lendingclub and is released under
the MIT License: https://opensource.org/licenses/MIT
"""

import requests


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
        Gets the details of the account.

        Returns
        -------
        dict
            a dictionary containing the account summary details

        """
        r = requests.get(self.accounts_url + '/summary', headers=self.header, timeout=5.0)
        return r.json()

    # TODO: convert to proper types?
    def get_available_cash(self):
        """
        Gets the current available cash in the account

        Returns
        -------
        float
            the available cash as a string

        """
        r = requests.get(self.accounts_url + '/availablecash', headers=self.header, timeout=5.0)
        return float(r.json().get('availableCash'))

    def add_funds(self, amount, transfer_frequency):
        """
        Initiates a funds transfer from the linked bank account to the Lending Club account.

        Parameters
        ----------
        amount: float
            the dollar amount to transfer

        transfer_frequency: str
            the frequency of the transfer

        Returns
        -------
        dict
            the result of the add funds request

        """
        payload = {'transferFrequency': transfer_frequency,
                   'amount': amount}
        r = requests.post(self.accounts_url + '/funds/add', json=payload, headers=self.header, timeout=5.0)
        return r.json()

    # TODO: test
    def withdraw_funds(self, amount):
        """
        Initiates a funds withdrawal from Lending Club to the linked bank account.

        Parameters
        ----------
        amount: float
            the dollar amount to withdraw

        Returns
        -------
        dict
            the result of the withdraw funds request

        """
        payload = {'amount': amount}
        r = requests.post(self.accounts_url + '/funds/withdraw', json=payload, headers=self.header, timeout=5.0)
        return r.json()

    def get_pending_transfers(self):
        """
        Gets the list of pending funds transfers, both additions and withdrawals.

        Returns
        -------
        [dict]
            the list of pending funds transfers

        """
        r = requests.get(self.accounts_url + '/funds/pending', headers=self.header, timeout=5.0)
        return r.json().get('transfers', [])

    def cancel_transfers(self, transfer_ids):
        """
        Requests that all transfers identified in transfer_ids be cancelled.

        Parameters
        ----------
        transfer_ids: [str]
            the list of transfer ids to cancel

        Returns
        -------
        [dict]
            the transfer status for each transfer cancel request

        """
        payload = {'transferIds': transfer_ids}
        r = requests.post(self.accounts_url + '/funds/cancel', json=payload, headers=self.header, timeout=5.0)
        return r.json().get('cancellationResults', [])

    # TODO: test
    def get_notes_owned(self, detailed=False):
        """
        Gets the list of notes currently owned in the account.

        Parameters
        ----------
        detailed: bool
            boolean flag, True returns detailed notes, False returns limited data.  Defaults to False.

        Returns
        -------
        [dict]
            a list of notes owned

        """
        if detailed:
            url = self.accounts_url + '/detailednotes'
        else:
            url = self.accounts_url + '/notes'

        r = requests.get(url, headers=self.header, timeout=5.0)
        return r.json().get('myNotes', [])

    def get_portfolios_owned(self):
        """
        Gets a list of account portfolios.

        Includes the portfolio id, name, and description.

        Returns
        -------
        [dict]
            a list of portfolio details

        """
        r = requests.get(self.accounts_url + '/portfolios', headers=self.header, timeout=5.0)
        return r.json().get('myPortfolios', [])

    def create_portfolio(self, name, description):
        """
        Creates a portfolio in the account.

        Returns the id, name, and description of the newly created portfolio.

        Parameters
        ----------
        name: str
            the name to give the portfolio

        description: str
            a description of the portfolio

        Returns
        -------
        dict
            portfolio creation response

        """
        payload = {'actorId': self.__account_id,
                   'portfolioName': name,
                   'portfolioDescription': description}

        r = requests.post(self.accounts_url + '/portfolios', json=payload, headers=self.header, timeout=5.0)
        return r.json()

    # TODO: test
    def submit_order(self, orders):
        """
        Submits a list of orders to Lending Club.

        An order must contain the loan id, requested amount (a multiple of $25), and optionally a portfolio id.

        Parameters
        ----------
        orders: [dict]
            a list of order dictionaries.
            e.g.,
            [{ "loanId":22222,
               "requestedAmount":55.0,
		       "portfolioId":44444 },
		        ...,
	         { "loanId": 44444,
		       "requestedAmount":25 }]

        Returns
        -------
        [dict]
            the order status for each order request

        """
        payload = {'aid': self.__account_id,
                   'orders': orders}
        r = requests.post(self.accounts_url + '/orders', json=payload, headers=self.header, timeout=5.0)
        return r.json()

    # TODO: test
    def get_filters(self):
        """
        Gets the list of filters defined within the account.

        Returns
        -------
        [dict]
            a list of filter data (id and name)

        """
        r = requests.get(self.accounts_url + '/filters', headers=self.header, timeout=5.0)
        return r.json()

    def get_listed_loans(self, show_all=True, filter_id=None):
        """
        Gets the current list of available loans on Lending Club.

        Results can be filtered by supplying the id of the filter to apply.

        Parameters
        ----------
        show_all: bool
            if True, shows all loans currently available, False returns loans from most recent listing period only

        filter_id: str
            the id of the filter to apply to the results, if any

        Returns
        -------
        dict
            a dict with the as-of-date and loan details list

        """
        if show_all:
            data = {'showAll': 'true',
                    'filterId': filter_id}
        else:
            data = {'showAll': 'false',
                    'filterId': filter_id}

        r = requests.get(self.loans_url + '/listing', headers=self.header, params=data, timeout=10.0)
        return r.json()

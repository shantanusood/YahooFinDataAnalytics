#!/usr/bin/env python3
import pickle

class data_download:

    def __init__(self, ticker, timestamp, html):
        self.ticker = ticker
        self.timestamp = timestamp
        self.html = html

    @property
    def ticker(self):
        return self.__ticker

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def html(self):
        return self.__html

    @ticker.setter
    def ticker(self, val):
        self.__ticker = val

    @timestamp.setter
    def timestamp(self, val):
        self.__timestamp = val

    @html.setter
    def html(self, val):
        self.__html = val

    def __str__(self):
        return "data_download(" + self.ticker + ", " + self.timestamp + ", [" + ''.join([i + ", " for i in self.html.keys()])[:-2] + "])"

    def __len__(self):
        return len(self.html)


def download_data(ticker):
    print(type(pickle))


download_data()

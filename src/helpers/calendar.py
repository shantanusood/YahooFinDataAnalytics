from obj import yahoo_obj as y
from src.helpers import commons as cm
import requests as r
from bs4 import BeautifulSoup

class calendar:
    start_date = ""
    end_date = ""
    target_date = ""
    offset = ""
    def __init__(self, start_date, end_date, target_date,  offset):
        self.start_date = start_date
        self.end_date = end_date
        self.target_date = target_date
        self.offset = offset

    def return_cal_table(self):
        req = r.get(cm.calendar(self.start_date, self.end_date, self.target_date, self.offset))
        soup = BeautifulSoup(req.text, 'html.parser')
        return soup.select(y.calendarTable())
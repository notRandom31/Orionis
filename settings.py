SEARCH_KEY = "AIzaSyClTavGZ6zMeYdLoOhAtCkEHh2LBP0DbNo"
SEARCH_ID = "cx=d601486bbbdbe4c17"
COUNTRY = "us"
SEARCH_URL = "https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&q={query}&start={start}&num=10&gl=" + COUNTRY
RESULT_COUNT = 20

import os
if os.path.exists("private.py"):
    from private import *
import datetime
import math
import re
from django.utils.html import strip_tags

def count_word(html_string):
    # html_string= """<h1>This is the testing</h1>"""
    word_string = strip_tags(html_string)
    mathching_word = re.findall(r'\w+',word_string)
    count = len(mathching_word)
    return count


def get_read_time(html_string):
    count = count_word(html_string)
    read_time_min = math.ceil(count/200.0) #200Wpm
    # read_time_sec = read_time_min*60
    # read_time = str(datetime.timedelta(minutes=read_time_min))
    return int(read_time_min)
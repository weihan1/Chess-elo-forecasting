import numpy as np
import matplotlib.pyplot as plt
import datetime
from api_acess import client
import calendar
from dateutil import parser


entries_of_bullet_ratings = \
client.users.get_rating_history("bibimbap123")[0]["points"]

def create_bullet_list(bullet_ratings):
    '''
    Creates a list of bullet ratings from the list of dictionaries
    returned by the api call.
    '''
    lst = []
    for entry in bullet_ratings:
        lst.append(entry[3])
    return lst
ratings = create_bullet_list(entries_of_bullet_ratings)


def times_list(bullet_ratings):
    '''
    Creates a list of tuples of the form (year, month, day) from the
    list of dictionaries returned by the api call.
    '''
    tl = []
    for entry in bullet_ratings:
        tl.append((str(entry[0]), calendar.month_name[entry[1]+1], \
                   str(entry[2])))
    return tl
times = times_list(entries_of_bullet_ratings)



def tuple_to_str(time):
    '''
    Converts a list of tuples of the form (year, month, day) to a list
    '''
    l = []
    for entry in time: 
        l.append(', '.join(entry))
    return l
str_times = tuple_to_str(times)



def str_to_datetime(time):
    '''
    Converts a list of strings of the form "year, month, day" to a list
    of datetime objects.'''
    l = []
    for entry in time:
        l.append(parser.parse(entry))
    return l
dtime = str_to_datetime(str_times)


fig, ax = plt.subplots()
fig.autofmt_xdate()
plt.plot(dtime, ratings)
plt.show()
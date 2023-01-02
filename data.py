import numpy as np
import matplotlib.pyplot as plt
import datetime
from api_access import client
import calendar
from dateutil import parser
import matplotlib
from datetime import datetime
import pandas as pd


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


def dictionary_mapping(time, ratings):
    '''
    Creates a dictionary mapping the datetime objects to the ratings.
    '''
    d = {}
    for i in range(len(time)):
        d[time[i]] = ratings[i]
    return d

dictionary_map = dictionary_mapping(dtime, ratings)
# print(dictionary_map)


def monthly_rating(dictionary):
    '''
    Creates a dictionary mapping the month and the year to the average rating.
    '''
    monthly_ratings = {}
    for key in dictionary:
        if (key.year, key.month) in monthly_ratings:
            monthly_ratings[(key.year, key.month)].append(dictionary[key])
        else:
            monthly_ratings[(key.year, key.month)] = [dictionary[key]]
    for key in monthly_ratings:
        monthly_ratings[key] = np.mean(monthly_ratings[key])
    return monthly_ratings


monthly_ratings = monthly_rating(dictionary_map)
# print(monthly_ratings)


def plot_ratings(dictionary):
    '''
    Plots the monthly ratings.
    '''
    x_values = [datetime(*(date+(1,))) for date in dictionary.keys()]
    y_values = list(dictionary.values())
    dates = matplotlib.dates.date2num(x_values)
    plt.plot_date(dates, y_values, linestyle='solid', marker='o')
    # plt.plot(dates, y_values, 'o')
    plt.show()

# plot_ratings(monthly_ratings)


def train_test_split(dictionary):
    '''
    Splits the dictionary into a training and testing set, every rating before 2022-07-01
    is in the training set, and every rating after 2022-07-01 is in the testing set.
    '''
    train = []
    test = []
    for key in dictionary:
        if key[0] < 2022 or (key[0] == 2022 and key[1] < 7):
            train.append(dictionary[key])
        else:
            test.append(dictionary[key])
    return train, test

def create_df(dictionary):
    '''
    Creates a dataframe from the dictionary mapping the month and year to the average rating.
    '''
    df = pd.DataFrame(list(dictionary.items()), columns = ['ds', 'y'])
    df['ds'] = pd.to_datetime(df['ds'].apply(lambda x: datetime(*(x+(1,)))))
    return df

df = create_df(monthly_ratings)
print(df)



    

# fig, ax = plt.subplots()
# fig.autofmt_xdate()
# plt.plot(dtime, ratings)
# plt.show()

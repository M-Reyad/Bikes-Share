# Importing the required Libraries:- #
# Created By: Mohamed Reyad#
# Last Edited 18/01/2022#


import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Global Declaration:- #
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ["all", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
          "november", "december"]
days = ["all", "saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]


# Get Filters Function:- #
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! \n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while city not in ["chicago", "new york city", "washington"]:
        city = input("Enter one of the following cities \n"
                     "- Chicago \n"
                     "- New York City \n"
                     "- Washington \n")
        city = city.lower()
        print("Well, You selected {} \n \n".format(city))

    # get user input for month (all, january, february, ... , june)
    month = ""
    while month not in months:
        month = input("Enter one of the following Months \n"
                      "- January \n"
                      "- February \n"
                      "- March \n"
                      "- April \n"
                      "- May \n"
                      "- June \n"
                      "- July \n"
                      "- August \n"
                      "- September \n"
                      "- October \n"
                      "- November \n"
                      "- December \n"
                      "- Or type 'all' to apply No month filter ")
        month = month.lower()
        if month == "all":
            print("That's great, you decided not to filter with Month!!")
        else:
            print("That's great! You selected {}".format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while day not in days:
        day = input("Enter on of the following days (Type the Name Correctly!!):\n"
                    "- Saturday \n"
                    "- Sunday \n"
                    "- Monday \n"
                    "- Tuesday \n"
                    "- Wednesday \n"
                    "- Thursday \n"
                    "- Friday \n"
                    "Or type all to apply no day filter ")
        day = day.lower()
        if day == "all":
            print("Awesome, you decided not to filter with a Day!")
        else:
            print("Awesome! You selected to filter with {}".format(day))

    print('-' * 40)
    return city, month, day


# Load Data Frame with the applied filters:- #
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Read the csv file
    file_name = CITY_DATA[city]
    df = pd.read_csv('./{}'.format(file_name))

    # Convert the Start Time/ End Time to datetime type
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])

    # Generate Day Column
    df["Day"] = df["Start Time"].dt.weekday_name

    # Generate Month Column
    df["Month"] = df["Start Time"].dt.month

    # Generate Year Column
    df["Year"] = df["Start Time"].dt.year

    # Generate Start Time Column
    df["Start hr"] = df["Start Time"].dt.time

    # Generate End Time Column
    df["End hr"] = df["End Time"].dt.time

    # Applying Day Filter:-
    if day != "all":
        df = df[df["Day"] == day.title()]

    # Applying Month Filter:-
    if month != "all":
        month = months.index(month)
        df = df[df["Month"] == month]

    print("There are Nan cells with counts as follows {}".format(df.isnull().sum()))

    # Eliminating Nan Rows!:- #
    # df.dropna(axis = 0)

    print(len(df))

    return df


# Time Stats Function:- #
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if len(df["Month"].unique()) != 1:
        most_common_month = df["Month"].mode()[0]
        print("Most Common Month is \n{} \n".format(most_common_month))
    else:
        print("As you selected to filter with a Month, there wouldn't be a Most Common Month Stats!! \n")

    # display the most common day of week
    if len(df["Day"].unique()) != 1:
        most_common_day = df["Day"].mode()[0]
        print("Most Common Day is \n{} \n".format(most_common_day))
    else:
        print("As you selected to filter with a Day, there wouldn't be a Most Common Day Stats!! \n")

    # display the most common start hour
    most_common_start_hr = df["Start hr"].mode()[0]
    print("Most Common Start Hour is \n{} \n".format(most_common_start_hr))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


# Station Stats Function:- #
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df["Start Station"].mode()[0]
    print("Most common Start Station is \n{} \n".format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df["End Station"].mode()[0]
    print("Most common End Station is \n{}\n".format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    df["Trip"] = df["Start Station"] + " to " + df["End Station"]
    most_frequent_combination = df["Trip"].mode()[0]
    print("Most Frequent Combination of Start:End Stations trips is \n{} \n".format(most_frequent_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


# Trip Duration Stats:- #
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_travel_time = df["Trip Duration"].sum()

    print("Total Travel Time is {} seconds \n".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("Mean Travel Time is {} seconds \n".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


# User Stats Function:- #
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users_counts = df["User Type"].value_counts()
    print(users_counts)

    # Display counts of gender | Only Washington Doesn't have Gneder/Year Stats!!
    try:
        gender_counts = df["Gender"].value_counts()
        print(gender_counts)

        # Display earliest, most recent, and most common year of birth
        earliest_year = int(df["Birth Year"].min())
        print("Earliest Year using Bikes Share is {} \n".format(earliest_year))

        most_recent_year = int(df["Birth Year"].max())
        print("Most Recent Year using Bikes Share is {} \n".format(most_recent_year))

        common_year = int(df["Birth Year"].mode()[0])
        print("Most Common Year using Bikes Share is {} \n".format(common_year))

    except KeyError:
        print("Unfortunately, Washington doesn't have Gender nor Birth Year Stats!! \n \n \n")

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-' * 40)


def show_row_data(df):
    reply = (input("Do you want to see the row data? Type 'Yes' or 'No'")).lower()
    rows = 0
    while reply == "yes":
        print(df.iloc[rows: rows + 5])
        rows += 5
        reply = (input("Do you want to see the row data? Type 'Yes' or 'No'")).lower()


# Main Function:- #
def main():
    while True:
        city, month, day = get_filters()  # done
        df = load_data(city, month, day)
        if df.empty:
            print("Empty DataFrame; No Data is Available, please select other Filters")
            continue

        else:
            time_stats(df)  # done
            station_stats(df)
            trip_duration_stats(df)  # done
            user_stats(df)  # done
            show_row_data(df)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break


# Starting Point:- #
if __name__ == "__main__":
    main()

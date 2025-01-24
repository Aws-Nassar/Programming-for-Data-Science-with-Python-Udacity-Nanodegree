import time
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

DATA_FILES = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_inputs():
    """
    Collects user inputs for city, month, and day filters.

    Returns:
        (str) selected_city - chosen city to analyze
        (str) selected_month - chosen month to filter by, or 'all' for no filter
        (str) selected_day - chosen day to filter by, or 'all' for no filter
    """
    print("Welcome! Let's analyze US bikeshare data.\n")
    
    # Get city input
    selected_city = input("Choose a city (Chicago, New York City, Washington): ").strip().lower()
    while selected_city not in DATA_FILES:
        print("Invalid choice. Please select from Chicago, New York City, or Washington.")
        selected_city = input("Try again: ").strip().lower()
    
    # Get month input
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    selected_month = input("Enter a month (January to June) or 'all' for no filter: ").strip().lower()
    while selected_month not in valid_months:
        print("Invalid month. Please enter a valid month or 'all'.")
        selected_month = input("Try again: ").strip().lower()

    # Get day input
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    selected_day = input("Enter a day (Monday to Sunday) or 'all' for no filter: ").strip().lower()
    while selected_day not in valid_days:
        print("Invalid day. Please enter a valid day or 'all'.")
        selected_day = input("Try again: ").strip().lower()

    print("\nFilters applied successfully!")
    print("=" * 50)
    return selected_city, selected_month, selected_day


def load_data(city, month, day):
    """
    Loads and filters data based on city, month, and day.

    Args:
        city (str): Selected city
        month (str): Selected month or 'all' for no filter
        day (str): Selected day or 'all' for no filter
    
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    logging.info("Loading data for city: %s", city)
    data = pd.read_csv(DATA_FILES[city])

    data['Start Time'] = pd.to_datetime(data['Start Time'])
    data['month'] = data['Start Time'].dt.month
    data['day_of_week'] = data['Start Time'].dt.day_name()

    if month != 'all':
        month_idx = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        data = data[data['month'] == month_idx]

    if day != 'all':
        data = data[data['day_of_week'].str.lower() == day]

    return data


def display_time_stats(data):
    """Displays the most frequent times of travel."""
    print("\n--- Most Frequent Times of Travel ---\n")
    
    popular_month = data['month'].mode()[0]
    print(f"Most Common Month: {popular_month}")

    popular_day = data['day_of_week'].mode()[0]
    print(f"Most Common Day: {popular_day}")

    data['hour'] = data['Start Time'].dt.hour
    popular_hour = data['hour'].mode()[0]
    print(f"Most Common Start Hour: {popular_hour}")
    print("=" * 50)


def display_station_stats(data):
    """Displays the most popular stations and trips."""
    print("\n--- Most Popular Stations and Trips ---\n")

    most_common_start = data['Start Station'].mode()[0]
    print(f"Most Common Start Station: {most_common_start}")

    most_common_end = data['End Station'].mode()[0]
    print(f"Most Common End Station: {most_common_end}")

    most_common_trip = data.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"Most Common Trip: {most_common_trip[0]} to {most_common_trip[1]}")
    print("=" * 50)


def display_trip_duration_stats(data):
    """Displays statistics on trip durations."""
    print("\n--- Trip Duration Statistics ---\n")
    
    total_seconds = data['Trip Duration'].sum()
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    print(f"Total Trip Duration: {int(hours)}h {int(minutes)}m {int(seconds)}s")

    mean_seconds = data['Trip Duration'].mean()
    mean_min = int(mean_seconds // 60)
    mean_sec = int(mean_seconds % 60)
    print(f"Mean Trip Duration: {mean_min}m {mean_sec}s")
    print("=" * 50)


def display_user_stats(data):
    """Displays user-related statistics."""
    print("\n--- User Statistics ---\n")

    user_types = data['User Type'].value_counts()
    print("Counts by User Type:")
    print(user_types)

    if 'Gender' in data.columns:
        gender_counts = data['Gender'].value_counts()
        print("\nCounts by Gender:")
        print(gender_counts)

    if 'Birth Year' in data.columns:
        earliest_birth = data['Birth Year'].min()
        most_recent_birth = data['Birth Year'].max()
        most_common_birth = data['Birth Year'].mode()[0]
        print("\nBirth Year Stats:")
        print(f"Earliest Year: {earliest_birth}")
        print(f"Most Recent Year: {most_recent_birth}")
        print(f"Most Common Year: {most_common_birth}")
    print("=" * 50)


def raw_data_display(data):
    """Displays raw data upon user request."""
    print("\nDisplaying Raw Data (5 rows at a time)...")
    start_loc = 0
    while True:
        show_data = input("Would you like to see 5 rows of data? Enter yes or no: ").strip().lower()
        if show_data == 'yes':
            print(data.iloc[start_loc:start_loc + 5])
            start_loc += 5
        elif show_data == 'no':
            break
        else:
            print("Invalid input. Please enter yes or no.")


def main():
    while True:
        city, month, day = get_inputs()
        data = load_data(city, month, day)

        display_time_stats(data)
        display_station_stats(data)
        display_trip_duration_stats(data)
        display_user_stats(data)
        raw_data_display(data)

        restart = input("\nWould you like to restart? Enter yes or no: ").strip().lower()
        if restart != 'yes':
            print("Thank you for using the bikeshare analysis tool. Goodbye!")
            break
    
    print("Analysis complete! Check the stats above.")


if __name__ == "__main__":
    main()

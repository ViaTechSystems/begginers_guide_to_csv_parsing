from collections import defaultdict
from datetime import datetime
import random

from dateutil.relativedelta import relativedelta


def make_example_data_csv():
    """
    used to create example csv to parse
    """

    list_of_dictionary_data = [
        # person 1
        {'first name': 'John', 'last name': 'Smith', 'employee number': 34345,
         'time-in': None, 'time-out': None, 'minutes break': 0, 'date': None,
         'amount per hour': f"{random.randint(10, 25)}{str(round(random.uniform(.50, .90), 2)).zfill(2)}"},
        # person 2
        {'first name': 'Sarah', 'last name': 'Jenkins', 'employee number': 66798,
         'time-in': None, 'time-out': None, 'minutes break': 0, 'date': None,
         'amount per hour': f"{random.randint(10, 25)}{str(round(random.uniform(.50, .90), 2)).zfill(2)}"},
        # person 3
        {'first name': 'Henry', 'last name': 'Orlando', 'employee number': 87654,
         'time-in': None, 'time-out': None, 'minutes break': 0, 'date': None,
         'amount per hour': f"{random.randint(10, 25)}{str(round(random.uniform(.50, .90), 2)).zfill(2)}"},
        # person 4
        {'first name': 'Jordan', 'last name': 'Smalls', 'employee number': 23474,
         'time-in': None, 'time-out': None, 'minutes break': 0, 'date': None,
         'amount per hour': f"{random.randint(10, 25)}{str(round(random.uniform(.50, .90), 2)).zfill(2)}"},
        # person 5
        {'first name': 'Henrietta', 'last name': 'Little', 'employee number': 56876,
         'time-in': None, 'time-out': None, 'minutes break': 0, 'date': None,
         'amount per hour': f"{random.randint(10, 25)}{str(round(random.uniform(.50, .90), 2)).zfill(2)}"},
    ]
    # make file...
    with open('example.csv', 'w') as file:
        file.write('first name, last name, employee number, time-in, time-out, minutes break, date, amount per hour')
        # loop negative 25 days
        for i in range(25, 0, -1):
            # current date - 1 day in range of 25
            cur_date = datetime.now() - relativedelta(days=i)

            # loop over all people and create valid looking fake data
            for person in list_of_dictionary_data:
                person['time-in'] = f"{str(random.randint(5, 9)).zfill(2)}:{str(random.randint(0, 59)).zfill(2)} AM"
                person['time-out'] = f"{str(random.randint(4, 8)).zfill(2)}:{str(random.randint(0, 59)).zfill(2)} PM"
                person['minutes break'] = random.randint(0, 60)
                person['date'] = cur_date.strftime("%m/%d/%Y")
                file.write(f"\n{person['first name']},{person['last name']},{person['employee number']},"
                           f"{person['time-in']},{person['time-out']},{person['minutes break']},"
                           f"{person['date']},{person['amount per hour']}")

    print('file created')


# only invoke if called explilicitly
if __name__ == "__main__":
    # run program
    # make_example_data_csv()

    with open('example.csv', 'r+') as file:
        # get column names, they are the first line of a CSV file
        first_line = file.readline().strip()
        # each line is separated by a , so we can logically make a list of it
        columns = [x.strip() for x in first_line.split(',')]  # turn into list with split

        # we want a default dictionary to store grouped entries,
        # which is a very common and useful datatype in Python, we use default because we need the values
        # to be lists by default
        dict_of_entries_grouped = defaultdict(list)

        # the file is open and named 'file' in our code, now loop over the lines of it
        for line in file.readlines():
            # turn line into a list as we did above
            list_of_entry_data = [x.strip() for x in line.split(',')]
            # turn into a dict for easier grouping and accessibility
            dict_of_data = dict(zip(columns, list_of_entry_data))
            # we will group users by employee number because
            # that is easier than both first and last name,
            # and now we can easily grab it due to using a dict
            dict_of_entries_grouped[dict_of_data['employee number']].append(dict_of_data)

    final_dict_sorted = dict()
    # now we need to find the minutes worked
    for employee_number, entry_dict_list in dict_of_entries_grouped.items():
        final_dict_sorted[employee_number] = {
            'amount_per_hour': None,
            'employee_name': '',
            'total_minutes_worked': 0,
            'amount_paid': 0,
            # 'entry_dict_list': entry_dict_list
        }
        for entry_dict in entry_dict_list:
            time_in = datetime.strptime(entry_dict['time-in'], '%I:%M %p')
            time_out = datetime.strptime(entry_dict['time-out'], '%I:%M %p')
            time_there = time_out - time_in
            time_in_seconds = time_there.seconds
            minutes = (time_in_seconds // 60) % 60
            final_dict_sorted[employee_number]['total_minutes_worked'] += minutes
            final_dict_sorted[employee_number]['amount_per_hour'] = entry_dict['amount per hour']

            # get amount paid. First convert amount per hour to minute payments
            amount_paid = (float(entry_dict['amount per hour']) / 60) * minutes
            # now update the final dict
            final_dict_sorted[employee_number][
                'employee_name'] = f"{entry_dict['first name']} {entry_dict['last name']}"
            final_dict_sorted[employee_number]['amount_paid'] += amount_paid
        # round to 2 decimals
        final_dict_sorted[employee_number]['amount_paid'] = round(final_dict_sorted[employee_number]['amount_paid'], 2)

    print(final_dict_sorted)

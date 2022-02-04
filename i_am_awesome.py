from collections import defaultdict
from datetime import datetime
import random
from dateutil.relativedelta import relativedelta

with open('example.csv', 'r+') as file:
    # get column names
    first_line = file.readline().strip()
    columns = [x.strip() for x in first_line.split(',')]
    entries = defaultdict(list)
    # loop the file and group the data
    for line in file.readlines():
        # turn line into a list as we did above
        list_of_entry_data = [x.strip() for x in line.split(',')]
        # turn into a dict for easier grouping and accessibility
        dict_of_data = dict(zip(columns, list_of_entry_data))
        # group users by employee number because names can be the same
        entries[dict_of_data['employee number']].append(dict_of_data)

# this is your final data dictionary
final_dict = dict()
for emp_num, entry_dict_list in entries.items():
    final_dict[emp_num] = {
        'employee_name': '', 'minutes_worked': 0,
        'amount_paid': 0, 'amount_hour': None,
        'amount_per_minute': None,
    }
    for _dict in entry_dict_list:
        # get timing worked out
        time_in = datetime.strptime(_dict['time-in'], '%I:%M %p')
        time_out = datetime.strptime(_dict['time-out'], '%I:%M %p')
        # minutes are easier to work with here because
        # people don't work solid hours
        time_in_minutes = ((time_out - time_in).seconds // 60) % 60
        final_dict[emp_num]['minutes_worked'] += time_in_minutes
        final_dict[emp_num]['amount_hour'] = _dict['amount per hour']
        amount_per_minute = (float(_dict['amount per hour']) / 60)
        final_dict[emp_num]['amount_per_minute'] = amount_per_minute
        # get amount paid which is time in min * amount per min
        amount_paid = amount_per_minute * time_in_minutes
        name = f"{_dict['first name']} {_dict['last name']}"
        final_dict[emp_num]['employee_name'] = name
        final_dict[emp_num]['amount_paid'] += amount_paid
    # round to 2 decimals
    final_dict[emp_num]['amount_paid'] = round(
        final_dict[emp_num]['amount_paid'], 2
    )
# write the final file back to the folder...
with open('final_payments.csv', 'w+') as file:
    # add new header to exported file
    file.write('employee_name,minutes_worked,'
               'amount_paid,amount_hour,amount_per_minute')
    for emp_num, data in final_dict.items():
        file.write(
            f"\n{data['employee_name']},"f"{data['minutes_worked']},"
            f"{data['amount_paid']}, {data['amount_hour']}, "
            f"{data['amount_per_minute']}")
print('output file created...')

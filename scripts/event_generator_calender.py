from ics import Calendar, Event
import csv

event_description = ""
with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if int(row[3]) >= 7:
            break
        event_description = event_description + str(row[0]) + " in " + str(row[3]) + " days\n"

c = Calendar()
e = Event()
e.name = "Items expiring this week"
e.description = event_description
e.begin = '2021-02-05 20:15:00'
c.events.add(e)
c.events

with open('my.ics', 'w') as my_file:
    my_file.writelines(c)
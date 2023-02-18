import tkinter as tk
import xml.etree.ElementTree as ET
import requests
from datetime import datetime, timedelta

# Define the initial lists of north-bound and south-bound trains
northbound_trains = []
southbound_trains = []

# Create a new Tkinter window
root = tk.Tk()
root.title('Train Queues')
root.geometry("500x500")

TODAY = datetime.today()
OSTRING = "Western (O'Hare Branch)"

# Create a label for the time until the next train
time_label = tk.Label(root, text='')
time_label.pack(side='top', fill='x', anchor='n')
time_label.configure(text=f'Next train in: ')

# Create a label for the current time
cur_time_label = tk.Label(root, text='')
cur_time_label.pack(side='bottom', fill='x')

# Create a frame for the north-bound train queue
north_frame = tk.Frame(root)
north_frame.pack(side='left', padx=10, fill='y')



# Create a label for each north-bound train and its arrival time
north_train_labels = []
for train, time in northbound_trains:
    north_train_label = tk.Label(north_frame, text=f'{train} - {time}')
    north_train_label.pack()
    north_train_labels.append(north_train_label)

# Create a frame for the south-bound train queue
south_frame = tk.Frame(root)
south_frame.pack(side='right', padx=10, fill='y')



# Create a label for each south-bound train and its arrival time
south_train_labels = []
for train, time in southbound_trains:
    south_train_label = tk.Label(south_frame, text=f'{train} - {time}')
    south_train_label.pack()
    south_train_labels.append(south_train_label)


def extract_times(queue: list, element: ET):
    stop_name = element.find('eta').find('staNm').text
    # print(f"Next {stop_name} trains:")
    for i, train in enumerate(element.findall('eta')):
        time = train.find('arrT').text.split(' ')[-1]
        time = datetime.strptime(time, '%H:%M:%S').time()
        dt = datetime.combine(TODAY, time)
        queue.append([dt, stop_name])
        # print(f"#{i+1} - {time}")
    return queue


def update_train_queues():
    # Make an HTTP API request to get the latest arrival times
    ro = requests.get('http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=97e711e0e761419e89d0ee28c76f0ef5&mapid=40670')
    rf = requests.get('http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=97e711e0e761419e89d0ee28c76f0ef5&mapid=40220')
    

    # Check if the API request was successful
    if ro.status_code == 200 and rf.status_code == 200:
        # Parse the response JSON to get the north-bound and south-bound train queues
        ror = ET.fromstring(ro.text)
        rfr = ET.fromstring(rf.text)
        ror_trains, rfr_trains = [], []

        ror_trains = extract_times(ror_trains, ror)
        rfr_trains = extract_times(rfr_trains, rfr)

        all_trains = ror_trains + rfr_trains

        # Clear the old labels from the train queue frames
        for widget in north_frame.winfo_children():
            widget.destroy()

        # Create a label for the north-bound train queue
        north_label = tk.Label(north_frame, text='North-bound Trains')
        north_label.pack()

        for widget in south_frame.winfo_children():
            widget.destroy()

        # Create a label for the south-bound train queue
        south_label = tk.Label(south_frame, text='South-bound Trains')
        south_label.pack()

        # Add new labels for each train and its arrival time to the train queue frames
        for time, dir in all_trains:
            if dir == OSTRING:
                north_train_label = tk.Label(north_frame, text=f'{time}')
                north_train_label.pack()
            else:
                south_train_label = tk.Label(south_frame, text=f'{time}')
                south_train_label.pack()

        # Calculate the time until the next train and update the time label
        now = datetime.now()
        next_train = min(all_trains, key=lambda x: x[0])
        next_train_time = next_train[0] - now + timedelta(hours=0, minutes=0, seconds=20) if next_train[1] == OSTRING else next_train[0] - now - timedelta(hours=0, minutes=0, seconds=20)
        next_train_direction = "O'Hare" if next_train[1] == OSTRING else 'FP'
        days, seconds = next_train_time.days, next_train_time.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        hours = hours if hours > 9 else f'0{hours}'
        minutes = minutes if minutes > 9 else f'0{minutes}'
        seconds = seconds if seconds > 9 else f'0{seconds}'
        time_label.configure(text=f'Next train in {hours}:{minutes}:{seconds} - ({next_train_direction})')
    
    # Update current time
    cur_time_label.configure(text=f'Current Time: {time.now().hour}:{time.now().minute}')

    # Schedule the next update of the train queues after a few seconds
    root.after(1000, update_train_queues)

# Schedule the first update of the train queues after a few seconds
root.after(0, update_train_queues)

# Run the main loop of the Tkinter window
root.mainloop()
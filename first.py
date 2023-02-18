import tkinter as tk

# Define the list of north-bound trains and their arrival times
northbound_trains = [
    ('Train A', '10:00'),
    ('Train B', '11:15'),
    ('Train C', '12:30')
]

# Define the list of south-bound trains and their arrival times
southbound_trains = [
    ('Train D', '09:45'),
    ('Train E', '11:00'),
    ('Train F', '12:15')
]

# Create a new Tkinter window
root = tk.Tk()
root.title('Train Queues')

# Create a frame for the north-bound train queue
north_frame = tk.Frame(root)
north_frame.pack(side='left', padx=10)

# Create a label for the north-bound train queue
north_label = tk.Label(north_frame, text='North-bound Trains')
north_label.pack()

# Create a label for each north-bound train and its arrival time
for train, time in northbound_trains:
    north_train_label = tk.Label(north_frame, text=f'{train} - {time}')
    north_train_label.pack()

# Create a frame for the south-bound train queue
south_frame = tk.Frame(root)
south_frame.pack(side='right', padx=10)

# Create a label for the south-bound train queue
south_label = tk.Label(south_frame, text='South-bound Trains')
south_label.pack()

# Create a label for each south-bound train and its arrival time
for train, time in southbound_trains:
    south_train_label = tk.Label(south_frame, text=f'{train} - {time}')
    south_train_label.pack()

# Run the main loop of the Tkinter window
root.mainloop()
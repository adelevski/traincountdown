from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from tkinter import *
import tkinter as tk
import requests
import asyncio
import time


TODAY = datetime.today()
OSTRING = "Western (O'Hare Branch)"
root = Tk()


class TrainWatch:

    def __init__(self, root):
        self.root = root


    def extract_times(self, queue: list, element: ET):
        stop_name = element.find('eta').find('staNm').text
        # print(f"Next {stop_name} trains:")
        for i, train in enumerate(element.findall('eta')):
            time = train.find('arrT').text.split(' ')[-1]
            time = datetime.strptime(time, '%H:%M:%S').time()
            dt = datetime.combine(TODAY, time)
            queue.append([dt, stop_name])
            # print(f"#{i+1} - {time}")
        return queue

    def myCoroutine(self):
        ro = requests.get('http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=97e711e0e761419e89d0ee28c76f0ef5&mapid=40670')
        rf = requests.get('http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=97e711e0e761419e89d0ee28c76f0ef5&mapid=40220')
        ror = ET.fromstring(ro.text)
        rfr = ET.fromstring(rf.text)
        all_times = []

        all_times = self.extract_times(all_times, ror)
        all_times = self.extract_times(all_times, rfr)

        next_train = min(all_times, key=lambda x: x[0])
        next_train_time = next_train[0] - datetime.now() + timedelta(hours=0, minutes=0, seconds=20) if next_train[1] == OSTRING else next_train[0] - datetime.now() - timedelta(hours=0, minutes=0, seconds=20)
        next_train_direction = "O'Hare" if next_train[1] == OSTRING else 'FP'
        # print(all_times)
        print(f"Next train in: {next_train_time} heading towards {next_train_direction}")
        root.after(1000, self.myCoroutine)


    def main(self):

        # GUI window config
        self.root.geometry("300x300")
        self.root.title("Train Watch")

        self.root.after(1000, self.myCoroutine)
        self.root.mainloop()

if __name__ == '__main__':
    watcher = TrainWatch(root)
    watcher.main()
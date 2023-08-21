import os
import requests
from dotenv import load_dotenv
import json
import tkinter as tk
import tkintermapview as tkm
from tkinter import *

load_dotenv()

WEATHER_URL = os.getenv("WEATHER_URL")
API_KEY = os.getenv("API_KEY")

mapShown = True
def showMap():
        searchedCity = searchBar.get("1.0","end-1c")
        url =  f"{WEATHER_URL}key={API_KEY}&q={searchedCity}&lang=ko"
        response = requests.get(url).json()
        print(response)

        try:
            latitude = response['location']['lat']
            longitute = response['location']['lon']
        except KeyError:
            print("Location not found")
        else:
            map_widget.set_position(latitude, longitute)
            map_widget.set_zoom(12)
            map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            searchButton.lift()
            mapShown = True

root = tk.Tk()
root.geometry("1024x768")
root.title("Weather checker")
root.configure(background="#333333")
#root['padx'] = 20
#['pady'] = 15


sideBar = tk.Frame(root, height=1024, width=50)
sideBar.pack(side=tk.LEFT)

searchBar = tk.Text(root,height=1, width=30, font=("Arial",20), background="white", fg="black", relief=tk.RAISED, pady=10, padx=35)
searchBar.pack(pady=10)

searchButton = tk.Button(root, text="Search",height=2, width=5, command=showMap)
searchButton.pack()

map_widget = tkm.TkinterMapView(root, width=1024, height=768, corner_radius=0)





root.mainloop()
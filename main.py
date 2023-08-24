import os
import requests
from dotenv import load_dotenv
import json
import tkinter as tk
import tkintermapview as tkm
from tkinter import *
from screeninfo import get_monitors



load_dotenv()

WEATHER_URL = os.getenv("WEATHER_URL")
API_KEY = os.getenv("API_KEY")

monitors = get_monitors()
for monitor in monitors:
    screen_width = int(monitor.width*0.5)
    screen_height = int(monitor.height *0.5)
    break

sidebarClosedWidth = 0.06*screen_width
sidebarOpenWidth = 0.2*screen_width
sidebarOpen = False
mapShown = True
def showMap():
        searchedCity = searchBar.get()
        url =  f"{WEATHER_URL}key={API_KEY}&q={searchedCity}&lang=en"
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
            searchBar.lift()
            sideBar.lift()
            mapShown = True


            sideBarCanvas.pack()
            sideBarCanvasButton = sideBarCanvas.create_window(sidebarClosedWidth * 0.5, screen_height * 0.1,window=weatherButton)


def showWeatherInfo():
    metric = True
    global sidebarOpen
    searchedCity = searchBar.get()
    url = f"{WEATHER_URL}key={API_KEY}&q={searchedCity}&lang=en"
    response = requests.get(url).json()
    if metric:
        currentTemp = str(response['current']['temp_c']) + " °C"
    else:
        currentTemp = str(response['current']['temp_f']) + " °F"

    condition = response['current']['condition']['text']
    print(condition)
    print(f"Showing weather of {searchedCity}")
    if sidebarOpen == False:
        sideBarCanvas.create_line(sidebarClosedWidth+5,screen_height *0.1- 32,sidebarClosedWidth+5,screen_height*0.9+32,fill="grey",width=1)
        sideBarCanvas.create_text(sidebarOpenWidth  *0.5, screen_height *0.1, text=f"{currentTemp}\n{condition}")

        sideBarCanvas.config(width=sidebarOpenWidth)
        sidebarOpen = True
    else:
        sideBarCanvas.config(width=sidebarClosedWidth)
        sidebarOpen = False

def calculateTemp(response,temp_kelvin, metric):
    if metric:
        temp_celsius = temp_kelvin - 273.15
        return temp_celsius
    else:
        temp_fahrenheit = (temp_kelvin - 273.15) *(9/5) +32
        return temp_fahrenheit



root = tk.Tk()
root.geometry(f"{screen_width}x{screen_height}")
root.title("Weather checker")
root.configure(background="#333333")

sideBar = tk.Frame(root)
sideBar.pack(side=tk.LEFT)
sideBarCanvas = tk.Canvas(sideBar, width=sidebarClosedWidth, height=screen_height)

weatherImage = PhotoImage(file="weather/64x64/day/113.png")
weatherButton = tk.Button(sideBarCanvas, height=64, width= 64, image=weatherImage,bd=0, highlightthickness=0, command=showWeatherInfo)

searchBar = tk.Entry(root)

searchBar.pack(pady=10)

searchButton = tk.Button(root, text="Search",height=2, width=5, command=showMap)
searchButton.pack()

map_widget = tkm.TkinterMapView(root, width=1024, height=768, corner_radius=0)





root.mainloop()
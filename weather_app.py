# Author:      Gleb Ignatski (gignatski@gmail.com)

# References
# https://www.geeksforgeeks.org/python-tkinter-text-widget/
# https://stackoverflow.com/questions/50581309/tkinter-clear-text-widget
# https://www.askpython.com/python/examples/display-images-using-python
# https://www.programiz.com/python-programming/datetime/current-datetime#:~:text=Get%20the%20current%20date%20and,class%20of%20the%20datetime%20module.&text=Here%2C%20we%20have%20used%20datetime,and%20time%20in%20another%20format.
# https://stackoverflow.com/questions/67031013/how-to-get-time-by-timezone-that-gives-in-openwathermap-api-response-python

import requests
import json
import datetime
from tkinter import *
import sys
import cv2

root = Tk()
root.geometry("800x800")
root.title("Weather Application")

# ------------------------Personal API key and Base URL for OpenWeatherMap Server------------------------
api_key = "" # enter your API key 
base_url = "http://api.openweathermap.org/data/2.5/weather?"

while True:

    # ------------------------Prompt the user for the city------------------------
    def user_entry():
        city_name = inputtxt.get("1.0", "end-1c")
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()

        if x["cod"] != "404":
            y = x["main"]

            # ------------------------Gather weather content from JSON------------------------
            current_temperature = y["temp"]
            current_temperature = current_temperature - 273.15
            current_temperature = round(current_temperature, 1)
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]

            # ------------------------Produce the current datetime string denoting the local date and time------------------------
            current_timezone = x["timezone"]
            tz = datetime.timezone(datetime.timedelta(seconds=int(current_timezone)))
            current_time = datetime.datetime.now(tz = tz).strftime("%d/%m/%Y %H:%M:%S")

            # ------------------------Capitalize the city name and/or country name------------------------
            city_name = city_name[0].upper() + city_name[1:len(city_name)]

            str_list = []
            str_list = list(city_name)

            for i in range(len(str_list)):
                if str_list[i] == (" "):
                    str_list[i+1] = str_list[i+1].upper()

            city_name = ""
            for i in range(len(str_list)):
                city_name = city_name + str_list[i]

            # ------------------------Create a string that displays all relevant weather content, including the current time and name of the city capitalized------------------------
            s = "Weather in " + city_name + " (" + current_time + " local time)\n\n"
            s = s + "Temperature (in degress Celsius unit) = " + str(current_temperature) + "\n"
            s = s + "Atmospheric pressure (in hPa unit) = " + str(current_pressure) + "\n"
            s = s + "Humidity (in percentage) = " + str(current_humidity) + "\n"
            s = s + "Description = " + str(weather_description) + "\n"
            cv2.destroyAllWindows()
            Output.delete("1.0", END)
            Output.insert(END, s)

            # ------------------------Display Image according to the type of weather returned------------------------
            if "clear" in weather_description:
                img = cv2.imread("images/clear_sky.png", cv2.IMREAD_ANYCOLOR)
                width = 900
                height = 675
                dim = (width, height)
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                cv2.imshow("Clear Sky", resized)
            elif ("heavy" in weather_description and "rain" in weather_description) or "thunder" in weather_description:
                img = cv2.imread("images/heavy_rain_sky.png", cv2.IMREAD_ANYCOLOR)
                width = 900
                height = 675
                dim = (width, height)
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                cv2.imshow("Heavy Rain", resized)
            elif ("moderate" in weather_description or "light" in weather_description) and ("rain" in weather_description or "drizzle" in weather_description):
                img = cv2.imread("images/light_rain_sky.png", cv2.IMREAD_ANYCOLOR)
                width = 900
                height = 675
                dim = (width, height)
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                cv2.imshow("Light-Moderate Rain", resized)
            elif ("few" in weather_description or "scattered" in weather_description or "broken" in weather_description) and "clouds" in weather_description:
                img = cv2.imread("images/partly_cloudy_sky.png", cv2.IMREAD_ANYCOLOR)
                width = 900
                height = 675
                dim = (width, height)
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                cv2.imshow("Partly Cloudy", resized)
            elif "cloud" in weather_description:
                img = cv2.imread("images/overclouded_sky.png", cv2.IMREAD_ANYCOLOR)
                width = 900
                height = 675
                dim = (width, height)
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                cv2.imshow("Overclouded", resized)
            elif "mist" in weather_description or "haze" in weather_description:
                img = cv2.imread("images/mist_sky.png", cv2.IMREAD_ANYCOLOR)
                width = 900
                height = 675
                dim = (width, height)
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                cv2.imshow("Mist", resized)
            elif "snow" in weather_description:
                img = cv2.imread("images/snowy_sky.png", cv2.IMREAD_ANYCOLOR)
                width = 900
                height = 675
                dim = (width, height)
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                cv2.imshow("Snowfall", resized)
        else:
            s = "City " + "'" + city_name + "'" + " Not Found!\n"
            Output.delete("1.0", END)
            Output.insert(END, s)


    # ------------------------Handle display, label, and input/output windows------------------------
    l = Label(text = "Enter the 'city' or the 'city, country' for which you would like to check the weather conditions")
    inputtxt = Text(root,
                    height = 1,
                    width = 50,
                    bg = "light yellow")
     
    Output = Text(root,
                  height = 10,
                  width = 80,
                  bg = "light cyan")
     
    Display = Button(root, height = 2,
                     width = 20,
                     bg = "cyan",
                     text ="Submit",
                     command = lambda:user_entry())

    l.pack()
    inputtxt.pack()
    Display.pack()
    Output.pack()
     
    mainloop()

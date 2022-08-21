# import inky stuff
import inky
from inky import InkyWHAT

# import Pillow for image creation
import PIL
from PIL import Image, ImageDraw, ImageColor, ImageFont

# import other useful things
import datetime
import yaml
import requests
import json
from time import sleep
import logging


"""
OFFICIAL TIMELINE FOR WHAT IS SHOWN AT WHAT TIMES OF DAY

12am    2am    4am    6am    8am   10am   12pm    2pm    4pm    6pm    8pm   10pm   12am
 |      |      |      |      |      |      |      |      |      |      |      |      |
 |------|------|------|------|------|------|------|------|------|------|------|------|
 |                    |                                         |
 | Current temp       | Current temp                            | Current temp
 | Overnight low      | Today high                              | Overnight low
 | Today high         | Tomorrow high                           | Tomorrow high

Three main switches: one at 12am, one at 6am, one at 6pm
Temps and conditions update every 30 minutes

"""

WEATHER_CARD_POS_1 = (0, 90)
WEATHER_CARD_POS_2 = (135, 90)
WEATHER_CARD_POS_3 = (270, 90)


# initialize logging
logging.basicConfig(
    filename="logs/output.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)

"""
Function to draw a weather card on the provided background
Weather cards contain the following items:
    date (datetime)
    date_desc (str)
    subtitle (str)
    temp (int)
    condition_icon (PIL.Image)
Weather cards are 130px wide and 220px tall, with 5px gaps between them
"""
def draw_weather_card(
    background: PIL.Image, 
    date: datetime,
    date_desc: str,
    subtitle: str,
    temp: int,
    condition: str,
    font_path: str,
    card_pos: tuple
) -> PIL.Image:
    
    # generate the fonts we'll need
    date_font_size = 26
    date_font = ImageFont.truetype(font_path, date_font_size)

    subtitle_font_size = 18
    subtitle_font = ImageFont.truetype(font_path, subtitle_font_size)

    temp_font_size = 52
    temp_font = ImageFont.truetype(font_path, temp_font_size)


    # create a new image to represent the weather card
    weather_card = Image.new("P", (130, 210), 0)
    draw_weather_card = ImageDraw.Draw(weather_card)


    # write the given date to the weather card
    date_text = date.strftime("%b %-d")
    draw_weather_card.text(
        (65, 0),
        date_text,
        fill=1,
        anchor="mt",
        font=date_font,
    )


    # write the date description
    draw_weather_card.text(
        (65, date_font_size),
        date_desc,
        fill=1,
        anchor="mt",
        font=date_font,
    )


    # write the subtitle
    draw_weather_card.text(
        (65, 2*date_font_size+8),
        subtitle,
        fill=1,
        anchor="mt",
        font=subtitle_font,
    )


    # write the temperature
    draw_weather_card.text(
        (65, 2*date_font_size+subtitle_font_size+12),
        str(temp),
        fill=2,
        anchor="mt",
        font=temp_font,
    )


    # load the condition_icon image, based on the condition given
    try:
        with Image.open(f"icons/{condition}.png", "r") as condition_icon:
            weather_icon_pos = (25, 130)
            weather_card.paste(condition_icon, weather_icon_pos)
    except OSError as exception:
        logging.exception(f"Could not get icon: {exception}")


    # return the value that we've been modifying, the given background
    background.paste(weather_card, card_pos)
    return background


"""
Function to draw a weather banner on top of the provided background
"""
def draw_weather_banner(
    background: PIL.Image,
    date: datetime,
    date_desc: str,
    subtitle: str,
    temp: int,
    condition: str,
    font_path: str,
) -> PIL.Image:

    # generate the fonts we'll need
    date_font_size = 34
    date_font = ImageFont.truetype(font_path, date_font_size)

    subtitle_font_size = 40
    subtitle_font = ImageFont.truetype(font_path, subtitle_font_size)

    temp_font_size = 70
    temp_font = ImageFont.truetype(font_path, temp_font_size)
 
    
    # create a new image to represent the weather banner
    weather_banner = Image.new("P", (400, 85), 0)
    draw_weather_banner = ImageDraw.Draw(weather_banner)


    # write the given date to the weather banner
    date_text = date.strftime("%b %-d %I:%M")
    draw_weather_banner.text(
        (0, 0),
        date_text,
        fill=1,
        anchor="lt",
        font=date_font,
    )

    # write the given subtitle to the weather banner
    draw_weather_banner.text(
        (0, 38),
        subtitle,
        fill=1,
        anchor="lt",
        font=subtitle_font,
    )

    # write the given temperature to the weather banner
    draw_weather_banner.text(
        (260, 12),
        str(int(temp)),
        fill=2,
        anchor="mt",
        font=temp_font,
    )
 
  

    # load the condition_icon image, based on the condition given
    try:
        with Image.open(f"icons/{condition}.png", "r") as condition_icon:
            weather_icon_pos = (320, 0)
            weather_banner.paste(condition_icon, weather_icon_pos)
    except OSError as exception:
        logging.exception(f"Could not get icon: {exception}")


    background.paste(weather_banner, (0, 0))
    return background
    


def openweather_current():
    # get info from config.yml
    latitude = 0.0
    longitude = 0.0
    api_key = ""
    with open("config.yml") as config_file:
        config = yaml.full_load(config_file)
        latitude = config["latitude"]
        longitude = config["longitude"]
        api_key = config["api_key"]

    # craft the API call (current weather)
    # https://openweathermap.org/current 
    url = "https://api.openweathermap.org/data/2.5/weather?"\
        f"lat={latitude}&lon={longitude}"\
        f"&appid={api_key}&lang=en&units=imperial"

    # make the API call
    response = requests.get(url)

    # if we got a bad response, return that
    if response.status_code != 200:
        logging.error(f"OpenWeather get returned non-200: {response.status_code}, {response.text}")
        return {
            "status": response.status_code,
            "error_message": response.text,
        }
    
    # obtain the important data we want and return it
    data = response.json()
    logging.info("OpenWeather data gotten")
    return {
        "status": 200,
        "current_temp": data["main"]["temp"],
        "icon": data["weather"][0]["icon"],
    }


def noaa_forecast():
    # get the grid and office from lat and long
    latitude = 0.0
    longitude = 0.0
    with open("config.yml") as config_file:
        config = yaml.full_load(config_file)
        latitude = config["latitude"]
        longitude = config["longitude"]
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    

    response = requests.get(url)
    data = response.json()
    important_data = {
        "status_code": response.status_code,
        "forecast": data["properties"]["forecast"],
    }

    forecast_response = requests.get(important_data["forecast"])
    
    # if we get a bad response, return that
    if forecast_response.status_code != 200:
        logging.error(f"NOAA forecast get returned non-200: {forecast_response.status_code}, {forecast_response.text}")
        return {
            "status": forecast_response.status_code,
            "error_message": forecast_response.text
        }

    # obtain the important data we want and return 
    forecast_data = {
        "status": 200,
        "forecast": []
    }
    for prediction in forecast_response.json()["properties"]["periods"]:
        forecast_data["forecast"].append({
            "date_name": prediction["name"],
            "date": datetime.date.fromisoformat(prediction["startTime"][:10]),
            "temp": prediction["temperature"],
            "is_daytime": prediction["isDaytime"],
            "icon": prediction["icon"].split("/")[6].split("?")[0],
        })
    logging.info("NOAA forecast data gotten")
    return forecast_data


def get_icon(icon_name: str, daytime: bool = False) -> str:
    # using a mapping of icons I determined, get the icon name given the api's names
    if icon_name in ["skc", "01d", "few", "wind_skc", "wind_few", "hot"]:
        return "sunny" if daytime else "clear_night"
    if icon_name == "01n":
        return "clear_night"
    if icon_name in ["02d", "02n", "sct", "wind_sct"]:
        return "partly_cloudy"
    if icon_name in ["03d", "03n", "04d", "04n", "bkn", "ovc", "wind_bkn", "wind_ovc"]:
        return "cloudy"
    if icon_name in ["09d", "09n", "10d", "10n", "rain", "rain_showers", "rain_showers_hi", "tornado", "hurricane", "tropical_storm"]:
        return "rain"
    if icon_name in ["11d", "11n", "tsra", "tsra_sct", "tsra_hi"]:
        return "thunderstorm"
    if icon_name in ["13d", "13n", "snow", "rain_snow", "rain_sleet", "snow_sleet", "fzra", "rain_fzra", "snow_fzra", "sleet", "cold", "blizzard"]:
        return "snow"
    if icon_name in ["50d", "50n", "dust", "smoke", "haze", "fog"]:
        return "haze"
    logging.error(f"Icon not found icon_name: {icon_name} daytime: {daytime}")
    return "unknown" # default, cause pic to not print

def get_date_desc(today: datetime.date, date: datetime.date, daytime: bool):
    # provide the date desc ("Today", "Tngt", "Tmrw", etc)
    if today.day == date.day:
        return "Today" if daytime else "Tngt"
    if (date - today).days == 1:
        return "Tmrw"
    logging.error(f"Date description not found today: {today} date: {date} daytime: {daytime}")
    return "???"


def main():
    # inky setup
    display = InkyWHAT("red")
    
    # in a while loop, to run forever until the process is killed;
    while True:

        # create the image to write
        image = Image.new("P", (400, 300))

        # get the weather data
        current_weather = openweather_current()
        forecast_weather = noaa_forecast()
        if current_weather["status"] == 200 and forecast_weather["status"] == 200:

            todays_date = datetime.date.today()
            current_datetime = datetime.datetime.now()
            current_hour = current_datetime.time().hour

            # draw the weather banner 
            image = draw_weather_banner(
                background=image,
                date=current_datetime,
                date_desc="Today",
                subtitle="Current (F)",
                temp=current_weather["current_temp"],
                condition=get_icon(current_weather["icon"], True if current_hour >= 6 and current_hour <= 20 else False),
                font_path="fonts/Ramabhadra-Regular.ttf",
            )
    


            # draw three weather cards
            sub = "High (F)" if forecast_weather["forecast"][0]["is_daytime"] else "Low (F)"
            image = draw_weather_card(
                background=image, 
                date=forecast_weather["forecast"][0]["date"],
                date_desc=get_date_desc(todays_date, forecast_weather["forecast"][0]["date"], forecast_weather["forecast"][0]["is_daytime"]),
                subtitle=sub,
                temp=forecast_weather["forecast"][0]["temp"],
                condition=get_icon(forecast_weather["forecast"][0]["icon"], forecast_weather["forecast"][0]["is_daytime"]),
                font_path="fonts/Ramabhadra-Regular.ttf",
                card_pos=WEATHER_CARD_POS_1,
            )

            sub = "High (F)" if forecast_weather["forecast"][1]["is_daytime"] else "Low (F)"
            image = draw_weather_card(
                background=image,
                date=forecast_weather["forecast"][1]["date"],
                date_desc=get_date_desc(todays_date, forecast_weather["forecast"][1]["date"], forecast_weather["forecast"][1]["is_daytime"]),
                subtitle=sub,
                temp=forecast_weather["forecast"][1]["temp"],
                condition=get_icon(forecast_weather["forecast"][1]["icon"], forecast_weather["forecast"][1]["is_daytime"]),
                font_path="fonts/Ramabhadra-Regular.ttf",
                card_pos=WEATHER_CARD_POS_2,
            )

            sub = "High (F)" if forecast_weather["forecast"][2]["is_daytime"] else "Low (F)"
            image = draw_weather_card(
                background=image,
                date=forecast_weather["forecast"][2]["date"],
                date_desc=get_date_desc(todays_date, forecast_weather["forecast"][2]["date"], forecast_weather["forecast"][2]["is_daytime"]),
                subtitle=sub,
                temp=forecast_weather["forecast"][2]["temp"],
                condition=get_icon(forecast_weather["forecast"][2]["icon"], forecast_weather["forecast"][2]["is_daytime"]),
                font_path="fonts/Ramabhadra-Regular.ttf",
                card_pos=WEATHER_CARD_POS_3,
            )
    


            # draw the image in the correct orientation on the screen
            image = image.rotate(180)
            display.set_image(image)
            display.show()
            logging.info("New weather data drawn to display")
        
        # sleep for 10 minutes
        logging.info("Begin sleep")
        sleep(600)
        logging.info("End sleep")


if __name__ == "__main__":
    main()


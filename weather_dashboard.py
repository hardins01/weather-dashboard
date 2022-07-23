# import inky stuff
import inky
from inky import InkyWHAT

# import Pillow for image creation
import PIL
from PIL import Image, ImageDraw, ImageColor, ImageFont

# import other useful things
import datetime


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

WEATHER_CARD_POS_1 = (0, 0)
WEATHER_CARD_POS_2 = (135, 0)
WEATHER_CARD_POS_3 = (270, 0)

"""
Function to draw a weather card on the provided background
Weather cards contain the following items:
    date (datetime)
    date_desc (str)
    subtitle (str)
    temp (int)
    condition_icon (PIL.Image)
Weather cards are 130px wide and 200px tall, with 5px gaps between them
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

    temp_font_size = 55
    temp_font = ImageFont.truetype(font_path, temp_font_size)


    # create a new image to represent the weather card
    weather_card = Image.new("P", (130, 200), 0)
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
        fill=1,
        anchor="mt",
        font=temp_font,
    )


    # load the condition_icon image, based on the condition given
    with Image.open(f"icons/{condition}.png", "r") as condition_icon:
        weather_icon_pos = (25, 120)
        condition_icon.thumbnail((80, 80))
        weather_card.paste(condition_icon, weather_icon_pos)


    # return the value that we've been modifying, the given background
    background.paste(weather_card, card_pos)
    return background


def get_weather_data(location: str):
    pass

def main():
    # inky setup
    display = InkyWHAT("red")
    
    # create the image to write to the display
    image = Image.new("P", (400, 300))

    # draw three weather cards
    todays_date = datetime.datetime.now()
    
    image = draw_weather_card(
        background=image, 
        date=todays_date,
        date_desc="Today",
        subtitle="Current (F)",
        temp=current_temp,
        condition="cloudy",
        font_path="fonts/Lora-VariableFont_wght.ttf",
        card_pos=WEATHER_CARD_POS_1,
    )

    image = draw_weather_card(
        background=image,
        date=todays_date,
        date_desc="Today",
        subtitle="High (F)",
        temp=77,
        condition="cloudy",
        font_path="fonts/Lora-VariableFont_wght.ttf",
        card_pos=WEATHER_CARD_POS_2,
    )
    
    image = draw_weather_card(
        background=image,
        date=todays_date + datetime.timedelta(days=1),
        date_desc="Tmrw",
        subtitle="High (F)",
        temp=81,
        condition="cloudy",
        font_path="fonts/Lora-VariableFont_wght.ttf",
        card_pos=WEATHER_CARD_POS_3,
    )


    # draw the image in the correct orientation on the screen
    image = image.rotate(180)
    display.set_image(image)
    display.show()


if __name__ == "__main__":
    main()

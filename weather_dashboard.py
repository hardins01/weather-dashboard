# import inky stuff
import inky
from inky import InkyWHAT

# import Pillow for image creation
import PIL
from PIL import Image, ImageDraw, ImageColor, ImageFont


"""
OFFICIAL TIMELINE FOR WHAT IS SHOWN AT WHAT TIMES OF DAY

12am    2am    4am    6am    8am   10am   12pm    2pm    4pm    6pm    8pm   10pm   12am
 |      |      |      |      |      |      |      |      |      |      |      |      |
 |------|------|------|------|------|------|------|------|------|------|------|------|
 |                                                              |
 | Current temp                                                 | Current temp
 | Today (same date) high                                       | Tomorrow (next date) high
 | Tomorrow (next date) high                                    | 

Two main switches: one at 12am, one at 6pm
Temps and conditions update every 30 minutes

"""



"""
Function to draw a weather card on the provided background
Weather cards contain the following items:
    date (datetime)
    date_desc (str)
    subtitle (str)
    temp (int)
    condition (str)
    condition_icon (PIL.Image)
"""
def draw_weather_card(background: PIL.Image, condition: str):
    # load the image, based on the condition given
    with Image.open(f"icons/{condition}.png", "r") as condition_icon:
        position = (80, 80)
        condition_icon.thumbnail((150, 150))
        condition_icon.save(f"smaller_{condition}.png")
        background.paste(condition_icon, position)
    return background


def main():
    # inky setup
    display = InkyWHAT("red")
    display.set_border(display.BLACK)

    
    # test new image library
    image = Image.new("P", (400, 300))
    drawn_image = ImageDraw.Draw(image)
    
    # write some text in a downloaded font
    # font = ImageFont.truetype("fonts/Lora-VariableFont_wght.ttf", 40)
    # drawn_image.text((30, 30), "ur mom", font=font, fill=display.BLACK)
    # drawn_image.text((30, 100), "this is so sick", font=font, fill=display.RED)


    # draw a weather card
    image = draw_weather_card(image, "cloudy")


    # draw the image in the correct orientation
    image = image.rotate(180)
    display.set_image(image)
    display.show()


if __name__ == "__main__":
    main()

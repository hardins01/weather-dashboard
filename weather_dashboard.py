# import inky stuff
import inky
from inky import InkyWHAT

# import Pillow for image creation
from PIL import Image, ImageDraw, ImageColor, ImageFont

def main():
    # inky setup
    display = InkyWHAT("red")
    display.set_border(display.BLACK)

    
    # test new image library
    image = Image.new("P", (400, 300))
    drawn_image = ImageDraw.Draw(image)
    
    font = ImageFont.truetype("fonts/Lora-VariableFont_wght.ttf", 40)
    drawn_image.text((30, 30), "ur mom", font=font, fill=display.BLACK)
    drawn_image.text((30, 100), "this is so sick", font=font, fill=display.RED)

    # draw the image in the correct orientation
    image = image.rotate(180)
    display.set_image(image)
    display.show()


if __name__ == "__main__":
    main()

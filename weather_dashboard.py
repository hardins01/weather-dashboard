# import inky stuff
import inky
from inky import InkyWHAT

# import Pillow for image creation
from PIL import Image, ImageDraw, ImageColor

def main():
    # inky setup
    display = InkyWHAT("red")

    # test new image library
    Image.new("RGB", (400, 300), ImageColor.getrgb("white"))
    font = ImageFont.load("")
    



if __name__ == "__main__":
    main()

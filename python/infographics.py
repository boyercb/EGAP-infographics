import numpy
import pandas
import glob
import matplotlib.pyplot as plt
from PIL import Image

# def resize:
def resize(file, size):
    """
    Resizes image file to size.
    """
    img = Image.open(file)
    fname, ext = os.path.splitext(file)
    resized = img.resize(size)
    resized.save(fname + "_resized.png")

# def create_plot:
def create_bar_plot(data):
    """
    Creates a green/red bar plot from data.
    """
    data.plot(kind = "barh")
    plt.
    return plt

# def
def create_bar_figure(plot, img):
    """
    Merges bar plot with image for percentage variables.
    """


def create_numbered_figure(data, img):
    """
    Creates an image with a number colored by whether it's positive/negative.
    """

def create_summary_figure():
    """
    Creates the summary image colored by whether it's positive/negative.
    """

def create_infographic(title, top, mid, bot, img):
    """
    Constructs the final infographic image from components.
    """

# read data
data = pandas.read_csv('../indicators.csv')
text = pandas.read_csv('../text.csv')

# clean and organize indicators

# read and trim image files
size = (600, 400)
altsize = (1000, 800)

altnames = [ "summary_presence",
             "summary_absence",
             "school_supply2_presence",
             "school_supply2_absence" ]

for file in glob.glob('../png/*.png'):
    resize(file, size if file in altnames else altsize)

for ind in text["indicator"]:
    for obs in length(data):
        exclude = ["summary_municipality", "school_supplies_delay_municipality"]

        # infographic logic
        if ind in exclude:
            if ind == exclude[1]:
                create_numbered_figure(data, img)

            elif ind == exclude[2]:
                create_summary_figure()

            else:
                EnvironmentError

        else:
            create_bar_plot(data)
            create_bar_figure()

        canvas = (4096, 1086)
        title = text[ind, title]
        top = text[ind, title]
        mid = text[ind, mid]
        bot = text[ind, bot]

        mid = mid.replace("[v]", data[obs, ind])
        mid = mid.replace("[commune name]", data[obs, ind])
        bot = bot.replace("[X]", data[obs, ind])
        bot = bot.replace("[Y]", data[obs, ind])

        infog = create_infographic(canvas, title, top, mid, bot)

        # export

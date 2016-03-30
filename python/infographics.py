import glob
import numpy
import pandas
import matplotlib.style as sty
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

# function definitions
def resize(file, size):
    """
    Resizes image file to size.
    """
    img = Image.open(file)
    resized = img.resize(size)
    return resized

def create_text_img(text, fontfamily, fontsize, fontfill, size, fill):
    img = Image.new('RGBA', size, fill)
    font = ImageFont.truetype(fontfamily, fontsize, fontfill)
    d = ImageDraw.Draw(img)
    d.text(size, text, font)
    return img

def create_bar_plot(df):
    """
    Creates a green/red bar plot from data.
    """
    colors = ['g', 'r']
    names = df.values
    bars = df.plot(kind = "barh", color = colors)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, 0.90 * height,
            's'% (names[i]), ha = 'center', va = 'bottom')
    plt.axis('off')
    plt.canvas.draw()
    pillow = Image.frombyte('RGBA', plt.canvas.get_width_height(),
        plt.canvas.tostring_rgba())
    return pillow

def create_bar_figure(plot, img):
    """
    Merges bar plot with image for percentage variables.
    """
    canvas = Image.new('RGBA', (400, 800))
    out = Image.alpha_composite(canvas, img, plot)
    return out

def create_numbered_figure(delay, img):
    """
    Creates an image with numbered text colored by whether it's positive/negative.
    """
    canvas = Image.new('RGBA', (400, 800))
    msg = delay + "jours d'avances" if delay <= 0 else "jours de retard"
    fill = (x, x, x, x) if delay <= 0 else (x, x, x, x)
    img = create_text_img(msg, "Roboto-Bold_0.tff", 48, fill, )
    out = Image.alpha_composite(canvas, img, txt)
    return out

def create_summary_figure(img):
    """
    Creates the summary image colored by whether it's positive/negative.
    """
    canvas = (400, 800)

def create_infographic(commune, title, top, mid, bot, grob):
    """
    Constructs the final infographic image from components.
    """
    canvas = (4096, 1086)
    commune_grob = create_text_img(commune, "Roboto-Bold_0.tff")
    title_grob = create_text_img(title, "Roboto-Bold_0.tff")
    top_grob = create_text_img(top, "Roboto-Regular.tff")
    mid_grob = create_text_img(mid, "Roboto-Regular.tff")
    bot_grob = create_text_img(bot, "Roboto-Regular.tff")

    stage1 = Image.alpha_composite(commune_grob, title_grob)
    stage2 = Image.alpha_composite(stage1, top_grob)
    stage3 = Image.alpha_composite(stage2, mid_grob)
    stage4 = Image.alpha_composite(stage3, bot_grob)
    infog = Image.alpha_composite(stage4, grob)

    return infog


# read data
data = pandas.read_csv('../indicators.csv')
text = pandas.read_csv('../text.csv')

# set matplotlib plot style
sty.use('ggplot')

# clean and organize indicators

size = (600, 400)
altsize = (1000, 800)

altnames = [ "summary_presence",
             "summary_absence",
             "school_supply2_presence",
             "school_supply2_absence" ]

# read and trim image files
for file in glob.glob('../png/*.png'):
    fname, ext = os.path.splitext(file)
    resized = resize(file, size if file in altnames else altsize)
    resized.save(fname + "_resized.png")

for ind in text["indicator"]:
    for idx, row in data.iterrows():
        exclude = ["summary_municipality", "school_supplies_delay_municipality"]

        # infographic logic
        if ind in exclude:
            if ind == exclude[1]:
                delay = row[ind]
                fname = ind + '_presence.png' if delay <= 0 else '_absence.png'
                img = Image.open('../png' + fname)
                grob = create_numbered_figure(delay, img)

            elif ind == exclude[2]:
                rank = row[ind.replace("_municipality", "_performance")]
                fname = ind + '_presence.png' if rank == "PLUS" else '_absence.png'
                img = Image.open('../png' + fname)
                grob = create_summary_figure(rank, img)

            else:
                EnvironmentError

        else:
            row[ind + "_neg"] = 100 - row[ind]
            plot = create_bar_plot(row[ind, ind + "_neg"])
            img = Image.open('../png/' + ind + ".png")
            grob = create_bar_figure(plot, img)

        # fetch infographic text
        title = text[ind, "title"]
        top = text[ind, "title"]
        mid = text[ind, "mid"]
        bot = text[ind, "bot"]

        # replace place holders with values in infographic text
        mid = mid.replace("[v]", row[ind])
        mid = mid.replace("[commune name]", row[ind])
        bot = bot.replace("[X]", row[ind])
        bot = bot.replace("[Y]", row[ind])

        # construct the infographic from its components
        infog = create_infographic(title, top, mid, bot, grob)

        # export
        infog.save()

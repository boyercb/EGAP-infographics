import glob
import numpy
import pandas
import textwrap
import matplotlib.style as sty
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from progressbar import ProgressBar

# function definitions
def resize(file, size):
    """
    Resizes image file to size.
    """
    img = Image.open(file)
    fname, ext = os.path.splitext(file)
    resized = img.resize(size)
    resized.save(fname + "_resized.png")

def create_bar_plot(df):
    """
    Creates a green/red bar plot from data.
    """
    colors = ['g', 'r']
    hfont = {'fontname' : 'Roboto Bold'}

    df[df >= 99.5] = 99.5
    df[df <= 0.5] = 0.5

    names = df.values
    names = [100 if x == 99.5 else x for x in names]

    ax = df.plot.barh(color = colors)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    plt.axis('off')

    for i, bar in enumerate(ax.patches):
        ax.annotate(str(names[i]),
            (bar.get_width() - 7, bar.get_y() + bar.get_height()/2.0),
            ha = 'center', va = 'center', fontsize = 40, fontname = "Roboto", color = 'w')

    canvas = plt.get_current_fig_manager().canvas
    plt.close()
    canvas.draw()
    pillow = Image.frombytes('RGB', canvas.get_width_height(),
        canvas.tostring_rgb())
    return pillow

def create_bar_figure(plot, img1, img2):
    """
    Merges bar plot with image for percentage variables.
    """
    out = Image.new('RGB', (3000, 1500))
    rplot = plot.resize((1800, 1500))
    rimg1 = img1.resize((1200, 750))
    rimg2 = img2.resize((1200, 750))
    out.paste(rimg1, (0,0))
    out.paste(rimg2, (0, 750))
    out.paste(rplot, (1200, 0))
    return out

def create_text_img(text, fontfamily, fontsize, fontfill, size):
    img = Image.new('RGB', size, (255, 255, 255))
    font = ImageFont.truetype(fontfamily, fontsize)
    d = ImageDraw.Draw(img)
    offset = 0
    for line in textwrap.wrap(text, width = 115):
        d.text((0, offset), line, font = font, fill = fontfill)
        offset += font.getsize(line)[1]
    return img

def create_numbered_figure(delay, img):
    """
    Creates an image with numbered text colored by whether it's positive/negative.
    """
    out = Image.new('RGB', (3500, 1500))
    rimg = img.resize((2000, 1500))
    msg = ("0" if delay <= 0 else str(delay)) + " jours de retard"
    msg = " " + msg
    fill = (0, 127, 0) if delay <= 0 else (255, 0, 0)
    txt = create_text_img(msg, "Roboto-Bold_0.ttf", 120, fill, (1500, 1500))
    out.paste(rimg, (0, 0))
    out.paste(txt, (2000, 0))
    return out

def create_infographic(commune, title, top, mid, bot, fig):
    """
    Constructs the final infographic image from components.
    """
    fill = (0, 0, 0, 0)
    infog = Image.new('RGB', (4800, 3000), (255,255,255))

    grob1 = create_text_img(commune, "Roboto-Bold_0.ttf", 200, fill, (4800, 300))
    grob2 = create_text_img(title, "Roboto-Bold_0.ttf", 150, fill, (4800, 300))
    grob3 = create_text_img(top, "Roboto-Regular.ttf", 90, fill, (4800, 250))
    grob4 = create_text_img(mid, "Roboto-Regular.ttf", 90, fill, (4800, 250))
    grob5 = create_text_img(bot, "Roboto-Regular.ttf", 90, fill, (4800, 250))

    infog.paste(grob1, (0, 10))
    infog.paste(grob2, (0, 320))
    infog.paste(grob3, (0, 630))
    infog.paste(grob4, (0, 940))
    infog.paste(grob5, (0, 1250))
    infog.paste(fig, (900, 1500))
    #
    return infog

# read data
data = pandas.read_csv('../indicators.csv')
text = pandas.read_csv('../text.csv')

# set matplotlib plot style
sty.use('ggplot')

# initialize progress bar
pbar = ProgressBar(max_value = len(data.index))
exclude = ["summary_municipality", "school_supplies_delay_municipality"]

for ind in text["indicator"]:
    print("\n" + ind + ":\n")
    pbar.start()
    for idx, row in data.iterrows():
        # get indicator root
        root = ind.replace("_municipality", "")

        # substitution values
        v = row[ind]
        Y = row[root + "_ranking_below"]
        X = row["number_of_municipalities_in_region"]

        # infographic logic
        if ind in exclude:
            if ind == exclude[1]:
                fname = root + ('_presence.png' if v <= 0 else '_absence.png')
                img = Image.open('../png/' + fname)
                grob = create_numbered_figure(v, img)

            elif ind == exclude[0]:
                rank = row[ind.replace("_municipality", "_performance")]
                fname = root + ('_presence.png' if rank == "PLUS" else '_absence.png')
                img = Image.open('../png/' + fname)
                grob = img.resize((2400, 1500))

            else:
                EnvironmentError

        else:
            row[ind + "_neg"] = 100 - row[ind]
            plot = create_bar_plot(row[[ind, ind + "_neg"]])
            imga = Image.open('../png/' + root + "_absence.png")
            imgp = Image.open('../png/' + root + "_presence.png")
            grob = create_bar_figure(plot, imgp, imga)

        # fetch infographic text
        top = text[text["indicator"] == ind]["top"].values[0]
        mid = text[text["indicator"] == ind]["middle"].values[0]
        bot = text[text["indicator"] == ind]["bottom"].values[0]
        title = text[text["indicator"] == ind]["title"].values[0]
        commune = row["commune"]
        region = row["region"]


        # replace text placeholders
        # the first case is a special update for the school supplies indicator
        if v <= 0 and ind == exclude[1]:
            mid = mid.replace("avec [v] jours de retard après la rentrée.",
                "à temps pour la rentrée scolaire.")
        elif v >= 100 and ind not in exclude:
            mid = mid.replace("[v]", "près de 100")
        else:
            mid = mid.replace("[v]", str(v))

        # replace remaining place holders with values in infographic text
        mid = mid.replace("[commune name]", commune)
        bot = bot.replace("[X]", str(X))
        bot = bot.replace("[Y]", str(Y))

        # construct the infographic from its components
        infog = create_infographic(commune, title, top, mid, bot, grob)

        # export
        infog.save("../output/" + region + "_" + commune + "_" + root + ".png", "PNG")

        pbar.update(idx + 1)
    pbar.finish()

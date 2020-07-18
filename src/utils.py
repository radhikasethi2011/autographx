from pathlib import Path

import gdown
from pathlib import Path
import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import emoji
import re


def strip_emoji_and_dots(text):
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    new_text = new_text.replace("...", ". ")
    new_text = new_text.replace("...", ". ")
    new_text = new_text.replace(" . ", ". ")
    new_text = new_text.replace(" .", ". ")
    return new_text


def get_files_from_gdrive(url: str, fname: str) -> None:
    file_id = url.split("/")[3].split("?")[1]
    print(file_id)
    url = f"https://drive.google.com/uc?{file_id}"
    gdown.download(url, fname, quiet=False)


def get_autos(df, filepath="YearbookENTC", details="docs/details.csv"):
    df = pd.read_csv(details)
    df["query_name"] = df["First Name"] + df["Last Name"]
    df["query_name"] = df["query_name"].apply(lambda x: x.lower())
    df.set_index("query_name", inplace=True)
    autos = []
    filepath = Path(filepath)
    assert filepath.is_dir()
    file_list = []
    for x in filepath.iterdir():
        if x.is_dir():
            file_list.append(x)
    print(file_list)

    for f in file_list:
        details = {}
        name = str(f)[len(str(filepath)) + 1 :]
        if name in list(df.index):
            details["Name"] = (
                df.loc[name]["First Name"] + " " + df.loc[name]["Last Name"]
            )
            details["Quote"] = strip_emoji_and_dots(str(df.loc[name]["Quote for yearbook"]))
            # get_files_from_gdrive(
            #     df.loc[name]["Year Book Image"],
            #     f"src/static/{df.loc[name]['filename of your image (With extension .jpg or .png)']}",
            # )
            details["Image"] = (
                f"{df.loc[name]['filename of your image (With extension .jpg or .png)']}",
            )
            details["autographs"] = {}
        else:
            print(f"Something is wrong with {name}")
            # details["Image"] = f"unknown.png",
            continue

        for x in f.iterdir():
            if not (str(x) == f"{str(filepath)}/{name}/{name}.txt") and not (
                str(x) == f"{str(filepath)}/{name}/{name}.jpg"
                or str(x) == f"{str(filepath)}/{name}/{name}.png"
            ):

                try:
                    l = len(str(filepath)) + len(name) + 12
                    f = open(x, "r").read().replace("\n", " ").replace("\ufeff", "")
                    f = strip_emoji_and_dots(f)
                    output = split_paragraph(f, 10)
                except:
                    output = "Input Error"
                try:
                    pname = (
                        df.loc[str(x)[l:-4]]["First Name"]
                        + " "
                        + df.loc[str(x)[l:-4]]["Last Name"]
                    )
                except:
                    pname = str(x)
                    print(f"{name} : {pname}")
                details["autographs"][pname] = output
        autos.append(details)
    return autos


def get_display_img(imgpath):
    if Path(imgpath).is_file():
        return str(imgpath)
    else:
        return "unknown.png"


def add_image(autos, plt, sno):
    try:
        imgpath = autos[sno]["Image"][0]
        img = mpimg.imread(get_display_img(imgpath))
        plt.imshow(img)
    except:
        img = mpimg.imread("unknown.png")
        plt.imshow(img)
    plt.axis("off")


def add_quote(autos, plt, sno):
    try:
        output = autos[sno]["Quote"]
        output = split_paragraph(output, 4)
    except:
        output = "Wrong formatting for quote"
    plt.text(
        0.5,
        0.5,
        output,
        horizontalalignment="center",
        verticalalignment="center",
        fontdict={
            "family": "serif",
            # "color": "#f0bc81",
            "weight": "normal",
            "size": 20,
        },
    )
    try:
        title = autos[sno]["Name"]
    except:
        title = "error"
    plt.title(
        title,
        fontdict={
            "family": "serif",
            # "color": "#f0bc81",
            "weight": "normal",
            "size": 24,
        },
    )
    plt.axis("off")


def split_paragraph(para, n):
    """Returns a string that's sliced after n words.

      Input -> string, n->after n words, adding a \n.
  """
    res = para.split()
    ans = [" ".join(res[i : i + n]) for i in range(0, len(res), n)]
    return "\n".join(ans)


# autos = get_autos("YearbookENTC")
# print(autos)

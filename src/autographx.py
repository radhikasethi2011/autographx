import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path

autographs = {
    "Meghana": "Heya, this is my autograph for you",
    "Shriya": "This is another test autograph\n I hope you like it",
}


def get_autographs(pathtofile):
    """Takes input to the yearbook dir and return a dictionary of all the autographs

    Arguments:
        pathtofile {[type]} -- path to the yearbook dir

    Returns:
        [dict] -- {name : {nameofautographer : autograph}
    """

    autos = {}

    path = Path(pathtofile)
    assert path.is_dir()
    file_list = []
    for x in path.iterdir():
        if x.is_dir():
            file_list.append(x)
    print(f"Found files {len(file_list)} -- {file_list}")

    for f in file_list:
        name = str(f)[len(pathtofile) + 1 :]
        autos[name] = {}
        for x in f.iterdir():
            if str(x) == f"{pathtofile}/{name}/{name}.txt":
                info_file = x
                f = open(info_file, "r").readlines()
                info_name = f[0]
                info_quote = f[1]
            elif (
                str(x) == f"{pathtofile}/{name}/{name}.jpg"
                or str(x) == f"{pathtofile}/{name}/{name}.png"
            ):
                info_img = x
            else:
                l = len(pathtofile) + len(name) + 12
                f = open(x, "r").read().replace("\n", " ").split()
                s = []
                for i in range(0, len(f), 20):
                    s.append(" ".join(f[i : i + 20]))
                output = "\n".join(s)
                autos[name][str(x)[l:-4]] = output

    return autos


def autographs_topdf(autographs: dict, name: str) -> None:
    """Takes autographs and converts them to pdfs

    Arguments:
        autographs {dict} -- Dict of name-autograph mapping
        name {str} -- name of the person who these autographs are for
    """
    img = mpimg.imread("./cover.png")
    with PdfPages(f"{name}.pdf") as pdf:
        plt.figure(figsize=(11.69, 8.27))
        ax = plt.axes()
        ax.imshow(img)
        ax.patch.set_facecolor("black")
        plt.axis("off")
        pdf.savefig()
        plt.close()

        img = mpimg.imread("./auto.png")
        for key, value in autographs.items():
            plt.figure(figsize=(11.69, 8.27))
            plt.subplot(2, 1, 1)
            plt.imshow(img)
            plt.axis("off")

            plt.subplot(2, 1, 2)
            plt.text(
                0.5,
                0.5,
                value,
                horizontalalignment="center",
                verticalalignment="center",
            )
            plt.title(
                f"Autograph by {key}",
                fontdict={
                    "family": "serif",
                    "color": "#f0bc81",
                    "weight": "normal",
                    "size": 16,
                },
            )
            plt.axis("off")

            # plt.tight_layout()
            pdf.savefig()
            plt.close()


autos = get_autographs("YearbookENTC")
for name, autographs in autos.items():
    autographs_topdf(autographs, name)

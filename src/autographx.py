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
    # print(f"Found files {len(file_list)} -- {file_list}")

    for f in file_list:
        name = str(f)[len(pathtofile) + 1 :]
        autos[name] = {}
        for x in f.iterdir():
            if not (str(x) == f"{pathtofile}/{name}/{name}.txt") and not (
                str(x) == f"{pathtofile}/{name}/{name}.jpg"
                or str(x) == f"{pathtofile}/{name}/{name}.png"
            ):
                try:
                    l = len(pathtofile) + len(name) + 12
                    f = open(x, "r").read().replace("\n", " ").split()
                    s = []
                    for i in range(0, len(f), 10):
                        s.append(" ".join(f[i : i + 10]))
                    output = "\n".join(s)
                except:
                    output = "Input Error"
                autos[name][str(x)[l:-4]] = output

    return autos


def autographs_topdf(autos: dict, pathtofile) -> None:
    """Takes autographs and converts them to pdfs

    Arguments:
        autographs {dict} -- Dict of name-autograph mapping
        name {str} -- name of the person who these autographs are for
    """
    for name, autographs in autos.items():
        with PdfPages(f"{name}.pdf") as pdf:
            print_cover(pdf)
            print_grid(autos, pdf, pathtofile)
            print_autographs(autographs, pdf)


def print_cover(pdf):
    img = mpimg.imread("./cover.png")
    plt.figure(figsize=(10.8, 19.2))
    ax = plt.axes()
    ax.imshow(img)
    ax.patch.set_facecolor("black")
    plt.axis("off")
    pdf.savefig()
    plt.close()


def get_display_img(sname, pathtofile):
    if Path(f"{pathtofile}/{sname}/{sname}.jpg").is_file():
        return f"{pathtofile}/{sname}/{sname}.jpg"
    elif Path(f"{pathtofile}/{sname}/{sname}.png").is_file():
        return f"{pathtofile}/{sname}/{sname}.png"
    else:
        # print(f"they don't match for {sname}")
        return "unknown.png"


def print_grid(autos, pdf, pathtofile):
    all_name = list(autos.keys())
    for sname in range(0, len(all_name), 2):
        plt.figure(figsize=(10.8, 19.2))
        plt.subplot(4, 1, 1)
        try:
            img = mpimg.imread(get_display_img(all_name[sname], pathtofile))
            plt.imshow(img)
        except:
            img = mpimg.imread("unknown.png")
            plt.imshow(img)
        plt.axis("off")

        plt.subplot(4, 1, 2)
        try:
            value = (
                open(f"{pathtofile}/{all_name[sname]}/{all_name[sname]}.txt")
                .readlines()[1]
                .split()
            )
            s = []
            for i in range(0, len(value), 5):
                s.append(" ".join(value[i : i + 5]))
            output = "\n".join(s)
        except:
            output = "Wrong formatting"
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

        plt.title(
            f"{all_name[sname]}",
            fontdict={
                "family": "serif",
                # "color": "#f0bc81",
                "weight": "normal",
                "size": 24,
            },
        )
        plt.axis("off")

        plt.subplot(4, 1, 3)
        try:
            img = mpimg.imread(get_display_img(all_name[sname + 1], pathtofile))
            plt.imshow(img)
        except:
            img = mpimg.imread("unknown.png")
            plt.imshow(img)
        plt.axis("off")

        plt.subplot(4, 1, 4)
        try:
            value = (
                open(f"{pathtofile}/{all_name[sname+1]}/{all_name[sname+1]}.txt")
                .readlines()[1]
                .split()
            )
            s = []
            for i in range(0, len(value), 5):
                s.append(" ".join(value[i : i + 5]))
            output = "\n".join(s)
        except:
            output = "Wrong formatting"
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

        plt.title(
            f"{all_name[sname+1]}",
            fontdict={
                "family": "serif",
                # "color": "#f0bc81",
                "weight": "normal",
                "size": 24,
            },
        )
        plt.axis("off")
        pdf.savefig()
        plt.close()


def print_autographs(autographs, pdf):
    img = mpimg.imread("./auto.png")
    for key, value in autographs.items():
        plt.figure(figsize=(10.8, 19.2))
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
            fontdict={
                "family": "serif",
                # "color": "#f0bc81",
                "weight": "normal",
                "size": 20,
            },
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

autographs_topdf(autos, "YearbookENTC")

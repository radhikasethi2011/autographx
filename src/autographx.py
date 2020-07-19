import datetime
from pathlib import Path
import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from os.path import dirname, abspath
from tqdm import tqdm
from utils import add_image, add_quote, get_autos, get_display_img, split_paragraph
import warnings
warnings.filterwarnings("ignore")

def autographs_topdf(autos: list) -> None:
    """Takes autographs and converts them to pdfs

    Arguments:
        autographs {dict} -- Dict of name-autograph mapping
        name {str} -- name of the person who these autographs are for
    """
    for person in tqdm(autos):
        with PdfPages(f"{person['Name']}.pdf") as pdf:
            print_cover(pdf)
            print_grid(autos, pdf)
            print_autographs(person["autographs"], pdf)


def print_cover(pdf):
    img = mpimg.imread("./cover.png")
    plt.figure(figsize=(10.8, 19.2))
    ax = plt.axes()
    ax.imshow(img)
    ax.patch.set_facecolor("black")
    plt.axis("off")
    pdf.savefig()
    plt.close()


def print_grid(autos, pdf):
    for sno in range(0, len(autos), 4):
        plt.figure(figsize=(10.8, 19.2))
        plt.subplot(4, 2, 1)
        add_image(autos, plt, sno)

        plt.subplot(4, 2, 3)
        add_quote(autos, plt, sno)

        plt.subplot(4, 2, 2)
        add_image(autos, plt, sno + 1)

        plt.subplot(4, 2, 4)
        add_quote(autos, plt, sno + 1)

        plt.subplot(4, 2, 5)
        add_image(autos, plt, sno + 2)

        plt.subplot(4, 2, 7)
        add_quote(autos, plt, sno + 2)

        plt.subplot(4, 2, 6)
        add_image(autos, plt, sno + 3)

        plt.subplot(4, 2, 8)
        add_quote(autos, plt, sno + 3)

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


autos = get_autos("YearbookENTC", download_image=False)
autographs_topdf(autos)

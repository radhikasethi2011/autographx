import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

autographs = {
    "Meghana": "Heya, this is my autograph for you",
    "Shriya": "This is another test autograph\n I hope you like it",
}


def autographs_topdf(autographs: dict, name: str) -> None:
    """Takes autographs and converts them to pdfs

    Arguments:
        autographs {dict} -- Dict of name-autograph mapping
        name {str} -- name of the person who these autographs are for
    """
    img = mpimg.imread("./cover.png")
    with PdfPages(f"{name}.pdf") as pdf:
        ax = plt.axes()
        ax.imshow(img)
        ax.patch.set_facecolor('black')
        plt.axis("off")
        pdf.savefig()
        plt.close()

        img = mpimg.imread("./auto.png")
        for key, value in autographs.items():
            # plt.figure(figsize=(11.69,8.27))
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

            plt.tight_layout()
            pdf.savefig()
            plt.close()


autographs_topdf(autographs, "testname")

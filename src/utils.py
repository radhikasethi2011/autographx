import os
import re
import typing
from pathlib import Path

import gdown
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from tqdm import tqdm

import docx2txt
import emoji


def clean_text(text: str) ->str:
    """
    clean the non ascii characters from the complete autograph text
    remove og's quote & name
    """
    string_with_nonASCII = text
    encoded_string = string_with_nonASCII.encode("ascii", "ignore")
    decode_string = encoded_string.decode()
    return decode_string

def strip_emoji_and_dots(text: str) -> str:
    """The files have a lot of emojies, and it causes errors. 
    Currently removing emojies and ... because they cause the 
    sentence to grow longer
    Args:
        text (str): input text
    Returns:
        str: de-emojised text
    """
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    new_text = new_text.replace("...", ". ")
    new_text = new_text.replace("...", ". ")
    new_text = new_text.replace(" . ", ". ")
    new_text = new_text.replace(" .", ". ")
    new_text = new_text.replace("\ufeff", "")
    new_text = new_text.replace("\n", " ")
    new_text = new_text.replace("'", "")
    new_text = new_text.replace(" '", "")
    new_text = new_text.replace("' ", "")
    new_text = new_text.replace(" ' ", "")
    new_text1 = clean_text(new_text)
    return new_text1


def get_files_from_gdrive(url: str, fname: str) -> None:
    """downloads file from gdrive
    Args:
        url (str): gdrive url
        fname (str): name of the file
    """
    file_id = url.split("/")[3].split("?")[1]
    url = f"https://drive.google.com/uc?{file_id}"
    gdown.download(url, fname, quiet=True)


def get_autos(
    filepath: str = "YearbookENTC",
    details_file: str = "docs/details.csv",
    download_image: bool = True,
) -> list:
    """Returns a list of dictionaries of autographs for each person.
    Args:
        filepath (str, optional): Dir path to all the autographs. Defaults to "YearbookENTC".
        details_file (str, optional): details for name and quotes and photos Defaults to "docs/details.csv".
        download_image (bool, optional): do you want to download the images again. Defaults to True.
    Returns:
        dict: autos dict
    """
    df = clean_details(details_file)

    autos = []
    filepath = Path(filepath)
    file_list = file_list_from_dir(filepath)


    for f in tqdm(file_list):

        details = {}
        name = str(f)[len(str(filepath)) + 1 :]
        if name in list(df.index):
            details["Name"] = extract_full_name(df, name)
            details["Quote"] = extract_quote(df, name)
            yearbook_image = df.loc[name]["Year Book Image"]
            yearbook_image_filename = f"src/static/{df.loc[name]['filename of your image (With extension .jpg or .png)']}"
            if download_image:

                get_files_from_gdrive(yearbook_image, yearbook_image_filename)
            details["Image"] = yearbook_image_filename
            details["flask_image"] = f"{df.loc[name]['filename of your image (With extension .jpg or .png)']}"
            details["autographs"] = {}
        else:
            # print(f"something is wrong with {name}")
            continue

        for x in f.iterdir():
           
            path_to_persons_files = f"{str(filepath)}\{name}\{name}"
            if not (str(x) == f"{path_to_persons_files}.txt") and not (
                str(x) == f"{path_to_persons_files}.jpg"
                or str(x) == f"{path_to_persons_files}.png"
            ):
                output, pname = extract_autographs_and_pname(filepath, name, x, df)
                #if()
          

                details["autographs"][pname] = output
        autos.append(details)
    return autos


def extract_quote(df: pd.DataFrame, name: str) -> str:
    """Extracts the quote of the person from dataframe
    Args:
        df (pd.DataFrame): details dataframe
        name (str): the person's name who's quote you're querying
    Returns:
        str: the yearbook quote of the person
    """
    return strip_emoji_and_dots(str(df.loc[name]["Quote for yearbook"]))


def extract_full_name(df: str, name: str) -> str:
    """Based on the queryname returns full name with space.
    Args:
        df (pd.DataFrame): details dataframe
        name (str): the person's name who's quote you're querying
    Returns:
        str: the yearbook quote of the person
    """
    return df.loc[name]["First Name"] + " " + df.loc[name]["Last Name"]


def extract_autographs_and_pname(filepath, name, x, df):
    """extracts autographs from folder and the name of the person writing the autograph
    Args:
        filepath : path to the main dir where all autograph dirs are there
        name : queryname of the person
        x : Pathlib file to the file in concern
        df : details dataframe
    Returns:
        output : the autogaph of person
        pname : name of the person who wrote that autograph
    """
    try:
        f = check_for_txt_docx(x)
        f = strip_emoji_and_dots(f)
        output = split_paragraph(f, 10)
    except:
        output = "input error due to try block 1"
        try:
            f = docx2txt.process(x)
            f = strip_emoji_and_dots(f)
            output = split_paragraph(f, 10)
        except:
            output = "Input Error due to try block 2"
            # print(f"Input Error for {name}")
            # print(f"Input Error file name {str(x)}")
    try:
        l = len(str(filepath)) + len(name) + 2
        if str(x).lower()[l : l + 9] == "autograph":
            pname = extract_name(x, df, l)
        pname = extract_full_name(df, str(x)[l + 10 : -4])
    except:
        pname = f"{str(x)[l+10:-4]}\n"
    return output, pname


def extract_name(x, df, l):
    """[summary]
    Args:
        x : Pathlib file to the file in concern
        df : details datafame
        l : length of the string till "autograph" begins
    Returns:
        str: name of the peron (firstname lastname)
    """
    if str(x)[-4:] == ".txt":
        pname = extract_full_name(df, str(x)[l + 10 : -4])
    elif str(x)[-9:] == ".txt.docx":
        pname = extract_full_name(df, str(x)[l + 10 : -9])
    elif str(x)[-4:] == "docx":
        pname = extract_full_name(df, str(x)[l + 10 : -5])
    elif str(x)[-4:] == "gdoc":
        pname = extract_full_name(df, str(x)[l + 10 : -5])
    elif str(x)[-9:] == ".txt.gdoc":
        pname = extract_full_name(df, str(x)[l + 10 : -9])
    elif str(x)[-5:] == "..txt":    
        pname = extract_full_name(df, str(x)[l + 10 : -5])
    
    return pname


def check_for_txt_docx(x):
    if str(x)[-4:] == "docx":
        f = docx2txt.process(str(x))
    elif str(x)[-4:] == ".txt":
        f = open(x, "r").read()
    return f


def file_list_from_dir(filepath):
    assert filepath.is_dir()
    file_list = []
    for x in filepath.iterdir():
        if x.is_dir():
            file_list.append(x)
    return file_list


def clean_details(details_file):
    df = pd.read_csv(details_file)
    df["query_name"] = df["First Name"] + df["Last Name"]
    df["query_name"] = df["query_name"].apply(lambda x: x.lower())
    df.set_index("query_name", inplace=True)
    return df


def get_display_img(imgpath):
    if Path(imgpath).is_file():
        return str(imgpath)
    else:
        return "unknown.png"


def add_image(autos, plt, sno):
    try:
        imgpath = autos[sno]["Image"]
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
import unicodedata

from string import ascii_lowercase
from numpy import logical_not
import pandas as pd
import pyperclip
from fuzzyfinder import fuzzyfinder
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.validation import ValidationError, Validator

df = pd.read_csv("UnicodeData.txt", sep=";", header=None)
df = df[[0, 1]]
df = df.rename(columns={0: "code", 1: "name"})
df = df[["name", "code"]]
df["char"] = [chr(int(c, 16)) for c in df["code"]]
df["cat"] = [unicodedata.category(v) for v in df["char"]]
df["bidic"] = [unicodedata.bidirectional(v) for v in df["char"]]
df["name"] = [name.lower() for name in df["name"]]
df["sorted_name"] = [" ".join(sorted(name.split(" "))) for name in df["name"]]

df = df[df["cat"] != "Cc"]
df = df[df["cat"] != "Cf"]

alphabets = pd.read_csv("alphabets.csv", header=None)
alphabets = [alphabets.iloc[i].values[0].lower() for i in range(alphabets.shape[0])]
alphabets = [a for a in alphabets if a not in ["latin", "greek"]]


# ishape = df[df["name"].str.contains("modifier")].shape[0]
for alphabet in alphabets:
    if alphabet == "modi":
        alphabet += " "
    df = df[logical_not(df["name"].str.startswith(alphabet))]
    # if df[df["name"].str.contains("modifier")].shape[0] < ishape:
    #     print(alphabet)
    #     breakpoint()
    #     ishape = df[df["name"].str.contains("modifier")].shape[0]
    #     pass

df = df[logical_not(df["name"].str.startswith("variation"))]
df = df[logical_not(df["name"].str.startswith("tag"))]
df = df[logical_not(df["name"].str.contains("cjk"))]
df = df[logical_not(df["name"].str.contains("xiangqi"))]
df = df[logical_not(df["name"].str.contains("<plane"))]
df = df[logical_not(df["name"].str.contains("canadian"))]
df = df[logical_not(df["name"].str.contains("braille"))]
df = df[logical_not(df["name"].str.contains("ethiopic"))]
df = df[logical_not(df["name"].str.contains("kangxi"))]
df = df[logical_not(df["name"].str.contains("ideographic"))]
df = df[logical_not(df["name"].str.contains("japanese"))]
df = df[logical_not(df["name"].str.contains("ideographic"))]
df = df[logical_not(df["name"].str.contains("hiragana"))]
df = df[logical_not(df["name"].str.contains("hexagram"))]
df = df[logical_not(df["name"].str.contains("yi syllable"))]
df = df[logical_not(df["name"].str.contains("old turkic"))]
df = df[logical_not(df["name"].str.contains("cuneiform"))]
df = df[logical_not(df["name"].str.contains("egyptian"))]
df = df[logical_not(df["name"].str.contains("anatolian"))]
df = df[logical_not(df["name"].str.contains("nushu"))]
df = df[logical_not(df["name"].str.contains("hentaigana"))]
df = df[logical_not(df["name"].str.contains("nyiakeng"))]
df = df[logical_not(df["name"].str.contains("katakana"))]
df = df[logical_not(df["name"].str.contains("vai syllable"))]
df = df[logical_not(df["name"].str.contains("ideogram"))]
df = df[logical_not(df["name"].str.contains("hungarian"))]
df = df[logical_not(df["name"].str.contains("zanabazar"))]
df = df[logical_not(df["name"].str.contains("bhaiksuki"))]
df = df[logical_not(df["name"].str.contains("marchen"))]
df = df[logical_not(df["name"].str.contains("tangut"))]
df = df[logical_not(df["name"].str.contains("miao"))]
df = df[logical_not(df["name"].str.contains("medefaidrin"))]
df = df[logical_not(df["name"].str.contains("masaram"))]
df = df[logical_not(df["name"].str.contains("warang"))]
df = df[logical_not(df["name"].str.contains("duployan"))]
df = df[logical_not(df["name"].str.contains("byzantine"))]
df = df[logical_not(df["name"].str.contains("signwriting"))]
df = df[logical_not(df["name"].str.contains("wancho"))]
df = df[logical_not(df["name"].str.contains("mahjong"))]
df = df[logical_not(df["name"].str.contains("alchemical"))]
df = df[logical_not(df["name"].str.contains("cyrillic"))]
df = df[logical_not(df["name"].str.contains("ogham"))]
df = df[logical_not(df["name"].str.contains("bopomofo"))]
df = df[logical_not(df["name"].str.contains("phaistos"))]
df = df[logical_not(df["name"].str.contains("osage"))]
df = df[logical_not(df["name"].str.contains("meroitic"))]
df = df[logical_not(df["name"].str.contains("inscriptional"))]
df = df[logical_not(df["name"].str.contains("hanifi"))]
df = df[logical_not(df["name"].str.contains("rumi"))]
df = df[logical_not(df["name"].str.contains("sogdian"))]
df = df[logical_not(df["name"].str.contains("elymaic"))]
df = df[logical_not(df["name"].str.contains("multani"))]
df = df[logical_not(df["name"].str.contains("dogra"))]
df = df[logical_not(df["name"].str.contains("soyombo"))]
df = df[logical_not(df["name"].str.contains("gunjala"))]
df = df[logical_not(df["name"].str.contains("makasar"))]
df = df[logical_not(df["name"].str.contains("tetragram"))]
df = df[logical_not(df["name"].str.contains("adlam"))]
df = df[logical_not(df["name"].str.contains("indic"))]
df = df[logical_not(df["name"].str.contains("domino"))]
df = df[logical_not(df["name"].str.contains("hangul"))]
df = df[logical_not(df["name"].str.contains("ideograph"))]
df = df[logical_not(df["name"].str.contains("cypriot"))]
df = df[logical_not(df["name"].str.contains("pahlavi"))]
df = df[logical_not(df["name"].str.contains("nandinagari"))]
df = df[logical_not(df["name"].str.contains("bassa"))]

df = df.reset_index(drop=True)
idx = []
for i in range(df.shape[0]):
    try:
        df.iloc[i]["char"].encode("utf8")
    except:
        idx.append(i)
df = df.iloc[list(set(range(df.shape[0])) - set(idx))]
df = df.reset_index(drop=True)

df.to_pickle("unicode_clean1.pkl", protocol=-1)

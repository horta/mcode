import unicodedata

from string import ascii_lowercase
import pandas as pd
import pyperclip
from fuzzyfinder import fuzzyfinder
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.validation import ValidationError, Validator

df = pd.read_pickle("unicode_clean1.pkl")

def append(df, values):
    cols = ["name", "code", "char", "cat", "bidic", "sorted_name"]
    d = dict(zip(cols, values))
    return df.append(d, ignore_index = True)

def _append(df, name, s):
    df0 = df[df["name"] == name]
    if df0.shape[0] == 0:
        return df
    code = df0["code"].values[0]
    ch = df0["char"].values[0]
    cat = df0["cat"].values[0]
    bidic = df0["bidic"].values[0]
    return append(df, [s, code, ch, cat, bidic, s])

numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
for i, num in enumerate(numbers):
    df0 = df[df["name"] == f"superscript {num}"]
    code = df0["code"].values[0]
    ch = df0["char"].values[0]
    cat = df0["cat"].values[0]
    bidic = df0["bidic"].values[0]
    df = append(df, [f"^{i}", code, ch, cat, bidic, f"^{i}"])

for i, num in enumerate(numbers):
    df0 = df[df["name"] == f"subscript {num}"]
    code = df0["code"].values[0]
    ch = df0["char"].values[0]
    cat = df0["cat"].values[0]
    bidic = df0["bidic"].values[0]
    df = append(df, [f"_{i}", code, ch, cat, bidic, f"_{i}"])

names = ["superscript left parenthesis", "superscript right parenthesis",
         "superscript minus", "superscript plus sign", "superscript equals sign"]
shortcut = ["^(", "^)", "^-", "^+", "^="]

for i, name in enumerate(names):
    df0 = df[df["name"] == name]
    code = df0["code"].values[0]
    ch = df0["char"].values[0]
    cat = df0["cat"].values[0]
    bidic = df0["bidic"].values[0]
    s = shortcut[i]
    df = append(df, [s, code, ch, cat, bidic, s])

for a in ascii_lowercase:
    name = f"superscript latin small letter {a}"
    df0 = df[df["name"] == name]
    if df0.shape[0] == 0:
        continue
    code = df0["code"].values[0]
    ch = df0["char"].values[0]
    cat = df0["cat"].values[0]
    bidic = df0["bidic"].values[0]
    df = append(df, [f"^{a}", code, ch, cat, bidic, f"^{a}"])

names = ["subscript left parenthesis", "subscript right parenthesis",
         "subscript minus", "subscript plus sign", "subscript equals sign"]
shortcut = ["_(", "_)", "_-", "_+", "_="]

for i, name in enumerate(names):
    df0 = df[df["name"] == name]
    code = df0["code"].values[0]
    ch = df0["char"].values[0]
    cat = df0["cat"].values[0]
    bidic = df0["bidic"].values[0]
    s = shortcut[i]
    df = append(df, [s, code, ch, cat, bidic, s])
    
for a in ascii_lowercase:
    name = f"latin subscript small letter {a}"
    df0 = df[df["name"] == name]
    if df0.shape[0] == 0:
        continue
    code = df0["code"].values[0]
    ch = df0["char"].values[0]
    cat = df0["cat"].values[0]
    bidic = df0["bidic"].values[0]
    df = append(df, [f"_{a}", code, ch, cat, bidic, f"_{a}"])

greek = pd.read_csv("notebook/greek.csv", header=None)
for name in greek[0]:
    print(name)
    df = _append(df, f"mathematical italic small {name}", "\\" + name)
    df = _append(df, f"mathematical bold small {name}", "\\boldsymbol \\" + name)

# df = _append(df, "mathematical italic small alpha", r"\alpha")
# df = _append(df, "mathematical bold small alpha", r"\boldsymbol \alpha")
# df = _append(df, "mathematical italic small beta", r"\beta")
# df = _append(df, "mathematical bold small beta", r"\boldsymbol \beta")
# df = _append(df, "mathematical italic small delta", r"\delta")

df = _append(df, "modifier letter capital t", r"^T")
df = _append(df, "circled times", r"\otimes")
df = _append(df, "multiplication sign", r"\times")
df = _append(df, "dot operator", r"\cdot")
df = _append(df, "tilde operator", r"\sim")
df = _append(df, "mathematical bold script capital n", r"\mathcal N")
df = _append(df, "mathematical bold digit zero", r"\boldsymbol 0")

_collection = list(zip(df.index.to_list(), df["sorted_name"].to_list()))
_names = set(df["name"].to_list())


class MyCustomCompleter(Completer):
    def get_completions(self, document, _):
        txt = document.current_line.strip()

        words = txt.split(" ")
        words = list(set(words))
        words = sorted(words)
        txt = " ".join(words)

        pos = document.cursor_position
        suggestions = fuzzyfinder(txt, _collection, accessor=lambda x: x[1])
        for s in suggestions:
            idx = s[0]
            symbol = df.loc[idx]["char"]
            name = df.loc[idx]["name"]
            display = symbol + ": " + name
            yield Completion(name, start_position=-pos, display=display)


class NameValidator(Validator):
    def validate(self, document):
        if document.text.lower() not in _names:
            raise ValidationError(message="Not an unicode name.", cursor_position=0)


while True:

    text = prompt(
        "> ",
        completer=MyCustomCompleter(),
        complete_in_thread=True,
        complete_while_typing=True,
        validator=NameValidator(),
    )

    text = text.lower()
    symbol = df[df["name"] == text]["char"].values[0]
    pyperclip.copy(symbol)
    print(symbol)

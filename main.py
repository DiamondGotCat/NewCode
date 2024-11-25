import random
from math import gcd
from rich import print
from rich.prompt import Prompt
from rich.console import Console

# NewCodeの文字セット
CHARSET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
BASE = len(CHARSET)

def int_to_crypttext(num):
    """整数をNewCode形式に変換する関数"""
    if num == 0:
        return CHARSET[0]
    chars = []
    while num > 0:
        num, rem = divmod(num, BASE)
        chars.append(CHARSET[rem])
    # 4文字ごとに「-」を挿入。
    return '-'.join([''.join(chars[i:i+4]) for i in range(0, len(chars), 4)])

def crypttext_to_int(crypttext):
    """NewCode形式を整数に変換する関数"""
    crypttext = crypttext.replace('-', '')
    return sum(CHARSET.index(c) * (BASE ** i) for i, c in enumerate(reversed(crypttext)))

if __name__ == "__main__":
    mode = Prompt.ask("MODE", choices=["encode", "decode"])
    if mode == "encode":
        type = Prompt.ask("TYPE", choices=["number", "text"])
        if type == "number":
            num = int(Prompt.ask("NUMBER"))
            print(int_to_crypttext(num))
        elif type == "text":
            text = int.from_bytes(Prompt.ask("TEXT").encode('utf-8'), byteorder='big')
            print(int_to_crypttext(text))
    elif mode == "decode":
        crypttext = Prompt.ask("CRYPTTEXT")
        print(crypttext_to_int(crypttext))

#!/usr/bin/env python3
# newcode.py

import argparse
import sys

# Define the character set and base
CHARSET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
BASE = len(CHARSET)  # 34

def int_to_crypttext(num):
    """
    Convert an integer to a NewCode string.
    
    Args:
        num (int): The integer to convert.
    
    Returns:
        str: The NewCode string.
    """
    if num == 0:
        return CHARSET[0]
    
    chars = []
    while num > 0:
        rem = num % BASE
        chars.append(CHARSET[rem])
        num = num // BASE
    
    # Group into 4-character segments from least significant first, reverse each group
    grouped = []
    for i in range(0, len(chars), 4):
        group = ''.join(chars[i:i+4][::-1])  # Reverse each group
        grouped.append(group)
    return '-'.join(grouped)

def crypttext_to_int(crypttext):
    """
    Convert a NewCode string to an integer.
    
    Args:
        crypttext (str): The NewCode string.
    
    Returns:
        int: The corresponding integer.
    
    Raises:
        ValueError: If the crypttext contains invalid characters.
    """
    clean_text = crypttext.replace('-', '').upper()
    num = 0
    for char in clean_text:
        if char not in CHARSET:
            raise ValueError(f"Invalid character: {char}")
        index = CHARSET.index(char)
        num = num * BASE + index
    return num

def text_to_int(text):
    """
    Convert text to an integer by interpreting each character as its ASCII value.
    
    Args:
        text (str): The text to convert.
    
    Returns:
        int: The corresponding integer.
    """
    num = 0
    for char in text:
        num = (num << 8) + ord(char)
    return num

def encode_number(input_num):
    """
    Encode a number into NewCode.
    
    Args:
        input_num (str): The number as a string.
    
    Returns:
        str: The NewCode string.
    
    Raises:
        ValueError: If the input is not a valid integer.
    """
    try:
        num = int(input_num)
        if num < 0:
            raise ValueError("Number must be non-negative.")
    except ValueError as ve:
        raise ValueError(f"Invalid number: {ve}")
    
    return int_to_crypttext(num)

def encode_text(input_text):
    """
    Encode text into NewCode.
    
    Args:
        input_text (str): The text to encode.
    
    Returns:
        str: The NewCode string.
    """
    num = text_to_int(input_text)
    return int_to_crypttext(num)

def decode_crypttext(input_crypttext):
    """
    Decode a NewCode string back into a number.
    
    Args:
        input_crypttext (str): The NewCode string.
    
    Returns:
        int: The decoded number.
    """
    return crypttext_to_int(input_crypttext)

def main():
    parser = argparse.ArgumentParser(
        description="NewCode Encoder/Decoder",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands: encode or decode')
    
    # Encode subparser
    encode_parser = subparsers.add_parser('encode', help='Encode a number or text into NewCode')
    encode_parser.add_argument('--type', choices=['number', 'text'], required=True, help='Type to encode: number or text')
    encode_parser.add_argument('--input', required=True, help='Input value to encode')
    
    # Decode subparser
    decode_parser = subparsers.add_parser('decode', help='Decode a NewCode string back into a number')
    decode_parser.add_argument('--input', required=True, help='NewCode string to decode')
    
    args = parser.parse_args()
    
    if args.command == 'encode':
        if args.type == 'number':
            try:
                result = encode_number(args.input)
                print(f"Encoded NewCode: {result}")
            except ValueError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        elif args.type == 'text':
            result = encode_text(args.input)
            print(f"Encoded NewCode: {result}")
        else:
            print("Invalid encode type. Use 'number' or 'text'.", file=sys.stderr)
            sys.exit(1)
    elif args.command == 'decode':
        try:
            result = decode_crypttext(args.input)
            print(f"Decoded Number: {result}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()

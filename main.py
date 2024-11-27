#!/usr/bin/env python3
# newcode.py

import argparse
import sys
import os

# Define the character set and base
CHARSET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
BASE = len(CHARSET)  # 32

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
    
    # Reverse to make most significant digits first
    chars = chars[::-1]
    
    # Group into 4-character segments from most significant first, pad with 'A's
    grouped = []
    for i in range(0, len(chars), 4):
        group = ''.join(chars[i:i+4])
        if len(group) < 4:
            group = group.ljust(4, 'A')  # Pad with 'A's to make 4 characters
        grouped.append(group)
    
    # Reverse each group for better readability
    grouped = [group[::-1] for group in grouped]
    
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
    groups = crypttext.upper().split('-')
    reversed_chars = []
    for group in groups:
        # Reverse each group back to original order
        reversed_group = group[::-1]
        reversed_chars.extend(reversed_group)
    
    # Convert list to string
    digit_str = ''.join(reversed_chars)
    
    # Remove trailing 'A's used for padding
    digit_str = digit_str.rstrip('A')
    
    num = 0
    for char in digit_str:
        if char not in CHARSET:
            raise ValueError(f"Invalid character: {char}")
        index = CHARSET.index(char)
        num = num * BASE + index
    return num

def text_to_int(text):
    """
    Convert text to an integer by encoding it in UTF-8 and interpreting as bytes.
    
    Args:
        text (str): The text to convert.
    
    Returns:
        int: The corresponding integer.
    """
    utf8_bytes = text.encode('utf-8')
    num = 0
    for byte in utf8_bytes:
        num = (num << 8) + byte
    return num

def int_to_text(num):
    """
    Convert an integer back to text by interpreting it as UTF-8 bytes.
    
    Args:
        num (int): The integer to convert.
    
    Returns:
        str: The corresponding text.
    
    Raises:
        ValueError: If the integer cannot be decoded as UTF-8.
    """
    if num == 0:
        return '\x00'
    bytes_list = []
    while num > 0:
        bytes_list.append(num & 0xFF)
        num = num >> 8
    bytes_list.reverse()
    try:
        return bytes(bytes_list).decode('utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"Decoded bytes are not valid UTF-8: {e}")

def file_to_int(file_path):
    """
    Convert a file's binary content to an integer.
    
    Args:
        file_path (str): Path to the input file.
    
    Returns:
        int: The corresponding integer.
    
    Raises:
        IOError: If the file cannot be read.
    """
    try:
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
        num = 0
        for byte in file_bytes:
            num = (num << 8) + byte
        return num
    except Exception as e:
        raise IOError(f"Failed to read file '{file_path}': {e}")

def int_to_file(num, file_path):
    """
    Convert an integer to binary data and write to a file.
    
    Args:
        num (int): The integer to convert.
        file_path (str): Path to the output file.
    
    Raises:
        IOError: If the file cannot be written.
    """
    if num == 0:
        bytes_list = [0]
    else:
        bytes_list = []
        while num > 0:
            bytes_list.append(num & 0xFF)
            num = num >> 8
        bytes_list.reverse()
    try:
        with open(file_path, 'wb') as f:
            f.write(bytes(bytes_list))
    except Exception as e:
        raise IOError(f"Failed to write to file '{file_path}': {e}")

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

def encode_file(input_file_path):
    """
    Encode a file into NewCode.
    
    Args:
        input_file_path (str): Path to the input file.
    
    Returns:
        str: The NewCode string.
    
    Raises:
        IOError: If the file cannot be read.
    """
    num = file_to_int(input_file_path)
    return int_to_crypttext(num)

def decode_to_number(input_crypttext):
    """
    Decode a NewCode string back into a number.
    
    Args:
        input_crypttext (str): The NewCode string.
    
    Returns:
        int: The decoded number.
    """
    return crypttext_to_int(input_crypttext)

def decode_to_text(input_crypttext):
    """
    Decode a NewCode string back into text.
    
    Args:
        input_crypttext (str): The NewCode string.
    
    Returns:
        str: The decoded text.
    """
    num = crypttext_to_int(input_crypttext)
    return int_to_text(num)

def decode_to_file(input_crypttext, output_file_path):
    """
    Decode a NewCode string back into a file.
    
    Args:
        input_crypttext (str): The NewCode string.
        output_file_path (str): Path to the output file.
    
    Raises:
        IOError: If the file cannot be written.
    """
    num = crypttext_to_int(input_crypttext)
    int_to_file(num, output_file_path)

def main():
    parser = argparse.ArgumentParser(
        description="NewCode Encoder/Decoder",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands: encode or decode')
    
    # Encode subparser
    encode_parser = subparsers.add_parser('encode', help='Encode a number, text, or file into NewCode')
    encode_parser.add_argument('--type', choices=['number', 'text', 'file'], required=True, help='Type to encode: number, text, or file')
    encode_parser.add_argument('--input', required=True, help='Input value to encode (for file type, provide file path)')
    
    # Decode subparser
    decode_parser = subparsers.add_parser('decode', help='Decode a NewCode string back into a number, text, or file')
    decode_parser.add_argument('--output', choices=['number', 'text', 'file'], default='number', help='Type to decode to: number, text, or file (default: number)')
    decode_parser.add_argument('--input', required=True, help='NewCode string to decode')
    decode_parser.add_argument('--output-file', help='Output file path (required if decoding to file)')
    
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
            try:
                result = encode_text(args.input)
                print(f"Encoded NewCode: {result}")
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        elif args.type == 'file':
            if not os.path.isfile(args.input):
                print(f"Error: File '{args.input}' does not exist.", file=sys.stderr)
                sys.exit(1)
            try:
                result = encode_file(args.input)
                print(f"Encoded NewCode: {result}")
            except IOError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print("Invalid encode type. Use 'number', 'text', or 'file'.", file=sys.stderr)
            sys.exit(1)
    elif args.command == 'decode':
        if args.output == 'number':
            try:
                result = decode_to_number(args.input)
                print(f"Decoded Number: {result}")
            except ValueError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        elif args.output == 'text':
            try:
                result = decode_to_text(args.input)
                print(f"Decoded Text: {result}")
            except ValueError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        elif args.output == 'file':
            if not args.output_file:
                print("Error: '--output-file' is required when decoding to file.", file=sys.stderr)
                sys.exit(1)
            try:
                decode_to_file(args.input, args.output_file)
                print(f"Decoded file has been saved to '{args.output_file}'")
            except IOError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print("Invalid decode output type. Use 'number', 'text', or 'file'.", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import shutil
import os
from pathlib import Path
import argparse
from getpass import getpass
from stegpy import lsb 

def main():
    parser = argparse.ArgumentParser(
        description="Simple steganography program based on the LSB method."
    )
    parser.add_argument(
        "a", help="file or message to encode (if none, will read host)", nargs="?"
    )
    parser.add_argument("b", help="host file")
    parser.add_argument(
        "c", help="output file", nargs="?"
    )
    parser.add_argument(
        "-p",
        "--password",
        help="set password to encrypt or decrypt a hidden file",
        nargs="?",
    )
    parser.add_argument(
        "-b",
        "--bits",
        help="number of bits per byte (default is 2)",
        nargs="?",
        default=2,
        choices=["1", "2", "4"],
    )
    args = parser.parse_args()

    bits = int(args.bits)
    tmp_path = os.path.join(os.getcwd(), "tmp")
    host_file = os.path.abspath(args.b)
    if(not os.path.exists(tmp_path)):
        os.mkdir(tmp_path)
    tmp_host_file = os.path.join(tmp_path, os.path.basename(host_file))
    shutil.copy(host_file, tmp_host_file)

    if(args.a):
        if(not args.c):
            raise("Please provide output path")
        if(os.path.isfile(args.a)):
            input_file = os.path.abspath(args.a)
            with open(input_file, "rb") as myfile:
                message = myfile.read()
            tmp_input_file = os.path.join(tmp_path, os.path.basename(input_file))
            shutil.copy(input_file, tmp_input_file)
        else:
            input_file = None	
            message = args.a.encode("utf-8")
        output_file = os.path.abspath(args.c)
        
        os.chdir(tmp_path)
        host = lsb.HostElement(os.path.basename(host_file))
        host.insert_message(message, bits, os.path.basename(input_file) if input_file else None, args.password)
        host.save()
        shutil.copy(f"_{Path(tmp_host_file).stem}.png", output_file)
        os.remove(tmp_host_file)
        os.remove(tmp_input_file)
        os.remove(f"_{Path(tmp_host_file).stem}.png")
    else:
        host = lsb.HostElement(host_file)
        host.read_message(args.password)
        


if __name__ == "__main__":
    main()

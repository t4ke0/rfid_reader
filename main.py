#!/usr/bin/env python3

import serial

import sys

PORT = "/dev/ttyUSB0"
BOADRATE = 9600
BEGIN = bytes("\x02",("utf-8"))
END = bytes("\x03", ("utf-8"))

is_running = True

hex_to_ascii = lambda x: chr(int(x, 16))

def main():
    s = serial.Serial(PORT, BOADRATE)
    s.reset_input_buffer()

    ascii_id = ""
    parity_byte_ascii = ""

    global is_running
    while is_running:
        id_ = ""
        if (b := s.read()) == BEGIN:
            for i in range(10):
                d = s.read()
                id_ += hex(ord(d))
                if i != 9:
                    id_ += ","

            ascii_id = "".join(list(map(hex_to_ascii, id_.split(","))))

            parity_byte = ""
            count = 0
            while (r := s.read()) != END:
                parity_byte += hex(ord(r))
                if 1 & count  == 0:
                    parity_byte += ","
                count += 1

            parity_byte_ascii = "".join(list(map(hex_to_ascii, parity_byte.split(","))))

            


        s.reset_input_buffer()
        is_running = False

    print(f"ID {ascii_id}   || PARITY_BYTE {parity_byte_ascii}")
    print("Check parity byte", check_parity_bytes(ascii_id, parity_byte_ascii))
    s.close()

            

def check_parity_bytes(card_id:str, parity_byte:str) -> bool:
    hex_to_int = lambda x: int(x, 16)
    to_hex = lambda x: hex(int(x, 16))

    splitted_id = []
    fst = 0
    for index, _ in enumerate(card_id):
        if index != 0 and 1 & index == 0:
            lst = index
            splitted_id.append(card_id[fst:lst])
            fst = lst
    splitted_id.append(card_id[index-1:])

    start = 0
    l = hex_to_int(to_hex(splitted_id[start]))
    for index in range(1, len(splitted_id)):
        a = l
        if index == len(splitted_id):
            break
        b = hex_to_int(to_hex(splitted_id[index]))
        l = a ^ b

    return hex_to_int(to_hex(parity_byte)) == l
    


if __name__ == "__main__":
    main()

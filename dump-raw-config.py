#!/usr/bin/env python3
"""
Download configuration from a FlySky FS-CT6B / HK-T6A v2 transmitter
over its USB-serial link, and save it directly in the pickle format
that hkctrl.py's -u/--upload option expects.

Protocol (from https://github.com/yschaeff/HK-T6Av2):
  115200 baud, 8N1
  PC -> TX  parameter request: 55 FA 00
  TX -> PC  parameter dump:    55 FD <payload...> <checksum 2 bytes>

Usage:
  uv run ct6b_dump.py -t /dev/ttyUSB0 -o ct6b_backup.pkl
  uv run hkctrl.py -u ct6b_backup.pkl
"""
import argparse
import pickle
import sys
import time

import serial

MSGSTART = 0x55
REQ_PARAMS = 0xFA
DUMP_PARAMS = 0xFD
DUMP_MSG_LEN = 68  # length of msg[] as built by hkctrl.py's read_msg (excl MSGSTART)


def main():
    ap = argparse.ArgumentParser(description="CT6B config downloader (pickle output)")
    ap.add_argument("-t", "--tty", default="/dev/ttyUSB0", help="serial port")
    ap.add_argument("-b", "--baud", type=int, default=115200)
    ap.add_argument("-o", "--out", default="ct6b_backup.pkl", help="output pickle file")
    ap.add_argument("--timeout", type=float, default=2.0)
    ap.add_argument("--save-raw", metavar="FILE",
                     help="also save the raw serial bytes to FILE, for debugging")
    args = ap.parse_args()

    print(f"Opening {args.tty} @ {args.baud} baud...")
    ser = serial.Serial(args.tty, args.baud, timeout=args.timeout)

    # Give the OS/driver a moment, then clear any junk sitting in the buffer
    time.sleep(0.3)
    ser.reset_input_buffer()

    print("Sending parameter request (55 FA 00)...")
    ser.write(bytes([MSGSTART, REQ_PARAMS, 0x00]))
    ser.flush()

    # Read whatever comes back within the timeout window
    time.sleep(0.3)
    raw = ser.read(4096)
    ser.close()

    if not raw:
        print("No response received. Checklist:")
        print("  - Is the transmitter powered ON?")
        print("  - Does it need a button held / menu mode for 'PC connect'?")
        print("  - Try unplugging/replugging the USB cable, then re-run.")
        sys.exit(1)

    print(f"Received {len(raw)} bytes: " + " ".join(f"{b:02X}" for b in raw))

    if args.save_raw:
        with open(args.save_raw, "wb") as f:
            f.write(raw)
        print(f"Also saved raw bytes to {args.save_raw}")

    # Find the 0x55 0xFD header (mirrors read_msg's sync logic)
    idx = None
    for i in range(len(raw) - 1):
        if raw[i] == MSGSTART and raw[i + 1] == DUMP_PARAMS:
            idx = i
            break
    if idx is None:
        print("Could not find a 55 FD (param dump) header in the response.")
        print("Nothing written -- check the hex dump above.")
        sys.exit(1)

    # msg[0] = opcode (0xFD), then DUMP_MSG_LEN-1 more bytes follow
    msg = list(raw[idx + 1: idx + 1 + DUMP_MSG_LEN])
    if len(msg) < DUMP_MSG_LEN:
        print(f"Not enough bytes after header: got {len(msg)}, need {DUMP_MSG_LEN}.")
        print("Nothing written -- try again, or check the connection.")
        sys.exit(1)

    payload = msg[1:-2]  # same slice hkctrl.py uses: strip opcode + 2-byte checksum
    checksum = (msg[-2] << 8) | msg[-1]
    calc = sum(payload)
    print(f"Payload length: {len(payload)} bytes")
    print(f"Checksum in response: {checksum:#06x}  calculated: {calc:#06x}  "
          f"{'OK' if checksum == calc else 'MISMATCH -- proceed with caution'}")

    with open(args.out, "wb") as f:
        pickle.dump(payload, f)
    print(f"Wrote {args.out} -- upload with: python hkctrl.py -u {args.out}")


if __name__ == "__main__":
    main()

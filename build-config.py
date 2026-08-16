#!/usr/bin/env python3
"""
Build a complete CT6B config pickle from constants defined below.
Edit the constants, run this, then upload with hkctrl.py:

  uv run build_config.py
  uv run hkctrl.py -u ct6b_config.pkl

"""
import pickle
from message import *

OUT_FILE = "ct6b_config.pkl"

# ---------------------------------------------------------------------
# EDIT THESE. Raw values match each field's valid-range list in message.py.
# ---------------------------------------------------------------------

# --- Mode ---
TX_MODE     = 1   # 0=model1, 1=model2, 2=model3, 3=model4
CRAFT_TYPE  = 0   # 0=acro, 1=heli120, 2=heli90, 3=heli140

# --- Reverse (0=off, 1=on) ---
CH1_REVERSE = 1   # left motor
CH2_REVERSE = 1   # right motor
CH3_REVERSE = 0   # servo
CH4_REVERSE = 0
CH5_REVERSE = 0
CH6_REVERSE = 0

# --- Dual rate (0-127) ---
CH1_DR_ON   = 50
CH1_DR_OFF  = 100
CH2_DR_ON   = 50
CH2_DR_OFF  = 100
CH4_DR_ON   = 50
CH4_DR_OFF  = 100

# --- Swash AFR, heli modes only (-128 to 127) ---
CH1_SWASH = 100
CH2_SWASH = 100
CH6_SWASH = 0

# --- Endpoints / ATV (0-127) ---
CH1_END_LEFT  = 100
CH1_END_RIGHT = 100
CH2_END_LEFT  = 100
CH2_END_RIGHT = 100
CH3_END_LEFT  = 127   # forward/up
CH3_END_RIGHT = 90   # backward/down
CH4_END_LEFT  = 100
CH4_END_RIGHT = 100
CH5_END_LEFT  = 100
CH5_END_RIGHT = 100
CH6_END_LEFT  = 100
CH6_END_RIGHT = 100

# --- Throttle curve, heli modes only (0-127) ---
THRCRV_NORM = [0, 25, 50, 75, 100]   # P0..P4
THRCRV_IDLE = [100, 85, 80, 85, 100] # P0..P4

# --- Pitch curve, heli modes only (0-127) ---
PTCHCRV_NORM = [0, 25, 50, 75, 100]  # P0..P4
PTCHCRV_IDLE = [0, 25, 50, 75, 100]  # P0..P4

# --- Subtrim, signed (-128 to 127) ---
CH1_SUBTRIM = 0
CH2_SUBTRIM = 0
CH3_SUBTRIM = 0
CH4_SUBTRIM = 0
CH5_SUBTRIM = 0
CH6_SUBTRIM = 0

# --- Mixes: src/dst 0-7=CH1-CH6,VRA,VRB (dst only 0-5=CH1-CH6) ---
# switch: 0=SW A, 1=SW B, 2=On, 3=Off
MIX1_SRC, MIX1_DST, MIX1_UPR, MIX1_DWR, MIX1_SW = 0, 1, -100, -100, 2
MIX2_SRC, MIX2_DST, MIX2_UPR, MIX2_DWR, MIX2_SW = 1, 0, 100, 100, 2
MIX3_SRC, MIX3_DST, MIX3_UPR, MIX3_DWR, MIX3_SW = 0, 0, 0, 0, 3

# --- Switch/VR functions ---
# swa/swb: 0=None, 1=Dual Rate, 2=Throttle cut, 3=Normal/Idle
# vra/vrb: 0=None, 1=Pitch Adjust
SWA = 0
SWB = 0
VRA = 0
VRB = 0

# ---------------------------------------------------------------------
# Build the message and write out the pickle -- no need to edit below.
# ---------------------------------------------------------------------

def main():
    msg = [OPC_PARAM_DUMP] + [0] * 65 + [0, 0]  # checksum bytes recomputed at upload

    tx_mode.write(msg, TX_MODE)
    craft_type.write(msg, CRAFT_TYPE)

    ch1_reverse.write(msg, CH1_REVERSE)
    ch2_reverse.write(msg, CH2_REVERSE)
    ch3_reverse.write(msg, CH3_REVERSE)
    ch4_reverse.write(msg, CH4_REVERSE)
    ch5_reverse.write(msg, CH5_REVERSE)
    ch6_reverse.write(msg, CH6_REVERSE)

    ch1_dr_on.write(msg, CH1_DR_ON); ch1_dr_off.write(msg, CH1_DR_OFF)
    ch2_dr_on.write(msg, CH2_DR_ON); ch2_dr_off.write(msg, CH2_DR_OFF)
    ch4_dr_on.write(msg, CH4_DR_ON); ch4_dr_off.write(msg, CH4_DR_OFF)

    ch1_swash.write(msg, CH1_SWASH)
    ch2_swash.write(msg, CH2_SWASH)
    ch6_swash.write(msg, CH6_SWASH)

    ch1_end_left.write(msg, CH1_END_LEFT); ch1_end_right.write(msg, CH1_END_RIGHT)
    ch2_end_left.write(msg, CH2_END_LEFT); ch2_end_right.write(msg, CH2_END_RIGHT)
    ch3_end_left.write(msg, CH3_END_LEFT); ch3_end_right.write(msg, CH3_END_RIGHT)
    ch4_end_left.write(msg, CH4_END_LEFT); ch4_end_right.write(msg, CH4_END_RIGHT)
    ch5_end_left.write(msg, CH5_END_LEFT); ch5_end_right.write(msg, CH5_END_RIGHT)
    ch6_end_left.write(msg, CH6_END_LEFT); ch6_end_right.write(msg, CH6_END_RIGHT)

    for d, v in zip([thrcrv_norm_0, thrcrv_norm_1, thrcrv_norm_2, thrcrv_norm_3, thrcrv_norm_4], THRCRV_NORM):
        d.write(msg, v)
    for d, v in zip([thrcrv_idle_0, thrcrv_idle_1, thrcrv_idle_2, thrcrv_idle_3, thrcrv_idle_4], THRCRV_IDLE):
        d.write(msg, v)
    for d, v in zip([ptchcrv_norm_0, ptchcrv_norm_1, ptchcrv_norm_2, ptchcrv_norm_3, ptchcrv_norm_4], PTCHCRV_NORM):
        d.write(msg, v)
    for d, v in zip([ptchcrv_idle_0, ptchcrv_idle_1, ptchcrv_idle_2, ptchcrv_idle_3, ptchcrv_idle_4], PTCHCRV_IDLE):
        d.write(msg, v)

    ch1_subtrim.write(msg, CH1_SUBTRIM)
    ch2_subtrim.write(msg, CH2_SUBTRIM)
    ch3_subtrim.write(msg, CH3_SUBTRIM)
    ch4_subtrim.write(msg, CH4_SUBTRIM)
    ch5_subtrim.write(msg, CH5_SUBTRIM)
    ch6_subtrim.write(msg, CH6_SUBTRIM)

    mix1_src.write(msg, MIX1_SRC); mix1_dst.write(msg, MIX1_DST)
    mix1_upr.write(msg, MIX1_UPR); mix1_dwr.write(msg, MIX1_DWR); mix1_sw.write(msg, MIX1_SW)
    mix2_src.write(msg, MIX2_SRC); mix2_dst.write(msg, MIX2_DST)
    mix2_upr.write(msg, MIX2_UPR); mix2_dwr.write(msg, MIX2_DWR); mix2_sw.write(msg, MIX2_SW)
    mix3_src.write(msg, MIX3_SRC); mix3_dst.write(msg, MIX3_DST)
    mix3_upr.write(msg, MIX3_UPR); mix3_dwr.write(msg, MIX3_DWR); mix3_sw.write(msg, MIX3_SW)

    swa.write(msg, SWA)
    swb.write(msg, SWB)
    vra.write(msg, VRA)
    vrb.write(msg, VRB)

    payload = msg[1:-2]
    assert len(payload) == 65, f"expected 65-byte payload, got {len(payload)}"

    with open(OUT_FILE, "wb") as f:
        pickle.dump(payload, f)
    print(f"Wrote {OUT_FILE} ({len(payload)}-byte payload)")
    print(f"Upload with: python hkctrl.py -u {OUT_FILE}")


if __name__ == "__main__":
    main()

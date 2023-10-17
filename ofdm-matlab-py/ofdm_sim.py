import os
import numpy as np
from PIL import Image

from ofdm_parameters import ofdm_params
from ofdm_base_convert import ofdm_base_convert
from ofdm_modulate import ofdm_modulate

def ofdm_sim():
    carrier_count, carriers, clipping, conj_carriers, envelope, file_in, file_out, first_carrier, guard_time, head_len, ifft_size, last_carrier, midFreq, SNR_db, spacing, symb_per_frame, symb_period, symb_size, word_size  = ofdm_params()
    
    img = np.array(Image.open(file_in))

    img = img[:, :, :3]
    img_transposed = np.transpose(img, (2, 0, 1))
    img_flattened = img_transposed.flatten()
    baseband_tx = img_flattened.astype(np.float64)

    ######################## ORIGINAL LINES ###############################################
    # img_transposed = np.transpose(img, (1, 0, 2))
    # img_flattened = img_transposed.reshape(1, -1)
    # baseband_tx = img_flattened.astype(np.float64)
    ######################## ORIGINAL LINES ###############################################

    baseband_tx = ofdm_base_convert(baseband_tx, word_size, symb_size)
    
    ##################################################### OFDM TRANSMITTER ##################################################################

    # generate header and trailer (an exact copy of the header) 
    f = 0.25
    header = np.sin(np.arange(0, f * 2 * np.pi * head_len, f * 2 * np.pi))
    f = f / (np.pi * 2 / 3)
    header = header + np.sin(np.arange(0, f * 2 * np.pi * head_len, f * 2 * np.pi))
    with open('header.txt', 'w') as f:
        f.write(str(header))

    # arrange data into frames and transmit
    frame_guard = np.zeros((1, int(symb_period)), dtype=int)[0]
    time_wave_tx = np.array([])
    symb_per_carrier = np.ceil(len(baseband_tx) / carrier_count)
    fig = 1

    if symb_per_carrier > symb_per_frame: # if version still not been fixed since there is no sample
        power = 0

        while len(baseband_tx) > 0:
            # number of symbols per frame
            frame_len = min(symb_per_frame * carrier_count, len(baseband_tx))
            frame_data = baseband_tx[:frame_len]
            baseband_tx = baseband_tx[frame_len:]

            time_signal_tx = ofdm_modulate(baseband_tx, ifft_size, carriers, conj_carriers, carrier_count, symb_size, guard_time, fig)
            fig = 0

            time_wave_tx = np.concatenate((time_wave_tx, frame_guard, time_signal_tx))
            frame_power = np.var(time_signal_tx)

        power = power + frame_power
        time_wave_tx = np.concatenate((power * header, time_wave_tx, frame_guard, power * header))
    else:
        time_signal_tx = ofdm_modulate(baseband_tx, ifft_size, carriers, conj_carriers, carrier_count, symb_size, guard_time, fig)[0]
        power = np.var(time_signal_tx)
        time_wave_tx = np.concatenate((power * header, frame_guard, time_signal_tx, frame_guard, power * header))

    # Show summary of the OFDM transmission modelling

    # ####################################################### # 
    # **************** COMMUNICATION CHANNEL **************** #
    # ####################################################### # 

    # ===== signal clipping ===== # 
    clipped_peak = (10**(0-(clipping/20))) * max(abs(time_wave_tx))
    indices = np.where(np.abs(time_wave_tx) >= clipped_peak)
    time_wave_tx[indices] = (clipped_peak * time_wave_tx[indices]) / np.abs(time_wave_tx[indices])

if __name__  == "__main__" :
    ofdm_sim()
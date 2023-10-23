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

    baseband_tx = ofdm_base_convert(baseband_tx, word_size, symb_size)
    
    ##################################################### OFDM TRANSMITTER ##################################################################

    # generate header and trailer (an exact copy of the header) 
    f = 0.25
    header = np.sin(np.arange(0, f * 2 * np.pi * head_len, f * 2 * np.pi))
    f = f / (np.pi * 2 / 3)
    header = header + np.sin(np.arange(0, f * 2 * np.pi * head_len, f * 2 * np.pi))

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

    # ===== channel noise ===== #
    power = np.var(time_wave_tx)
    SNR_linear = 10**(SNR_db/10)
    noise_factor = np.sqrt(power/SNR_linear)
    noise = np.random.randn(1, len(time_wave_tx)) * noise_factor
    time_wave_rx = time_wave_tx + noise

    # show summary of the OFDM channel modeling
    # print(np.abs(time_wave_rx[int(head_len):len(time_wave_tx) - int(head_len)]))
    # peak = np.max(np.abs(time_wave_rx[int(head_len):len(time_wave_tx) - int(head_len)]))
    # with open("peak.txt", "w") as f:
    #     f.write(str(peak))
    # sig_rms = np.max(np.abs(time_wave_rx[head_len:(len(time_wave_tx)-head_len)]))

    # ####################################################### # 
    # ******************** OFDM RECEIVER ******************** #
    # ####################################################### # 

    time_wave_rx = time_wave_tx.T

    end_x = len(time_wave_rx)
    start_x = 1
    data = []
    phase = []
    last_frame = 0
    unpad = 0
    w = 16
    h = 16
    if w*h % carrier_count != 0:
        unpad = carrier_count - (w*h % carrier_count)

    num_frame = np.ceil((h*w) * (word_size/symb_size)/(symb_per_frame*carrier_count))
    fig = 0

    for k in range(len(num_frame+1)):
        if k == 0 or k == num_frame or k % np.max(np.floor(num_frame / 10), 1) == 0:
            print(f"Demodulating Frame #{k}")

        if k == 1:
            # time_wave = time_wave
            pass

if __name__  == "__main__" :
    ofdm_sim()
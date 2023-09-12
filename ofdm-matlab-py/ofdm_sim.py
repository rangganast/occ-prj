import os
import numpy as np
from PIL import Image

from ofdm_parameters import ofdm_params

def ofdm_sim():
    carrier_count, carriers, clipping, conj_carriers, envelope, file_in, file_out, first_carrier, guard_time, head_len, ifft_size, last_carrier, midFreq, SNR_db, spacing, symb_per_frame, symb_period, symb_size, word_size  = ofdm_params()
    
    img = Image.open(file_in)

    w, h = img.size
    img_transposed = np.transpose(img, (1, 0, 2))
    img_flattened = img_transposed.reshape(1, -1)
    baseband_tx = img_flattened.astype(np.float64)

if __name__  == "__main__" :
    ofdm_sim()
import os
import math

def ofdm_params():
    file_in = "";
    while not file_in:
        file_in = input("Source data filename: ")
        if not os.path.isfile(file_in):
            print(f"The file '{file_in} does not exist in the current directory'")
            file_in = ""

    file_out = f"{file_in[:len(file_in) - 4]}_OFDM.bmp"
    print(f"Output file will be: {file_out}")

    ifft_size = 0.1;
    while not int(ifft_size) or int(ifft_size) < 8:
        ifft_size = int(input('IFFT size (must be a power of 2 and at least 8): '))
        if not (ifft_size) or math.log2(ifft_size) % 1 != 0 or ifft_size < 8:
            print('IFFT size must be at least 8 and a power of 2.')

    carrier_count = int(ifft_size)
    while carrier_count > (ifft_size / 2 - 2) or carrier_count < 2:
        carrier_count = int(input("Number of carriers (must be less than IFFT size/2-2 and at least 2): "))
        if not carrier_count or carrier_count > ((ifft_size /2 ) - 2):
            print("Must NOT be greater than (IFFT size/2 - 2)")

    symb_size = 0
    while not symb_size or symb_size not in [1, 2, 4, 8]:
        symb_size = int(input('Modulation (1 = BPSK, 2 = QPSK, 4 = 16PSK, 8 = 256PSK): '))
        if not symb_size or symb_size not in [1, 2, 4, 8]:
            print('Only 1, 2, 4, or 8 can be chosen.')

    clipping = None
    while clipping is None:
        try:
            clipping = float(input('Amplitude clipping introduced by communication channel (in dB): '))
        except ValueError:
            pass

    SNR_db = None
    while not SNR_db:
        try:
            SNR_db = float(input('Signal-to-Noise Ratio (SNR) in dB:  '))
        except ValueError:
            pass

    # Other parameters
    word_size = 8
    guard_time = ifft_size / 4
    symb_per_frame = int(2 ** 13 / carrier_count)

    # Derived Parameters
    symb_period = ifft_size + guard_time
    head_len = symb_period * 8
    envelope = int(symb_period / 256) + 1

    # Carriers assigned to IFFT bins
    spacing = 0
    while (carrier_count * spacing) <= ((ifft_size/2)-2):
        spacing = spacing + 1

    spacing = spacing - 1

    midFreq = ifft_size / 4
    first_carrier = midFreq - round((carrier_count - 1) * spacing / 2)
    last_carrier = midFreq + int((carrier_count - 1) * spacing / 2)
    carriers = [first_carrier + i for i in range(0, carrier_count * spacing, spacing)]
    conj_carriers = [int(ifft_size - c + 2) for c in carriers]

    return (
        carrier_count,
        carriers,
        clipping,
        conj_carriers,
        envelope,
        file_in,
        file_out,
        first_carrier,
        guard_time,
        head_len,
        ifft_size,
        last_carrier,
        midFreq,
        SNR_db,
        spacing,
        symb_per_frame,
        symb_period,
        symb_size,
        word_size
    ) 

if __name__=="__main__":
    ofdm_params()
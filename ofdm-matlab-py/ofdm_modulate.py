import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt

def ofdm_modulate(data_tx, ifft_size, carriers, conj_carriers, carrier_count, symb_size, guard_time, fig):
    carrier_symb_count = int(np.ceil(len(data_tx) / carrier_count))

    if len(data_tx) / carrier_count != carrier_symb_count:
        padding = np.zeros(carrier_symb_count * carrier_count)
        padding[:len(data_tx)] = data_tx
        data_tx = padding
    
    data_tx_matrix = np.reshape(data_tx, (carrier_symb_count, carrier_count)).T

    carrier_symb_count = data_tx_matrix.shape[1] + 1
    # generate random list
    # diff_ref = np.round(np.random.rand(carrier_count) * (2**symb_size) + 0.5).reshape(1009, 1)
    diff_ref = loadmat('../matlab-sim/diff_ref.mat')
    diff_ref = diff_ref['diff_ref'][0].reshape(1009, 1)
    
    data_tx_matrix = np.hstack((diff_ref, data_tx_matrix))
    

    for k in range(1, data_tx_matrix.shape[1]):
        data_tx_matrix[:, k] = np.remainder(data_tx_matrix[:, k] + data_tx_matrix[:, k-1], 2**symb_size)    

    ones_array = np.ones_like(data_tx_matrix)

    X = np.round(np.cos(data_tx_matrix * (2* np.pi / 2**symb_size)) * ones_array)
    Y = np.round(np.sin(data_tx_matrix * (2* np.pi / 2**symb_size)) * ones_array)

    complex_matrix = X + 1j * Y

    spectrum_tx = np.zeros((ifft_size, carrier_symb_count), dtype=complex)
    spectrum_tx[carriers[0]:carriers[-1]+1, :] = complex_matrix  
    spectrum_tx[conj_carriers[-1]-2:conj_carriers[0]-1, :] = np.conjugate(complex_matrix)
    # safe until here

    # if fig == 1:
    #     plt.figure(1)
    #     plt.stem(np.arange(1, ifft_size + 1), np.abs(spectrum_tx[1, :]), 'b*-')
    #     plt.grid(True)
    #     plt.axis([0, ifft_size, -0.5, 1.5])
    #     plt.ylabel('Magnitude of PSK Data')
    #     plt.xlabel('IFFT Bin')
    #     plt.title('OFDM Carriers on deiignated IFFT bins')

    #     plt.figure(2)
    #     plt.plot(np.arange(1, ifft_size+1), (180/np.pi) * np.angle(spectrum_tx[1, 0:ifft_size]), 'go')
    #     plt.hold(True)
    #     plt.grid(True)
    #     plt.stem(carriers, (180/np.pi) * np.angle(spectrum_tx[1, carriers], 'b*-'))
    #     plt.stem(conj_carriers, (180/np.pi) * np.angle(spectrum_tx[1, conj_carriers]), 'b*-')
    #     plt.axis([0, ifft_size, -200, 200])
    #     plt.ylabel('Phase (degree)')
    #     plt.xlabel('IFFT Bin')
    #     plt.title('Phases of the OFDM modulated data')

    # signal_tx = np.real(np.fft.ifft(spectrum_tx.T).T)

    # if fig == 1:
    #     limt = 1.1 * np.max(np.abs(np.reshape(signal_tx, (1, signal_tx.size))))
    #     plt.figure(3)
    #     plt.plot(np.arange(1, ifft_size+1), signal_tx[1, :])
    #     plt.grid(True)
    #     plt.axis([0, ifft_size, -limt, limt])
    #     plt.ylabel('Amplitude')
    #     plt.xlabel('Time')
    #     plt.title('OFDM Time Signal (one symbol period in one carrier)')

    #     plt.figure(4)
    #     colors = ['b', 'g', 'r', 'c', 'm', 'y']
    #     for k in range(1, min(len(colors), carrier_symb_count -1)):
    #         plt.plot(np.arange(1, ifft_size+1), signal_tx[k+1, :], colors[k])
    #         plt.hold(True)
    #     plt.gird(True)
    #     plt.axis([0, ifft_size, -limt, limt])
    #     plt.ylabel('Amplitude')
    #     plt.xlabel('Time')
    #     plt.title('Samples of OFDM Time Signals over one symbol period')

    # # Add a periodic guard time
    # end_symb = signal_tx.shape[1]
    # signal_tx = np.concatenate((signal_tx[:, end_symb - guard_time:end_symb], signal_tx), axis=1)

    # signal_tx = np.reshape(signal_tx.T, (1, signal_tx.size))

    # return signal_tx

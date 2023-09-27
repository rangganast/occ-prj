import numpy as np

np.set_printoptions(threshold=np.inf)

def ofdm_base_convert(data_in, base, new_base): # array 8 2
    # Ensure the size of data in the current base is a multiple of its new base
    if new_base > base:
        data_in = data_in[:np.floor(len(data_in) // (new_base // base)) * (new_base // base)]

    binary_matrix = np.array([])
    for d in data_in:
        binary_base = format(int(d), f'0{base}b')
        binary_base_8col = np.array([int(x) for x in binary_base])
        binary_matrix = np.append(binary_matrix, binary_base_8col)

    # Format the binary matrix to fit dimensions of the new base
    newbase_matrix = binary_matrix.reshape(2, -1, order='F')
    transposed_newbase_matrix = newbase_matrix.T

    # Convert binary to the new base
    data_out = np.zeros(transposed_newbase_matrix.shape[0])
    for k in range(1, new_base+1):
        data_out += transposed_newbase_matrix[:, k-1] * (2**(new_base - k))

    return data_out
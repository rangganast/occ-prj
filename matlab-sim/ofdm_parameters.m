% OFDM Simulation Parameters Initialization
% Student: Paul Lin
% Professor: Dr. Cheng Sun
% Date: June, 2010

% Input/output file names
file_in = [];
while isempty(file_in)
    file_in = input('Source data filename: ', 's');
    if exist([pwd '/' file_in],'file') ~= 2
        fprintf('"%s" does not exist in the current directory.\n', file_in);
        file_in = [];
    end
end
file_out = [file_in(1:length(file_in)-4) '_OFDM.bmp'];
disp(['Output file will be: ' file_out]);

% IFFT size (must be a power of 2)
ifft_size = 0.1; % Initialize to force into the while loop below
while isempty(ifft_size) || rem(log2(ifft_size), 1) ~= 0 || ifft_size < 8
    ifft_size = input('IFFT size (must be a power of 2 and at least 8): ');
    if isempty(ifft_size) || rem(log2(ifft_size), 1) ~= 0 || ifft_size < 8
        disp('IFFT size must be at least 8 and a power of 2.');
    end
end

% Number of carriers
carrier_count = ifft_size; % Initialize to force into the while loop below
while isempty(carrier_count) || carrier_count > (ifft_size/2-2) || carrier_count < 2
    carrier_count = input('Number of carriers (must be less than IFFT size/2-2 and at least 2): ');
    if isempty(carrier_count) || carrier_count > (ifft_size/2-2)
        disp('Must NOT be greater than (IFFT size/2-2).');
    end
end

% Modulation (1 = BPSK, 2 = QPSK, 4 = 16PSK, 8 = 256PSK)
symb_size = 0; % Initialize to force into the while loop below
while isempty(symb_size) || ~(ismember(symb_size, [1, 2, 4, 8]))
    symb_size = input('Modulation (1 = BPSK, 2 = QPSK, 4 = 16PSK, 8 = 256PSK): ');
    if isempty(symb_size) || ~(ismember(symb_size, [1, 2, 4, 8]))
        disp('Only 1, 2, 4, or 8 can be chosen.');
    end
end

% Amplitude clipping introduced by communication channel (in dB)
clipping = [];
while isempty(clipping)
    clipping = input('Amplitude clipping introduced by communication channel (in dB): ');
end

% Signal-to-Noise Ratio (SNR) in dB
SNR_dB = [];
while isempty(SNR_dB)
    SNR_dB = input('Signal-to-Noise Ratio (SNR) in dB: ');
end

% Other parameters
word_size = 8;          % Bits per word of source data (byte)
guard_time = ifft_size/4; % Length of guard interval for each symbol period (25% of ifft_size)
symb_per_frame = ceil(2^13/carrier_count);

% Derived Parameters
symb_period = ifft_size + guard_time;
head_len = symb_period * 8;
envelope = ceil(symb_period/256) + 1;

% Carriers assigned to IFFT bins
spacing = 0;
while (carrier_count * spacing) <= (ifft_size/2 - 2)
    spacing = spacing + 1;
end
spacing = spacing - 1;

midFreq = ifft_size/4;
first_carrier = midFreq - round((carrier_count-1)*spacing/2);
last_carrier = midFreq + floor((carrier_count-1)*spacing/2);
carriers = [first_carrier:spacing:last_carrier] + 1;
conj_carriers = ifft_size - carriers + 2;
disp(carriers)

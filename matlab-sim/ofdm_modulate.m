% FUNCTION: ofdm_modulate()
% This function performs OFDM modulation before data transmission.
function signal_tx = ofdm_modulate(data_tx, ifft_size, carriers, conj_carriers, carrier_count, symb_size, guard_time, fig)
    % Symbols per carrier for this frame
    carrier_symb_count = ceil(length(data_tx) / carrier_count);

    % Append zeros to data with a length not multiple of the number of carriers
    if length(data_tx) / carrier_count ~= carrier_symb_count
        padding = zeros(1, carrier_symb_count * carrier_count);
        padding(1:length(data_tx)) = data_tx;
        data_tx = padding;
    end

    % Serial to parallel: each column represents a carrier
    data_tx_matrix = reshape(data_tx, carrier_count, carrier_symb_count)';

    % Differential Encoding
    carrier_symb_count = size(data_tx_matrix, 1) + 1;
    diff_ref = round(rand(1, carrier_count) * (2^symb_size) + 0.5);
    data_tx_matrix = [diff_ref; data_tx_matrix];
    for k = 2:size(data_tx_matrix, 1)
        data_tx_matrix(k, :) = rem(data_tx_matrix(k, :) + data_tx_matrix(k-1, :), 2^symb_size);
    end

    % PSK (Phase Shift Keying) modulation
    [X, Y] = pol2cart(data_tx_matrix * (2*pi / (2^symb_size)), ones(size(data_tx_matrix)));
    complex_matrix = X + 1i * Y;

    % Assign IFFT bins to carriers and imaged carriers
    spectrum_tx = zeros(carrier_symb_count, ifft_size);
    spectrum_tx(:, carriers) = complex_matrix;
    spectrum_tx(:, conj_carriers) = conj(complex_matrix);

    % Plot OFDM Carriers on IFFT bins
    if fig == 1
        figure(1);
        stem(1:ifft_size, abs(spectrum_tx(2, :)), 'b*-');
        grid on;
        axis([0 ifft_size -0.5 1.5]);
        ylabel('Magnitude of PSK Data');
        xlabel('IFFT Bin');
        title('OFDM Carriers on designated IFFT bins');

        figure(2);
        plot(1:ifft_size, (180/pi) * angle(spectrum_tx(2, 1:ifft_size)), 'go');
        hold on;
        grid on;
        stem(carriers, (180/pi) * angle(spectrum_tx(2, carriers)), 'b*-');
        stem(conj_carriers, (180/pi) * angle(spectrum_tx(2, conj_carriers)), 'b*-');
        axis([0 ifft_size -200 +200]);
        ylabel('Phase (degree)');
        xlabel('IFFT Bin');
        title('Phases of the OFDM modulated Data');
    end

    % Obtain time wave from spectra using IFFT
    signal_tx = real(ifft(spectrum_tx'))';

    % Plot time signals
    if fig == 1
        % OFDM Time Signal (one symbol period in one carrier)
        limt = 1.1 * max(abs(reshape(signal_tx', 1, size(signal_tx, 1) * size(signal_tx, 2))));
        figure(3);
        plot(1:ifft_size, signal_tx(2, :));
        grid on;
        axis([0 ifft_size -limt limt]);
        ylabel('Amplitude');
        xlabel('Time');
        title('OFDM Time Signal (one symbol period in one carrier)');

        % Samples of OFDM Time Signals over one symbol period
        figure(4);
        colors = ['b', 'g', 'r', 'c', 'm', 'y'];
        for k = 1:min(length(colors), (carrier_symb_count - 1))
            plot(1:ifft_size, signal_tx(k + 1, :), colors(k));
            hold on;
        end
        grid on;
        axis([0 ifft_size -limt limt]);
        ylabel('Amplitude');
        xlabel('Time');
        title('Samples of OFDM Time Signals over one symbol period');
    end

    % Add a periodic guard time
    end_symb = size(signal_tx, 2);  % end of a symbol period without guard
    signal_tx = [signal_tx(:, (end_symb - guard_time + 1):end_symb) signal_tx];

    % Parallel to serial
    signal_tx = signal_tx';  % MATLAB's reshape goes along with columns
    signal_tx = reshape(signal_tx, 1, size(signal_tx, 1) * size(signal_tx, 2));
end

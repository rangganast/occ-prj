function start_symb = ofdm_frame_detect(signal, symb_period, env, label)
    % Find the approximate starting location
    signal = abs(signal);

    % Narrow down to an approximate start of the frame
    idx = 1:env:length(signal);
    samp_signal = signal(idx);  % Sampled version of signal
    mov_sum = filter(ones(1, round(symb_period / env)), 1, samp_signal);
    mov_sum = mov_sum(round(symb_period / env):end);
    apprx = min(find(mov_sum == min(mov_sum)) * env + symb_period);

    % Move back by approximately 110% of the symbol period to start searching
    idx_start = round(apprx - 1.1 * symb_period);

    % Look into the narrowed-down window
    mov_sum = filter(ones(1, symb_period), 1, signal(idx_start:round(apprx + symb_period / 3)));
    mov_sum = mov_sum(symb_period:end);
    null_sig = find(mov_sum == min(mov_sum));

    % Convert to global index
    start_symb = min(idx_start + null_sig + symb_period) - 1;
    start_symb = start_symb + (label - 1);
end

% FUNCTION: ofdm_base_convert()
% This function converts data from one base to another.
% "Base" refers to the number of bits the symbol/word uses to represent data.
function data_out = ofdm_base_convert(data_in, base, new_base)
    % Ensure the size of data in the current base is a multiple of its new base
    if new_base > base
        data_in = data_in(1:floor(length(data_in)/(new_base/base))*(new_base/base));
    end
    
    % Convert base to binary
    for k = 1:base
        binary_matrix(k, :) = floor(data_in / 2^(base - k));
        data_in = rem(data_in, 2^(base - k));
    end
    
    % Format the binary matrix to fit dimensions of the new base
    newbase_matrix = reshape(binary_matrix, new_base, size(binary_matrix, 1) * size(binary_matrix, 2) / new_base);
    
    % Convert binary to the new base
    data_out = zeros(1, size(newbase_matrix, 2));
    for k = 1:new_base
        data_out = data_out + newbase_matrix(k, :) * (2^(new_base - k));
    end
end

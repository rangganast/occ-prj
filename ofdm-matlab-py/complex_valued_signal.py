import numpy as np

# Create a sample frequency-domain signal (complex numbers)
frequency_signal = np.array([1 + 2j, 2 - 3j, 0 + 1j, -2 + 1j])

# Perform IFFT to convert it to the time-domain signal
time_signal = np.fft.ifft(frequency_signal)

# Display the frequency-domain and time-domain signals
print("Frequency-domain signal:")
print(frequency_signal)

print("\nTime-domain signal:")
print(time_signal)

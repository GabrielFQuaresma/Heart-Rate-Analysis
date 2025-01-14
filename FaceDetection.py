import cv2
from cvzone.FaceDetectionModule import FaceDetector
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import numpy as np



# Low-Pass filter Butterworth
def butter_lowpass(cutoff, fs=30, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

# Apply the filter
def apply_lowpass_filter(data, cutoff=2, fs=30, order=4):
    b, a = butter_lowpass(cutoff, fs, order)
    y = filtfilt(b, a, data)
    return y

# High-Pass Filter Butterworth
def butter_highpass(cutoff, fs=30, order=4):
    nyquist = 0.5 * fs  # Nyquist's Frequency
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

# Apply the filter
def apply_highpass_filter(data, cutoff=0.5, fs=30, order=4):
    b, a = butter_highpass(cutoff, fs, order)
    y = filtfilt(b, a, data)
    return y



def heart_rate_analysis(desired_fps=30):

    # Define the desired fps
    delay = int(1000 / desired_fps)

    #Open the first webcam
    webcam = cv2.VideoCapture(0)

    green_values = []

    #Using Close Range Modal
    detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)

    if webcam.isOpened():
        validation, frame = webcam.read()
        
        while validation:
            validation, frame = webcam.read()
            frame, bboxes = detector.findFaces(frame)

            if bboxes:
                x, y, w, h = bboxes[0]['bbox']
                
                # ------- Define ROI in forehead -------
                roi_x = x + 20
                roi_y = y - 20
                roi_w = w - 2 * 20
                roi_h = h // 5

                # Extract the ROI
                roi = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]

                #Getting the colors in the ROI
                mean_color = cv2.mean(roi)
                blue, green, red = mean_color[:3]

                #Building the time series
                green_values.append(green)

                #Write the color values
                cv2.putText(frame, f"R: {int(red)} G: {int(green)} B: {int(blue)}", (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                #Draw a new rectangle that represents the forehead
                cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)
            
            cv2.imshow("WebcamVideo", frame)
            
            key = cv2.waitKey(delay)
            
            # key == 'ESC'
            if key == 27:
                break         
        
        
        webcam.release()
        cv2.destroyAllWindows()

    # Filter to remove movements 
    lowPass = apply_lowpass_filter(green_values)

    # Filter to attenuate the light changes
    highPass = apply_highpass_filter(green_values)

    # Both filter combined
    filtered_signals = apply_highpass_filter(lowPass)

    #Draw the time series
    plt.plot(green_values, label="Green Channel")
    plt.plot(lowPass, label="Low-Pass Filter", linewidth=2)
    plt.plot(highPass, label="High-Pass Filter", linewidth=2, color="orange")
    plt.plot(filtered_signals, label="Filtered Signal (Both Filters)", linestyle="dashed", color="green")
    plt.title("Green Channel Intensity Over Time")
    plt.xlabel("Frame Index")
    plt.ylabel("Intensity")
    plt.legend()
    plt.show()


    # Apply FFT in the signal
    fft_result = np.fft.fft(filtered_signals)
    frequencies = np.fft.fftfreq(len(fft_result), d=1/30)

    # Only the positive part
    positive_frequencies = frequencies[:len(frequencies)//2]
    positive_magnitude = np.abs(fft_result[:len(fft_result)//2])

    # Identify the dominant frequency in the range of interest
    freq_min, freq_max = 0.8, 2  # Frequency range (0.8 to 2 Hz)
    valid_range = (positive_frequencies >= freq_min) & (positive_frequencies <= freq_max)
    dominant_freq = positive_frequencies[valid_range][np.argmax(positive_magnitude[valid_range])]

    # Convert to BPM
    bpm = dominant_freq * 60

    # Plot the signal and the frequency spectrum
    plt.figure(figsize=(12, 6))

    # Signal in time domain
    plt.subplot(2, 1, 1)
    plt.plot(filtered_signals, label="Filtered Signal")
    plt.title("Signal in Time Domain")
    plt.xlabel("Time (s)")
    plt.ylabel("Intensity")
    plt.legend()

    # Frequency spectrum
    plt.subplot(2, 1, 2)
    plt.plot(positive_frequencies, positive_magnitude, label="Frequency Spectrum")
    plt.axvline(dominant_freq, color='r', linestyle='--', label=f"Dominant Freq. = {dominant_freq:.2f} Hz ({bpm:.0f} BPM)")
    plt.title("Frequency Spectrum (FFT)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.legend()

    plt.tight_layout()
    plt.show()

    print(f"Dominant Frequency: {dominant_freq:.2f} Hz")
    print(f"Beats per Minute (BPM): {bpm:.0f}")
        # freq_min, freq_max = 0.8, 2  # Faixa de frequência (0.8 a 2 Hz)
        # valid_range = (positive_frequencies >= freq_min) & (positive_frequencies <= freq_max)
        # dominant_freq = positive_frequencies[valid_range][np.argmax(positive_magnitude[valid_range])]

        # # Converte para BPM
        # bpm = dominant_freq * 60

        # # Plota o sinal e o espectro de frequência
        # plt.figure(figsize=(12, 6))

        # # Sinal no tempo
        # plt.subplot(2, 1, 1)
        # plt.plot(filtered_signals, label="Sinal sem Ruído")
        # plt.title("Sinal no Domínio do Tempo")
        # plt.xlabel("Tempo (s)")
        # plt.ylabel("Intensidade")
        # plt.legend()

        # # Espectro de frequência
        # plt.subplot(2, 1, 2)
        # plt.plot(positive_frequencies, positive_magnitude, label="Espectro de Frequência")
        # plt.axvline(dominant_freq, color='r', linestyle='--', label=f"Freq. Dominante = {dominant_freq:.2f} Hz ({bpm:.0f} BPM)")
        # plt.title("Espectro de Frequência (FFT)")
        # plt.xlabel("Frequência (Hz)")
        # plt.ylabel("Magnitude")
        # plt.legend()

        # plt.tight_layout()
        # plt.show()

        # print(f"Frequência Dominante: {dominant_freq:.2f} Hz")
        # print(f"Batimentos por Minuto (BPM): {bpm:.0f}")

if __name__ == "__main__":
    heart_rate_analysis() 
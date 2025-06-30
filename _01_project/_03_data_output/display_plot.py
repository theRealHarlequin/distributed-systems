import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Dict, List
from datetime import datetime
# Call
    #generate_plot(stats ={'Timestamp': 1234545, 'Sensor_ID': 12},
    #                       data=dict(zip(timestamps, sensor_values)))


def generate_plot(data:Dict, stats:Dict=None):
    statistic_data:List[List]= [[]]
    time = [datetime.fromtimestamp(ts) for ts in list(data.keys())[1:]]
    value =list(data.values())
    sens_value_np = np.array(value)
    if stats is None:
        statistic_data = [['No Statistics available']]
    else:
        statistic_data = [[key, value] for key, value in stats.items()]

    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 4)

    # Data table
    ax_table = fig.add_subplot(gs[0, 0])
    ax_table.axis('off')
    table = ax_table.table(cellText=statistic_data, loc='center', cellLoc='left')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.3)  # Adjust the scale to fit your plot

    # Add a title to the table
    ax_table.text(0.5, 1.02, 'Sensor Data Statistics', fontsize=14, fontweight='bold', ha='center',
                  transform=ax_table.transAxes)

    # Time domain plot
    ax1 = fig.add_subplot(gs[0, 1:])
    ax1.plot(time, sens_value_np, 'b-', label='Sensor Data')
    ax1.set_title('Sensor Data')
    ax1.set_xlabel('Time')
    ax1.set_ylabel(f'DataUnit - {stats["Unit"] if "Unit" in stats.keys() else ""}')
    ax1.set_ylim(-1.5, 1.5)
    ax1.legend()
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    fig.autofmt_xdate()  # Rotate and align the tick labels

    # Compute FFT
    if 'Sampling Rate' in stats.keys():
        fft_values = np.fft.fft(sens_value_np)
        fft_freq = np.fft.fftfreq(len(sens_value_np), d=1 / stats['Sampling Rate'])
        positive_freq_idx = np.where(fft_freq >= 0)
        fft_freq = fft_freq[positive_freq_idx]
        fft_mag = np.abs(fft_values)[positive_freq_idx]

        # Magnitude Spectrum (linear scale)
        ax2 = fig.add_subplot(gs[1, :2])
        ax2.plot(fft_freq, fft_mag, 'r-', label='Magnitude')
        ax2.set_title('Magnitude Spectrum (Linear)')
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Magnitude')
        ax2.set_xlim(0, 10)
        ax2.legend()

        # Power Spectrum
        ax3 = fig.add_subplot(gs[1, 2:])
        ax3.plot(fft_freq, fft_mag ** 2, 'g-', label='Power')
        ax3.set_title('Power Spectrum')
        ax3.set_xlabel('Frequency (Hz)')
        ax3.set_ylabel('Power')
        ax3.set_xlim(0, 10)
        ax3.legend()

    # Magnitude Spectrum (dB scale)
    ax4 = fig.add_subplot(gs[2, :2])
    ax4.plot(fft_freq, 20 * np.log10(fft_mag), 'm-', label='Magnitude (dB)')
    ax4.set_title('Magnitude Spectrum (dB)')
    ax4.set_xlabel('Frequency (Hz)')
    ax4.set_ylabel('Magnitude (dB)')
    ax4.set_xlim(0, 10)
    ax4.legend()

    # Spectrogram

    if 'Sampling Rate' in stats.keys():
        ax5 = fig.add_subplot(gs[2, 2:])
        spec, freqs, t, im = ax5.specgram(sens_value_np, Fs=stats['Sampling Rate'], noverlap=128, cmap='viridis')
        ax5.set_title('Spectrogram')
        ax5.set_xlabel('Time')
        ax5.set_ylabel('Frequency (Hz)')
        fig.colorbar(im, ax=ax5, label='Intensity (dB)')

    plt.tight_layout()
    plt.show()

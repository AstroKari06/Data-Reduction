import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from pathlib import Path

folder = Path(r"your_folder_path_here")  # Replace with your actual folder path

# Master biasy
# Make sure to replace the file names with the actual names of your master bias files
bias_files = {
    "0C": folder / "average_bias_0.fits",
    "15C": folder / "average_bias_15.fits"
}

plt.figure(figsize=(10, 6))

for temperature, filename in bias_files.items():

    data = fits.getdata(filename)
    data = data[np.isfinite(data)]

    plt.hist(
        data.ravel(),
        bins=100,
        histtype="step",
        linewidth=1.5,
        label=temperature
    )

plt.xlabel("Wartość piksela [ADU]")
plt.ylabel("Liczba pikseli")
plt.title("Histogram master biasów dla różnych temperatur")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(folder / "histogram_master_bias.png", dpi=300) #dpi znaczy dots per inch, czyli ile pikseli przypada na cal. Im wyższa wartość dpi, tym lepsza jakość obrazu ale też większy rozmiar pliku. 300 dpi to standardowa wartość dla druku, natomiast 72 dpi jest wystarczające dla wyświetlania na ekranie.
plt.show()


# Master darki
# Make sure to replace the file names with the actual names of your master dark files
dark_files = {
    "0C, 10 s": folder / "average_dark_10_0.fits",
    "0C, 1 s": folder / "average_dark_01_0.fits",
    

    "15C, 10 s": folder / "average_dark_10_15.fits",
    "15C, 1 s": folder / "average_dark_01_15.fits"
}

plt.figure(figsize=(12, 7))

for label, filename in dark_files.items():

    data = fits.getdata(filename)
    data = data[np.isfinite(data)]

    plt.hist(
        data.ravel(),
        bins=100,
        histtype="step",
        linewidth=1.3,
        label=label
    )

plt.xlabel("Wartość piksela [ADU]")
plt.ylabel("Liczba pikseli")
plt.title("Histogram master darków dla różnych temperatur i czasów ekspozycji")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(folder / "histogram_master_dark.png", dpi=300)
plt.show()

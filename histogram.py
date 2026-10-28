import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from pathlib import Path

folder = Path(r"/mnt/c/Data/Histogram")

bias_files = {
    #"0C": folder / "average_bias_0.fits",
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

plt.yscale("log")
plt.xlabel("Pixel value [ADU]")
plt.ylabel("Number of pixels")
plt.title("Master Bias Histogram at Different Temperatures")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(folder / "histogram_master_bias.png", dpi=300)
plt.show()


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

plt.yscale("log")
plt.xlabel("Pixel value [ADU]")
plt.ylabel("Number of pixels")
plt.title("Master Dark Histogram at Different Temperatures and Exposure Times")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(folder / "histogram_master_dark.png", dpi=300)
plt.show()
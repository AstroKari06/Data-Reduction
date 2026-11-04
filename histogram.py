from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from matplotlib.axes import Axes


FOLDER = Path(r"/mnt/c/Data/Histogram")
BINS = np.linspace(0, 5000, 101)


def load_fits_data(filename: Path) -> np.ndarray:
    """Load finite pixel values from a FITS file."""
    if not filename.exists():
        raise FileNotFoundError(f"FITS file not found: {filename}")

    data = fits.getdata(filename)
    return data[np.isfinite(data)].ravel()


def add_histogram(
    axis: Axes,
    data: np.ndarray,
    label: str,
) -> None:
    """Add one outlined histogram to an existing axis."""
    axis.hist(
        data,
        bins=BINS,
        histtype="step",
        linewidth=1.5,
        label=label,
    )


def configure_histogram_axis(axis: Axes, title: str) -> None:
    """Apply the shared formatting used by dark histogram plots."""
    axis.set_title(title)
    axis.set_xlim(0, 5000)
    axis.set_yscale("log")
    axis.set_xlabel("Pixel value [ADU]")
    axis.grid(alpha=0.3)


def plot_bias_histograms(
    bias_files: dict[str, Path],
    output_file: Path,
) -> None:
    """Plot bias histograms for each temperature."""
    figure, axis = plt.subplots(figsize=(10, 6))

    for temperature, filename in bias_files.items():
        add_histogram(axis, load_fits_data(filename), temperature)

    axis.set_yscale("log")
    axis.set_xlim(550, 900)
    axis.set_xlabel("Pixel value [ADU]")
    axis.set_ylabel("Number of pixels")
    axis.set_title("Master Bias Histogram at Different Temperatures")
    axis.legend()
    axis.grid(alpha=0.3)
    figure.tight_layout()
    figure.savefig(output_file, dpi=300)
    plt.show()


def plot_dark_by_exposure(
    dark_files: dict[str, dict[str, Path]],
    output_file: Path,
) -> None:
    """Compare temperatures in a separate panel for each exposure time."""
    figure, axes = plt.subplots(
        1,
        len(dark_files),
        figsize=(12, 6),
        sharex=True,
        sharey=True,
        squeeze=False,
    )

    for axis, (exposure_time, temperature_files) in zip(
        axes.flat, dark_files.items()
    ):
        for temperature, filename in temperature_files.items():
            add_histogram(axis, load_fits_data(filename), temperature)

        configure_histogram_axis(axis, f"Exposure time: {exposure_time}")
        axis.legend()

    axes[0, 0].set_ylabel("Number of pixels")
    figure.suptitle("Master Dark Histograms at Different Temperatures")
    figure.tight_layout()
    figure.savefig(output_file, dpi=300)
    plt.show()


def plot_dark_by_temperature(
    dark_files: dict[str, dict[str, Path]],
    output_file: Path,
) -> None:
    """Compare exposure times in a separate panel for each temperature."""
    figure, axes = plt.subplots(
        1,
        len(dark_files),
        figsize=(12, 6),
        sharex=True,
        sharey=True,
        squeeze=False,
    )

    for axis, (temperature, exposure_files) in zip(
        axes.flat, dark_files.items()
    ):
        for exposure_time, filename in exposure_files.items():
            add_histogram(axis, load_fits_data(filename), exposure_time)

        configure_histogram_axis(axis, f"Temperature: {temperature}")
        axis.legend(title="Exposure time")

    axes[0, 0].set_ylabel("Number of pixels")
    figure.suptitle("Master Dark Histograms at Different Exposure Times")
    figure.tight_layout()
    figure.savefig(output_file, dpi=300)
    plt.show()


def main() -> None:
    """Create all bias and dark histogram figures."""
    bias_files = {
        "0C": FOLDER / "master_bias.fits",
        "15C": FOLDER / "average_bias_15.fits",
    }

    dark_files_by_exposure = {
        "1 s": {
            "0C": FOLDER / "average_dark_01_0.fits",
            "15C": FOLDER / "average_dark_01_15.fits",
        },
        "10 s": {
            "0C": FOLDER / "average_dark_10_0.fits",
            "15C": FOLDER / "average_dark_10_15.fits",
        },
    }

    dark_files_by_temperature = {
        "0C": dark_files_by_exposure["1 s"]
        | dark_files_by_exposure["10 s"],
        "15C": {
            "1 s": FOLDER / "average_dark_01_15.fits",
            "10 s": FOLDER / "average_dark_10_15.fits",
            "60 s": FOLDER / "average_dark_60_15.fits",
        },
    }

    plot_bias_histograms(
        bias_files,
        FOLDER / "histogram_master_bias.png",
    )
    plot_dark_by_exposure(
        dark_files_by_exposure,
        FOLDER / "histogram_master_dark_by_exposure.png",
    )
    plot_dark_by_temperature(
        dark_files_by_temperature,
        FOLDER / "histogram_master_dark_by_temperature.png",
    )


if __name__ == "__main__":
    main()

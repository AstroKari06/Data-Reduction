from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits


FOLDER = Path(r"/mnt/c/Data/Dark_bias/2026-10-21-Dark-15C60s")
OUTPUT_FILENAME = "average_dark_60_15.fits"


def find_fits_files(folder: Path, output_path: Path) -> list[Path]:
    """Find input FITS files without including the generated output file."""
    filenames = {
        filename
        for extension in ("*.fit", "*.fits", "*.fts")
        for filename in folder.glob(extension)
    }
    return sorted(filename for filename in filenames if filename != output_path)


def load_images(filenames: list[Path]) -> list[np.ndarray]:
    """Load image data from FITS files and validate their dimensions."""
    images = []

    for filename in filenames:
        with fits.open(filename) as hdul:
            data = hdul[0].data

        if data is not None:
            images.append(np.array(data, dtype=np.float64))
            print(f"Loaded: {filename.name}")

    print(f"Total images loaded: {len(images)}")

    if not images:
        raise ValueError("No FITS images found in the folder.")

    if not all(image.shape == images[0].shape for image in images):
        raise ValueError("FITS images have different dimensions.")

    return images


def average_images(images: list[np.ndarray]) -> np.ndarray:
    """Calculate the per-pixel mean of a collection of images."""
    average_image = np.mean(images, axis=0)
    print("Average image shape:", average_image.shape)
    return average_image


def save_fits_image(image: np.ndarray, output_path: Path) -> None:
    """Save an averaged image as a FITS file."""
    fits.writeto(output_path, image, overwrite=True)
    print(f"Saved average image to: {output_path}")


def show_image(image: np.ndarray) -> None:
    """Display an averaged image in grayscale."""
    plt.imshow(image, cmap="gray")
    plt.title("Average Dark Image")
    plt.show()


def main() -> None:
    """Load dark images, average them, save the result, and display it."""
    output_path = FOLDER / OUTPUT_FILENAME
    filenames = find_fits_files(FOLDER, output_path)
    images = load_images(filenames)
    average_image = average_images(images)
    save_fits_image(average_image, output_path)
    show_image(average_image)


if __name__ == "__main__":
    main()

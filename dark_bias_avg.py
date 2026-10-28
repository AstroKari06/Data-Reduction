from astropy.io import fits
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt

folder = Path(r"C:\Users\karos\AppData\Roaming\ASIImg\2026-10-21_16_07_36Z")

fits_files = (
    folder.glob("*.fit")
    + folder.glob("*.fits")
    + folder.glob("*.fts")
)

images = []

for filename in fits_files:
    with fits.open(filename) as hdul:
        data = hdul[0].data

        if data is not None:
            images.append(np.array(data, dtype=np.float64))
            print(f"Loaded: {filename.name}")

print(f"Total images loaded: {len(images)}")

if not images:
    raise ValueError("No FITS images found in the folder.")

if not all(img.shape == images[0].shape for img in images):
    raise ValueError("FITS images have different dimensions.")

average_image = np.mean(images, axis=0)

print("Average image shape:", average_image.shape)

output_path = folder / "average_dark.fits"

fits.writeto(
    output_path,
    average_image,
    overwrite=True
)

print(f"Saved average image to: {output_path}")

plt.imshow(average_image, cmap='gray')
plt.title('Average Dark Image')
plt.show()
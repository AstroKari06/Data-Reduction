from astropy.io import fits
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from itertools import chain

folder = Path(r"/mnt/c/Data/Dark_bias/2026-10-21_15_52_42Z")

fits_files = chain(
    folder.glob("*.fit"),
    folder.glob("*.fits"),
    folder.glob("*.fts")
) #sety od razu usuwają duplikaty, więc nie trzeba się martwić o powtarzające się pliki.

images = []

for filename in fits_files:
    with fits.open(filename) as hdul:
        data = hdul[0].data

        if data is not None:
            images.append(np.array(data, dtype=np.float64)) #np.float64 to typ danych zmiennoprzecinkowych o podwójnej precyzji, który pozwala na przechowywanie liczb rzeczywistych z większą dokładnością niż np. np.float32. Użycie tego typu danych jest istotne w przypadku obróbki obrazów astronomicznych, gdzie precyzja jest kluczowa dla analizy danych.
            print(f"Loaded: {filename.name}")

print(f"Total images loaded: {len(images)}")

if not images:
    raise ValueError("No FITS images found in the folder.")

if not all(img.shape == images[0].shape for img in images):
    raise ValueError("FITS images have different dimensions.")

average_image = np.mean(images, axis=0) #axis mówi o tym, wzdłuż której osi ma być obliczana średnia. W tym przypadku axis=0 oznacza, że średnia jest obliczana wzdłuż pierwszej osi (czyli dla każdego piksela w obrazie).

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
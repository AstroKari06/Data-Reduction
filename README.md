# Data-Reduction
University project for data reduction of observational data.

## Python tools for master frames and histograms

This repository now includes two VS Code-friendly Python scripts:

- `create_master_files.py`: creates **master bias** and **master dark** files grouped by temperature.
- `plot_master_histograms.py`: generates histogram plots for created master files.

### Expected input layout

Place raw calibration frames under:

```text
<input-root>/
  bias/
    <temperature-label>/
      frame1.npy or frame1.fits
      frame2.npy or frame2.fits
  dark/
    <temperature-label>/
      frame1.npy or frame1.fits
      frame2.npy or frame2.fits
```

Temperature labels are taken from folder names (for example `-10C`, `0C`, `20C`).

### Create master files

```bash
python create_master_files.py \
  --input-root ./calibration \
  --output-root ./masters \
  --combine median \
  --output-format npy
```

This creates output like:

```text
./masters/
  bias/master_bias_-10C.npy
  dark/master_dark_-10C.npy
```

### Create histograms of master files

```bash
python plot_master_histograms.py \
  --masters-root ./masters \
  --output-root ./histograms \
  --bins 100
```

This creates histogram images such as:

```text
./histograms/
  bias/master_bias_-10C_hist.png
  dark/master_dark_-10C_hist.png
```

### Notes

- `.npy` files work out of the box.
- FITS (`.fits`, `.fit`, `.fits.gz`) input/output is supported when `astropy` is installed.

#!/usr/bin/env python3
"""Generate histograms for master bias and master dark files."""

from __future__ import annotations

import argparse
from pathlib import Path

FITS_SUFFIXES = {".fits", ".fit", ".fts", ".fits.gz"}


def _np():
    try:
        import numpy as np  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("This script requires numpy. Install with: pip install numpy") from exc
    return np


def _plt():
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError(
            "This script requires matplotlib. Install with: pip install matplotlib"
        ) from exc
    return plt


def _is_fits(path: Path) -> bool:
    lower = path.name.lower()
    return any(lower.endswith(suffix) for suffix in FITS_SUFFIXES)


def _load_master(path: Path):
    np = _np()
    if _is_fits(path):
        try:
            from astropy.io import fits  # type: ignore
        except ImportError as exc:  # pragma: no cover - environment dependent
            raise RuntimeError(
                "FITS input requires astropy. Install with: pip install astropy"
            ) from exc
        return np.asarray(fits.getdata(path), dtype=np.float64)

    if path.suffix.lower() == ".npy":
        return np.asarray(np.load(path), dtype=np.float64)

    raise ValueError(f"Unsupported master file type: {path}")


def _iter_master_files(masters_root: Path):
    if not masters_root.exists():
        return
    for file_path in sorted(masters_root.rglob("*")):
        if not file_path.is_file():
            continue
        lower = file_path.name.lower()
        if lower.endswith((".npy", ".fits", ".fit", ".fts", ".fits.gz")):
            yield file_path


def _plot_histogram(array, title: str, output_path: Path, bins: int) -> None:
    plt = _plt()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 5))
    plt.hist(array.ravel(), bins=bins, color="steelblue", alpha=0.85)
    plt.title(title)
    plt.xlabel("Pixel value")
    plt.ylabel("Count")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate histograms for master bias and master dark files."
    )
    parser.add_argument(
        "--masters-root",
        type=Path,
        required=True,
        help="Root folder containing master bias/dark files.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        required=True,
        help="Folder where histogram PNG images will be written.",
    )
    parser.add_argument(
        "--bins",
        type=int,
        default=100,
        help="Number of histogram bins.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    written = 0
    for master_file in _iter_master_files(args.masters_root):
        data = _load_master(master_file)
        relative_parent = master_file.parent.relative_to(args.masters_root)
        output_name = f"{master_file.stem}_hist.png"
        output_path = args.output_root / relative_parent / output_name
        _plot_histogram(
            data,
            title=f"Histogram: {master_file.name}",
            output_path=output_path,
            bins=args.bins,
        )
        print(f"{master_file} -> {output_path}")
        written += 1

    if written == 0:
        print("No master files found to plot.")
        return 1

    print(f"Done. Wrote {written} histogram file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

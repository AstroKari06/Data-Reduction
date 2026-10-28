#!/usr/bin/env python3
"""Create master bias and master dark frames grouped by temperature."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

FITS_SUFFIXES = {".fits", ".fit", ".fts", ".fits.gz"}


def _np():
    try:
        import numpy as np  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("This script requires numpy. Install with: pip install numpy") from exc
    return np


def _is_fits(path: Path) -> bool:
    lower = path.name.lower()
    return any(lower.endswith(suffix) for suffix in FITS_SUFFIXES)


def _load_frame(path: Path):
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

    raise ValueError(f"Unsupported frame type: {path}")


def _save_frame(array: np.ndarray, out_path: Path, output_format: str) -> None:
    np = _np()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if output_format == "fits":
        try:
            from astropy.io import fits  # type: ignore
        except ImportError as exc:  # pragma: no cover - environment dependent
            raise RuntimeError(
                "FITS output requires astropy. Install with: pip install astropy"
            ) from exc
        fits.writeto(out_path, array, overwrite=True)
    else:
        np.save(out_path, array)


def _collect_temperature_groups(frames_root: Path) -> dict[str, list[Path]]:
    if not frames_root.exists():
        return {}

    groups: dict[str, list[Path]] = {}
    for path in sorted(frames_root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".npy", ".fits", ".fit", ".fts", ".gz"}:
            continue

        temp_label = path.parent.name if path.parent != frames_root else "unknown"
        groups.setdefault(temp_label, []).append(path)
    return groups


def _combine_frames(paths: Iterable[Path], combine: str) -> np.ndarray:
    np = _np()
    frames = [np.asarray(_load_frame(path), dtype=np.float64) for path in paths]
    if not frames:
        raise ValueError("No frames provided for master creation")

    stack = np.stack(frames, axis=0)
    if combine == "mean":
        return np.mean(stack, axis=0)
    return np.median(stack, axis=0)


def _build_masters(
    frame_kind: str,
    groups: dict[str, list[Path]],
    output_root: Path,
    combine: str,
    output_format: str,
) -> int:
    written = 0
    extension = ".fits" if output_format == "fits" else ".npy"
    for temp_label, paths in groups.items():
        master = _combine_frames(paths, combine=combine)
        output_name = f"master_{frame_kind}_{temp_label}{extension}"
        output_path = output_root / frame_kind / output_name
        _save_frame(master, output_path, output_format=output_format)
        print(f"[{frame_kind}] {temp_label}: {len(paths)} frame(s) -> {output_path}")
        written += 1
    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create master bias and dark frames grouped by temperature."
    )
    parser.add_argument(
        "--input-root",
        type=Path,
        required=True,
        help="Root folder containing 'bias/' and 'dark/' directories.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        required=True,
        help="Output folder where master files will be written.",
    )
    parser.add_argument(
        "--combine",
        choices=("median", "mean"),
        default="median",
        help="Combination method to build each master frame.",
    )
    parser.add_argument(
        "--output-format",
        choices=("npy", "fits"),
        default="npy",
        help="Output format for master files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    bias_groups = _collect_temperature_groups(args.input_root / "bias")
    dark_groups = _collect_temperature_groups(args.input_root / "dark")

    total_written = 0
    total_written += _build_masters(
        frame_kind="bias",
        groups=bias_groups,
        output_root=args.output_root,
        combine=args.combine,
        output_format=args.output_format,
    )
    total_written += _build_masters(
        frame_kind="dark",
        groups=dark_groups,
        output_root=args.output_root,
        combine=args.combine,
        output_format=args.output_format,
    )

    if total_written == 0:
        print("No supported frame files found in bias/ or dark/ folders.")
        return 1

    print(f"Done. Wrote {total_written} master file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

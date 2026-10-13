# Cloud-Gap Reconstruction from Satellite Observations

A deterministic multispectral reconstruction pipeline for cloud-contaminated satellite observations.

## Live dashboard

**https://cloud-gap-reconstruction.vercel.app/**

The live dashboard reads the real CSV files stored in this repository and lets you inspect the reconstruction pipeline pixel by pixel.

## Live features

- Loads `multispectral_observations.csv`
- Loads `cloud_masks.csv`
- Reads the configured cloud threshold
- Shows total / removed / reliable observation counts
- Select any pixel
- Select any spectral band
- Excludes high-cloud and shadow observations
- Detects `-999` missing values
- Applies linear interpolation
- Plots reconstructed time series
- Shows row-by-row quality and reconstructed values

## Original Python pipeline

The main reference implementation remains in:

```text
solution/solve.py
```

It generates:

- cleaned observations,
- reconstructed bands,
- uncertainty scores,
- holdout predictions,
- technical report.

The web dashboard is a visual explanation of the same cleaning and interpolation logic, not a replacement for the batch Python outputs.

## Run locally

```bash
cd web
python -m http.server 8000
```

Open `http://localhost:8000`.

The page fetches the public repository's data files, so internet access is required.

## Author

Sankalp Gupta  
GitHub: https://github.com/Sankalp-gupta1

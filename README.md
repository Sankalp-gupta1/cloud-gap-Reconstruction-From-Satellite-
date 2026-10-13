# Cloud-Gap Reconstruction from Satellite Observations

## Live app

**https://cloud-gap-reconstruction.vercel.app/**

The repository now includes a public browser reconstruction lab in `web/`.

The hosted demo lets you:
- paste multispectral observation CSV data,
- paste cloud-mask CSV data,
- change the cloud-probability threshold,
- remove cloud/shadow-contaminated observations,
- linearly interpolate missing spectral bands per pixel,
- inspect reconstructed rows,
- see a transparent uncertainty score based on the fraction of originally missing bands.

The browser version is deterministic and intentionally mirrors the documented reconstruction workflow. It does not claim calibrated satellite-production accuracy.

### Run the hosted-style demo locally

```bash
cd web
python -m http.server 8000
```

Open `http://localhost:8000`.

---

A deterministic multispectral reconstruction pipeline for cloud-contaminated satellite observations.

## Live dashboard

**https://cloud-gap-reconstruction-sankalp.vercel.app/**

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

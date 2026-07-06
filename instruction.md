# Reconstruction of Cloud-Contaminated Multispectral Environmental Observations

## Background
A climate and agricultural monitoring program has collected multispectral satellite observations from several forested and agricultural regions. Each observation contains measurements from multiple spectral bands used for vegetation monitoring, land-cover assessment, and environmental analysis.
During the observation period, persistent cloud cover and cloud shadows obscured portions of the imagery. As a result, several spectral measurements are incomplete or unreliable, limiting their use in downstream analyses such as vegetation monitoring, crop-yield estimation, and ecosystem assessment.
The monitoring team needs a reconstruction workflow that can identify cloud-affected observations, recover missing spectral measurements, estimate uncertainty, and generate complete observations for regions with incomplete records.
---
## Available Data

The environment provides the following input files.

### multispectral_observations.csv

Time-series multispectral observations for individual pixels.

The dataset contains fields such as:
- pixel_id
- timestamp
- region_id
- B2_blue
- B3_green
- B4_red
- B8_nir
- B11_swir1
Some spectral measurements may be incomplete because of cloud contamination.
---

### cloud_masks.csv
Cloud quality information corresponding to each observation.
The dataset contains fields such as:
- pixel_id
- timestamp
- cloud_probability
- shadow_flag
These values indicate observations that may require exclusion before reconstruction.
---
### region_metadata.csv
Static metadata describing each monitored region.
The dataset contains fields such as:
- region_id
- land_cover_type
- elevation
The metadata provides additional environmental context during reconstruction.
---

### holdout_regions.csv

A set of regions reserved for holdout evaluation.
These regions contain incomplete observations and should be processed using the same reconstruction workflow applied to the remaining dataset.

---

### reconstruction_config.json
Configuration parameters controlling the reconstruction workflow.
Representative parameters may include:

- maximum temporal reconstruction gap
- interpolation method
- uncertainty threshold
Configuration settings should be read directly from this file during execution.
---

## Objective

The reconstruction process is expected to:
- identify observations affected by cloud contamination
- exclude unreliable measurements from downstream analysis
- recover missing spectral information using a reproducible approach
- estimate uncertainty associated with reconstructed values
- generate outputs for the holdout regions
- summarize the overall reconstruction process and key findings
---

## Required Outputs

The solution must generate the following artifacts.

### cleaned_observations.csv

Filtered observations after removing measurements identified as unreliable because of cloud contamination.

---

### reconstructed_bands.csv

A reconstructed multispectral dataset containing complete spectral observations with all missing values appropriately addressed.

---

### uncertainty_scores.csv

Expected columns include:
- pixel_id
- timestamp
- uncertainty_value
- confidence_level
Each record should describe the estimated uncertainty associated with a reconstructed observation.

---

### holdout_predictions.csv

Reconstructed spectral observations generated for every region listed in the holdout dataset.

---

### report.md

A concise technical summary describing:
- observations processed
- observations removed during cleaning
- reconstruction approach
- summary of reconstructed observations
- uncertainty summary
- holdout reconstruction summary

---

## Constraints

- The workflow should remain reproducible when executed multiple times using the same inputs.
- Input files must remain unchanged throughout processing.
- Configuration settings should be read directly from `reconstruction_config.json` during execution.
- Missing observations should be handled without interrupting execution.
- Final reconstructed outputs should not contain unresolved spectral gaps.
- All required output artifacts should be written to the designated output locations.

---

## Evaluation Expectations

Evaluation will focus on:
- successful generation of all required output artifacts
- consistency of reconstructed spectral observations
- reasonable treatment of cloud-affected measurements
- complete processing of holdout regions
- meaningful uncertainty estimates
- adherence to the expected output requirements
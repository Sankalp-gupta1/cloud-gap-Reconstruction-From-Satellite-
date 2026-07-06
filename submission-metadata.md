# Platform submission form — Cloud-Contaminated Spectral Reconstruction

Not included in ZIP.

## Difficulty Explanation

The task requires combining cloud-quality information with temporal multispectral observations and reconstructing missing spectral values using deterministic methods. The workflow also includes uncertainty estimation and holdout-region processing, so mistakes in early filtering stages can affect multiple downstream outputs.

## Solution Explanation

The solution first identifies cloud-affected observations using the provided quality information, removes unreliable measurements, reconstructs missing spectral bands through a reproducible interpolation workflow, estimates uncertainty for reconstructed values, and generates predictions for holdout regions. The complete process produces the required output files and a final technical summary.

## Verification Explanation

The verification process checks that all required output artifacts are generated successfully, reconstructed datasets do not contain unresolved gaps, holdout predictions are produced, and the expected output structure is maintained across repeated executions.

## Workflow

Data science / ML

## Task Types

Data reconstruction; Signal reconstruction; Uncertainty estimation; Quality assessment

## Domain

Environmental Engineering

## Subdomains

Remote Sensing

## Skills

Reasoning; Processing Time-series Data; File Interaction; Tool-use; Long-horizon

## Tool Types

Scientific Computing Tools

## Number of Steps

36

## Expert time (minutes)

150

## Your submission time (minutes)

480
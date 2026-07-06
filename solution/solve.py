from pathlib import Path
import json
import pandas as pd
import numpy as np


ROOT_DIR = Path(__file__).resolve().parents[1]

# Docker default paths
DATA_DIR = Path("/app/data")
OUTPUT_DIR = Path("/app/output")

# Local development fallback
if not (DATA_DIR / "multispectral_observations.csv").exists():
    DATA_DIR = ROOT_DIR / "environment" / "data"
    OUTPUT_DIR = ROOT_DIR / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


BANDS = ["B2_blue", "B3_green", "B4_red", "B8_nir", "B11_swir1"]
MISSING_VALUE = -999


def load_inputs():
    observations = pd.read_csv(
        DATA_DIR / "multispectral_observations.csv"
    )

    cloud_masks = pd.read_csv(
        DATA_DIR / "cloud_masks.csv"
    )

    region_metadata = pd.read_csv(
        DATA_DIR / "region_metadata.csv"
    )

    holdout_regions = pd.read_csv(
        DATA_DIR / "holdout_regions.csv"
    )

    with open(
        DATA_DIR / "reconstruction_config.json",
        "r"
    ) as f:
        config = json.load(f)

    return (
        observations,
        cloud_masks,
        region_metadata,
        holdout_regions,
        config,
    )

def merge_cloud_information(observations, cloud_masks):
    merged = observations.merge(
        cloud_masks,
        on=["pixel_id", "timestamp"],
        how="left"
    )

    return merged

def mark_unreliable_observations(merged, config):
    cloud_threshold = config["cloud_threshold"]

    merged = merged.copy()

    merged["is_unreliable"] = (
        (merged["cloud_probability"] >= cloud_threshold)
        | (merged["shadow_flag"] == 1)
    )

    return merged

def create_cleaned_observations(merged):
    cleaned = merged[~merged["is_unreliable"]].copy()

    cleaned.to_csv(
        OUTPUT_DIR / "cleaned_observations.csv",
        index=False
    )

    return cleaned

def prepare_reconstruction_data(cleaned):
    reconstructed = cleaned.copy()

    for band in BANDS:
        reconstructed[band] = reconstructed[band].replace(
            MISSING_VALUE,
            np.nan
        )

    return reconstructed


def reconstruct_missing_bands(reconstructed):
    reconstructed = reconstructed.copy()

    reconstructed["timestamp"] = pd.to_datetime(
        reconstructed["timestamp"]
    )

    reconstructed = reconstructed.sort_values(
        ["pixel_id", "timestamp"]
    )

    for band in BANDS:
        reconstructed[band] = (
            reconstructed
            .groupby("pixel_id")[band]
            .transform(
                lambda x: x.interpolate(
                    method="linear",
                    limit_direction="both"
                )
            )
        )

    reconstructed.to_csv(
        OUTPUT_DIR / "reconstructed_bands.csv",
        index=False
    )

    return reconstructed

def generate_uncertainty_scores(reconstructed):
    uncertainty_records = []

    for pixel_id, group in reconstructed.groupby("pixel_id"):
        group = group.sort_values("timestamp")

        for _, row in group.iterrows():
            missing_count = sum(pd.isna(row[band]) for band in BANDS)

            if missing_count == 0:
                uncertainty = 0.05
                confidence = "high"
            elif missing_count == 1:
                uncertainty = 0.15
                confidence = "medium"
            else:
                uncertainty = 0.30
                confidence = "low"

            uncertainty_records.append(
                {
                    "pixel_id": row["pixel_id"],
                    "timestamp": row["timestamp"],
                    "uncertainty_value": uncertainty,
                    "confidence_level": confidence,
                }
            )

    uncertainty_df = pd.DataFrame(uncertainty_records)

    uncertainty_df.to_csv(
        OUTPUT_DIR / "uncertainty_scores.csv",
        index=False
    )

    return uncertainty_df

def generate_holdout_predictions(reconstructed, holdout_regions):
    holdout_ids = set(holdout_regions["region_id"].tolist())

    holdout_data = reconstructed[
        reconstructed["region_id"].isin(holdout_ids)
    ].copy()

    prediction_rows = []

    for region_id, group in holdout_data.groupby("region_id"):
        row = {"region_id": region_id}

        for band in BANDS:
            row[f"predicted_{band}"] = round(group[band].mean(), 6)

        prediction_rows.append(row)

    holdout_predictions = pd.DataFrame(prediction_rows)

    holdout_predictions.to_csv(
        OUTPUT_DIR / "holdout_predictions.csv",
        index=False
    )

    return holdout_predictions

def write_report(merged, cleaned, reconstructed, uncertainty_df, holdout_predictions):
    total_observations = len(merged)
    removed_observations = len(merged) - len(cleaned)
    reconstructed_observations = len(reconstructed)
    holdout_count = len(holdout_predictions)

    mean_uncertainty = round(
        uncertainty_df["uncertainty_value"].mean(),
        4
    )

    report = f"""# Cloud-Contaminated Spectral Reconstruction Report

Total observations processed: {total_observations}

Observations removed during cleaning: {removed_observations}

Reconstructed observations written: {reconstructed_observations}

Mean reconstruction uncertainty: {mean_uncertainty}

Holdout regions processed: {holdout_count}

The workflow merged multispectral observations with cloud-quality information, removed observations marked as unreliable, reconstructed missing spectral measurements, estimated uncertainty, and generated holdout-region predictions.
"""

    with open(OUTPUT_DIR / "report.md", "w") as f:
        f.write(report)




def main():
    (
        observations,
        cloud_masks,
        region_metadata,
        holdout_regions,
        config,
    ) = load_inputs()

    merged = merge_cloud_information(
        observations,
        cloud_masks,
    )

    merged = mark_unreliable_observations(
        merged,
        config,
    )

    cleaned = create_cleaned_observations(merged)

    reconstruction_data = prepare_reconstruction_data(
        cleaned
    )

    reconstructed = reconstruct_missing_bands(
        reconstruction_data
    )

    uncertainty_df = generate_uncertainty_scores(
        reconstructed
    )

    holdout_predictions = generate_holdout_predictions(
        reconstructed,
        holdout_regions,
    )

    write_report(
        merged,
        cleaned,
        reconstructed,
        uncertainty_df,
        holdout_predictions,
    )
    print("Pipeline completed successfully!")
    print("Output directory:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
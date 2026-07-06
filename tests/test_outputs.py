from pathlib import Path
import pandas as pd


OUTPUT_DIR = Path("/app/output")

REQUIRED_FILES = [
    "cleaned_observations.csv",
    "reconstructed_bands.csv",
    "uncertainty_scores.csv",
    "holdout_predictions.csv",
    "report.md",
]


def test_required_outputs_exist():
    for file_name in REQUIRED_FILES:
        file_path = OUTPUT_DIR / file_name
        assert file_path.exists(), f"{file_name} was not generated"


def test_reconstructed_bands_have_no_missing_values():
    reconstructed = pd.read_csv(OUTPUT_DIR / "reconstructed_bands.csv")

    band_columns = [
        "B2_blue",
        "B3_green",
        "B4_red",
        "B8_nir",
        "B11_swir1",
    ]

    for band in band_columns:
        assert not reconstructed[band].isna().any(), f"{band} contains NaN values"
        assert not (reconstructed[band] == -999).any(), f"{band} contains unresolved -999 values"


def test_holdout_predictions_include_all_regions():
    holdout = pd.read_csv(OUTPUT_DIR / "holdout_predictions.csv")

    expected_regions = {"R010", "R011", "R012"}
    actual_regions = set(holdout["region_id"])

    assert actual_regions == expected_regions


def test_uncertainty_scores_are_valid():
    uncertainty = pd.read_csv(OUTPUT_DIR / "uncertainty_scores.csv")

    assert "uncertainty_value" in uncertainty.columns
    assert "confidence_level" in uncertainty.columns

    assert uncertainty["uncertainty_value"].between(0, 1).all()

    allowed_confidence = {"high", "medium", "low"}
    assert set(uncertainty["confidence_level"]).issubset(allowed_confidence)


def test_report_is_not_empty():
    report_path = OUTPUT_DIR / "report.md"

    text = report_path.read_text().strip()

    assert len(text) > 100
    assert "Total observations processed" in text
    assert "Holdout regions processed" in text
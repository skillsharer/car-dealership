import pandas as pd

SELECTED_FEATURES = [
    "carname",
    "fueltype",
    "aspiration",
    "doornumber",
    "carbody",
    "drivewheel",
    "enginelocation",
    "wheelbase",
    "color",
    "carlength",
    "carwidth",
    "carheight",
    "curbweight",
    "cylindernumber",
    "enginesize",
    "compressionratio",
    "horsepower",
    "peakrpm",
    "citympg",
    "highwaympg",
    "price",
]

CRITICAL_COLUMNS = [
    "carname",
    "price",
]

BRAND_CORRECTIONS = {
    "maxda": "mazda",
    "porcsche": "porsche",
    "porcshce": "porsche",
    "toyouta": "toyota",
    "vokswagen": "volkswagen",
    "vw": "volkswagen"
}

def validate_required_columns(dataset: pd.DataFrame) -> None:
    missing_columns = [column for column in SELECTED_FEATURES if column not in dataset.columns]

    if missing_columns:
        raise ValueError(
            f"Input CSV is missing required columns: {missing_columns}"
        ) # Here if it would be in production, it would be better to use status codes.


def remove_rows_missing_critical_values(dataset: pd.DataFrame, critical_columns: list[str]) -> pd.DataFrame:
    return dataset.dropna(subset=critical_columns)


def preprocess_csv(input_path: str, output_path: str) -> None:
    dataset = pd.read_csv(input_path)

    dataset.columns = (dataset.columns.str.strip().str.lower())

    validate_required_columns(dataset)

    dataset['carname'] = (dataset['carname'].str.split().str[0].str.lower().replace(BRAND_CORRECTIONS))

    dataset = dataset[SELECTED_FEATURES].copy()

    dataset = remove_rows_missing_critical_values(
        dataset=dataset,
        critical_columns=CRITICAL_COLUMNS,
    )

    dataset.to_csv(output_path, index=False)

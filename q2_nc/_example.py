import pandas as pd


def samples_of_interest(metadata: pd.DataFrame) -> pd.Series:
    column = 'host_tax_id'
    value = '9606'
    return (metadata[column] == value)


def pivot_classification(labels: pd.Series) -> pd.DataFrame:
    df = pd.DataFrame(labels).reset_index()
    pivot = df.pivot(index='sample-id', columns='label',
                     values='label')
    return ~(pivot.isnull())

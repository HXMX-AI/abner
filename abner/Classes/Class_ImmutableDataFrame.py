import pandas as pd


class ImmutableDataFrame(pd.DataFrame):
    def __setitem__(self, key, value):
        if key in self.columns:
            super().__setitem__(key, value)
        else:
            raise ValueError("Cannot add new columns to this DataFrame")

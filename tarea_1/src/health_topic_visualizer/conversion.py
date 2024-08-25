import pandas as pd

from pandas import DataFrame


class DictToDataFrameConverter:
    @staticmethod
    def _attr_to_df(dicts: list[dict], attr: str, parent_pk: str, parent_prefix: str, attr_pk) -> DataFrame:
        dicts_with_attr = [d for d in dicts if attr in d]

        for d in dicts_with_attr:
            if not isinstance(d[attr], list):
                d[attr] = [d[attr]]

        attr_meta_df = pd.json_normalize(
            dicts_with_attr,
            record_path=attr,
            meta=[parent_pk],
            meta_prefix=parent_prefix
        )

        parent_pk_col_name = parent_prefix + parent_pk
        parent_pk_col = attr_meta_df.pop(parent_pk_col_name)
        attr_meta_df.insert(0, parent_pk_col_name, parent_pk_col)

        return attr_meta_df

    @staticmethod
    def _del_attr(dicts: list[dict], attr: str):
        return [{k: v for k, v in d.items() if k != attr} for d in dicts]

    @staticmethod
    def _standardize_df(df: DataFrame, pk_col_name: str) -> DataFrame:
        if pk_col_name == 'id':
            df['id'] = df['id'].astype(int)

        pk_col = df.pop(pk_col_name)
        df.insert(0, pk_col_name, pk_col)

        return df.sort_values(pk_col_name).reset_index(drop=True)

    @classmethod
    def _extract_attr_as_df(cls, dicts: list[dict], attr: str, parent_pk: str, parent_prefix: str, attr_pk) -> (
            list[dict], DataFrame):
        attr_meta_df = cls._attr_to_df(dicts, attr, parent_pk, parent_prefix, attr_pk)

        pruned_dicts = cls._del_attr(dicts, attr)

        attr_meta_df = cls._standardize_df(attr_meta_df, attr_pk)

        return pruned_dicts, attr_meta_df

    @classmethod
    def convert(cls, dicts: list[dict], root_name: str, attr_pks: list[(str, str)], root_pk: str = 'id') -> dict:
        """
        Returns a dict with the name of each attribute keying a corresponding un-normalized DataFrame
        """
        meta_prefix = root_name + '_'
        dataframes = {}
        for attr, attr_pk in attr_pks:
            (dicts, attr_meta_df) = cls._extract_attr_as_df(dicts, attr, root_pk, meta_prefix, attr_pk)
            dataframes[attr] = attr_meta_df

        root_df = cls._standardize_df(pd.json_normalize(dicts), root_pk)
        dataframes[root_name] = root_df
        return dataframes

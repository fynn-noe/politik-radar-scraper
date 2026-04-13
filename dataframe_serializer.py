from io import StringIO, BytesIO
from typing import List, Optional
import pandas as pd
from datetime import datetime
from dataclasses import dataclass

class DataframeSerializer:

    NO_RESULT_COLUMNS: List[str] = [
        "timestamp",
        "title",
        "medium_organisation",
        "content",
        "link",
        "source"
    ]

    @dataclass
    class Metadata:
        timestamp: datetime
        keywords: List[str]
        cos_threshold: Optional[float] = None

        def __str__(self) -> str:
            return f"""
# Abrufzeitpunkt: {self.timestamp.isoformat()}
# Schlagworte: {', '.join(self.keywords)}
# Ähnlichkeitsgrenzwert: {self.cos_threshold or 'NA'}
""".strip()

    def to_csv(self, df: pd.DataFrame, metadata: Metadata, add_metadata: bool, add_results: bool, add_keywords: bool) -> str:
        df_ = df.copy()

        cols = self.NO_RESULT_COLUMNS.copy()
        # Paywall is "ja" if link is empty and empty otherwise
        cols.append("Paywall")
        df_["Paywall"] = df_["link"].isna() | (df_["link"] == "")
        df_["Paywall"] = df_["Paywall"].map({True: "ja", False: ""})
        if add_results:
            result_cols = [col for col in df_.columns if col not in self.NO_RESULT_COLUMNS and col != "Stichwörter"]
            cols.extend(result_cols)

        if add_keywords and "Stichwörter" in df_.columns:
            cols.append("Stichwörter")

        df_ = df_[cols]
        if "Stichwörter" in df_.columns:
            df_["Stichwörter"] = df_["Stichwörter"].apply(
                lambda x: ", ".join(x) if isinstance(x, list) else x
            )
        io = StringIO()
        df_.to_csv(io, index=False)
        csv_string = io.getvalue()

        if add_metadata:
            csv_string = f"{metadata}\n{csv_string}"

        return csv_string

    def to_xlsx(self, df: pd.DataFrame , metadata: Metadata, add_metadata: bool, add_results: bool, add_keywords: bool) -> bytes:
        df_ = df.copy()
        cols = self.NO_RESULT_COLUMNS.copy()
        # Paywall is "ja" if link is empty and empty otherwise
        cols.append("Paywall")
        df_["Paywall"] = df_["link"].isna() | (df_["link"] == "")
        df_["Paywall"] = df_["Paywall"].map({True: "ja", False: ""})
        if add_results:
            result_cols = [col for col in df_.columns if col not in self.NO_RESULT_COLUMNS and col != "Stichwörter"]
            cols.extend(result_cols)

        if add_keywords and "Stichwörter" in df_.columns:
            cols.append("Stichwörter")

        df_ = df_[cols]
        if "Stichwörter" in df_.columns:
            df_["Stichwörter"] = df_["Stichwörter"].apply(
                lambda x: ", ".join(x) if isinstance(x, list) else x
            )
        io = BytesIO()
        with pd.ExcelWriter(io, engine="openpyxl") as writer:
            for source in df_["source"].unique():
                source_df = df_[df_["source"] == source]
                source_df.to_excel(writer, sheet_name=source, index=False)
            if add_metadata:
                metadata_df = pd.DataFrame({
                    "timestamp": metadata.timestamp,
                    "keywords": [metadata.keywords],
                    "cos_threshold": metadata.cos_threshold
                })
                metadata_df.to_excel(writer, sheet_name="metadata", index=False)
        return io.getvalue()
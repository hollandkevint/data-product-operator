"""Fetch and load the grader dataset: OHDSI Eunomia GiBleed, OMOP CDM 5.3.

The data is Synthea output: synthetic patients, no PHI. It is licensed
Apache-2.0 by OHDSI. The zip is pinned to one commit and one SHA-256, so every
clone grades against the same bytes. Nothing here is committed to the repo;
it lands in grader/.data/ (gitignored).
"""

from __future__ import annotations

import hashlib
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

COMMIT = "a11ad148a6b1b1fafb75a1e40c504c887db76fa4"
URL = f"https://raw.githubusercontent.com/OHDSI/EunomiaDatasets/{COMMIT}/datasets/GiBleed/GiBleed_5.3.zip"
SHA256 = "081b82e84c90e2904e02c26546e46412b01cce566071c77e0c4a355c2d0612f9"

HERE = Path(__file__).resolve().parent
DATA = HERE / ".data"
ZIP = DATA / "GiBleed_5.3.zip"
CSV_DIR = DATA / "GiBleed_5.3"
DB = DATA / "eunomia.duckdb"

TABLES = [
    "person", "observation_period", "visit_occurrence", "condition_occurrence",
    "drug_exposure", "drug_era", "condition_era", "procedure_occurrence",
    "measurement", "observation", "death", "concept", "concept_ancestor",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch() -> Path:
    """Download the pinned zip if absent and verify its checksum."""
    DATA.mkdir(exist_ok=True)
    if not ZIP.exists():
        print(f"downloading {URL}", file=sys.stderr)
        tmp = ZIP.with_suffix(".part")
        with urllib.request.urlopen(URL) as r, open(tmp, "wb") as f:
            shutil.copyfileobj(r, f)
        tmp.rename(ZIP)
    got = sha256(ZIP)
    if got != SHA256:
        ZIP.unlink()
        raise SystemExit(f"checksum mismatch: got {got}, want {SHA256}. Deleted the zip; rerun to refetch.")
    return ZIP


def build() -> Path:
    """Fetch, extract, and load the CSVs into a DuckDB file. Idempotent."""
    import duckdb

    if DB.exists():
        return DB
    fetch()
    with zipfile.ZipFile(ZIP) as z:
        for name in z.namelist():
            if name.startswith("GiBleed_5.3/") and name.endswith(".csv"):
                z.extract(name, DATA)
    tmp = DB.with_suffix(".part")
    if tmp.exists():
        tmp.unlink()
    con = duckdb.connect(str(tmp))
    for t in TABLES:
        con.execute(f"CREATE TABLE {t} AS SELECT * FROM read_csv_auto(?, header=true)", [str(CSV_DIR / f"{t.upper()}.csv")])
    con.close()
    tmp.rename(DB)
    return DB


def connect(read_only: bool = True):
    import duckdb

    return duckdb.connect(str(build()), read_only=read_only)


if __name__ == "__main__":
    print(build())

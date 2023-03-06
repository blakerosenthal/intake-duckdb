import duckdb
import numpy as np
import pandas as pd
import pytest

from .. import DuckDBSource

TEMP_TABLE = "temp"


@pytest.fixture(scope="module")
def connection(db):
    return duckdb.connect(db)


@pytest.fixture(scope="module")
def duckdb_source(db, connection, dataframe):
    connection.sql(f"CREATE TABLE {TEMP_TABLE} AS SELECT * FROM dataframe")
    sql_expr = f"SELECT * from {TEMP_TABLE}"
    return DuckDBSource(db, sql_expr)


@pytest.fixture(scope="module")
def dataframe():
    df = pd.DataFrame(
        {
            "a": np.random.rand(100).tolist(),
            "b": np.random.randint(100, size=100).tolist(),
            "c": np.random.choice(["a", "b", "c", "d"], size=100).tolist(),
        }
    )
    df.index.name = "p"

    return df


@pytest.fixture(scope="module")
def db(tmp_path_factory):
    return str(tmp_path_factory.mktemp("db") / "test.duckdb")
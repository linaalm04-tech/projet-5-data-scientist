
from unittest.mock import MagicMock

import pandas as pd
import pytest

from src import import_employees as module

def test_csv_vide(monkeypatch):
    monkeypatch.setattr(module, "Path", MagicMock())
    monkeypatch.setattr(
        module.pd,
        "read_csv",
        lambda path: pd.DataFrame(),
    )

    with pytest.raises(ValueError, match="ne contient aucune donnée"):
        module.import_employees()


def test_import_annule_si_employes_existants(monkeypatch, capsys):
    monkeypatch.setattr(module, "Path", MagicMock())
    monkeypatch.setattr(
        module.pd,
        "read_csv",
        lambda path: pd.DataFrame({"age": [30]}),
    )

    connection = MagicMock()
    connection.execute.return_value.scalar_one.return_value = 1470

    transaction = MagicMock()
    transaction.__enter__.return_value = connection
    monkeypatch.setattr(module.engine, "begin", lambda: transaction)

    module.import_employees()

    assert "Import annulé" in capsys.readouterr().out
    connection.execute.assert_called_once()


def test_csv_introuvable_avec_faux_path(monkeypatch):
    class FauxPath:
        def __init__(self, *args):
            pass

        def resolve(self):
            return self

        @property
        def parent(self):
            return self

        def __truediv__(self, other):
            return self

        def exists(self):
            return False

    monkeypatch.setattr(module, "Path", FauxPath)

    with pytest.raises(FileNotFoundError):
        module.import_employees()

def test_import_si_table_vide(monkeypatch, capsys):
    df = pd.DataFrame({"age": [30]})

    monkeypatch.setattr(module, "Path", MagicMock())
    monkeypatch.setattr(module.pd, "read_csv", lambda path: df)

    connection = MagicMock()
    connection.execute.return_value.scalar_one.return_value = 0

    transaction = MagicMock()
    transaction.__enter__.return_value = connection
    monkeypatch.setattr(module.engine, "begin", lambda: transaction)

    to_sql_calls = []
    monkeypatch.setattr(
        pd.DataFrame,
        "to_sql",
        lambda self, *args, **kwargs: to_sql_calls.append((args, kwargs)),
    )

    module.import_employees()

    assert len(to_sql_calls) == 1
    assert "1 employés importés" in capsys.readouterr().out
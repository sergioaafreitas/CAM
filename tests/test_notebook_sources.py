import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_notebook_source(notebook_name: str) -> str:
    notebook_path = REPO_ROOT / "src" / notebook_name
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    source_chunks = []

    for cell in notebook["cells"]:
        source = cell.get("source", [])
        if isinstance(source, list):
            source_chunks.extend(source)
        else:
            source_chunks.append(source)

    return "".join(source_chunks)


def test_requirements_cover_notebook_dependencies():
    requirements = (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8")

    assert "seaborn" in requirements
    assert "minisom" in requirements


def test_notebooks_do_not_depend_on_fixed_relative_paths():
    notebook_names = [
        "6.0 - lasso regression.ipynb",
        "6.0 - ridge regression.ipynb",
        "7.0 - rbf_regression.ipynb",
        "8.0 - logistic_regression.ipynb",
        "8.1 - saude cardiaca.ipynb",
        "9.0 - iris_dataset.ipynb",
        "14.1 - Kmeans.ipynb",
        "14.2 - Gauss.ipynb",
    ]

    for notebook_name in notebook_names:
        source = read_notebook_source(notebook_name)
        assert "../data/" not in source
        assert "resolve_data_path" in source


def test_local_notebook_datasets_exist():
    dataset_names = [
        "6.0 - dados_lasso_regression.csv",
        "6.0 - dados_ridge_regression.csv",
        "7.0 - dados_rbf_regression.csv",
        "8.0 - dados_logistic_regression.csv",
        "8.1 - dados_saude_cardiaca.csv",
        "9.0 - iris_dataset.csv",
        "14.1 - customer_data.csv",
    ]

    for dataset_name in dataset_names:
        assert (REPO_ROOT / "data" / dataset_name).exists()


def test_german_credit_notebook_uses_local_cache_before_remote():
    source = read_notebook_source("13.1 - LDA german credit data.ipynb")

    assert "resolve_data_path" in source
    assert "13.1 - german_credit_data.data" in source
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


def test_logistic_regression_accuracy():
    path = 'data/8.0 - dados_logistic_regression.csv'
    df = pd.read_csv(path)

    # check columns
    assert list(df.columns) == ['Feature1', 'Feature2', 'Target']

    X = df[['Feature1', 'Feature2']]
    y = df['Target']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    assert accuracy > 0.8


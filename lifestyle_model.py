import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression


def train_model():

    df = pd.read_excel("LifestyleDisease_ComplexRisk.xlsx")

    X = df.drop("Risk", axis=1)
    y = df["Risk"]

    num_features = ["Age","Height(cm)","Weight(kg)","SleepHours","StressLevel","BMI"]
    cat_features = ["Gender","Occupation","Diet","JunkFood","Smoking","Alcohol","FamilyHistory"]

    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), num_features),
        ("cat", OneHotEncoder(drop="first"), cat_features)
    ])

    model = Pipeline([
        ("preprocessing", preprocessor),
        ("classifier", LogisticRegression(max_iter=100))
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model.fit(X_train, y_train)

    print("Model accuracy:", model.score(X_test, y_test))

    return model

import pandas as pd

df = pd.read_csv("substitution_dataset.csv")
print(df.head())
print(df.shape)
df_encoded = pd.get_dummies(df, columns=["team"])
print(df_encoded.head())
print(df_encoded.shape)
X = df_encoded.drop("sub_happens", axis=1)
y = df_encoded["sub_happens"]

print(X.shape)
print(y.shape)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train.shape)
print(X_test.shape)
from sklearn.tree import DecisionTreeClassifier
tree_model = DecisionTreeClassifier(random_state=42, class_weight='balanced', max_depth=8)
tree_model.fit(X_train, y_train)
y_pred_tree = tree_model.predict(X_test)
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
print("=== Decision Tree ===")
print("Accuracy:", accuracy_score(y_test, y_pred_tree))
print(confusion_matrix(y_test, y_pred_tree))
print(classification_report(y_test, y_pred_tree))
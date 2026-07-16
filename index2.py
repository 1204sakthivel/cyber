# ============================================
# PHISHING EMAIL DETECTION USING LOGISTIC REGRESSION
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# -------------------------------
# Load Dataset
# -------------------------------
try:
    df = pd.read_csv("emails.csv")
except:
    print("Error: emails.csv not found.")
    exit()

print("\nColumns in Dataset:")
print(df.columns)

# -------------------------------
# Change these if your dataset has
# different column names
# -------------------------------
TEXT_COLUMN = "Email Text"
LABEL_COLUMN = "Email Type"

X = df[TEXT_COLUMN].fillna("")
y = df[LABEL_COLUMN]

# -------------------------------
# Convert Text to Numerical Values
# -------------------------------
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(X)

# -------------------------------
# Split Dataset
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -------------------------------
# Train Logistic Regression Model
# -------------------------------
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# -------------------------------
# Prediction
# -------------------------------
y_pred = model.predict(X_test)

# -------------------------------
# Accuracy
# -------------------------------
accuracy = accuracy_score(y_test, y_pred)

print("\n==============================")
print("MODEL ACCURACY")
print("==============================")
print("Accuracy : {:.2f}%".format(accuracy * 100))

print("\nClassification Report")
print(classification_report(y_test, y_pred))

# -------------------------------
# Confusion Matrix
# -------------------------------
cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix")
print(cm)

plt.figure(figsize=(5,5))
plt.imshow(cm, cmap="Blues")
plt.title("Confusion Matrix")
plt.colorbar()

classes = model.classes_

plt.xticks(range(len(classes)), classes)
plt.yticks(range(len(classes)), classes)

for i in range(len(cm)):
    for j in range(len(cm[0])):
        plt.text(j, i, cm[i][j],
                 ha="center",
                 va="center",
                 color="black")

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# -------------------------------
# Predict New Email
# -------------------------------
print("\n===================================")
print("PHISHING EMAIL DETECTOR")
print("===================================")

while True:

    email = input("\nEnter Email (type EXIT to quit):\n")

    if email.lower() == "exit":
        print("Program Closed.")
        break

    email_vector = vectorizer.transform([email])

    result = model.predict(email_vector)[0]

    print("\nPrediction :", result)

    if result.lower() == "phishing":
        print("⚠ Warning! This email looks like a PHISHING email.")
    else:
        print("✅ This email appears SAFE.")
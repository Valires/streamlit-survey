# Adapted from https://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html
# License: BSD 3 clause

# Standard scientific Python imports
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

# Import datasets, classifiers and performance metrics
from sklearn import datasets, metrics, svm
from sklearn.model_selection import train_test_split

# Load the digits dataset
digits = datasets.load_digits()

# flatten the images
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# Create a classifier: a support vector classifier
model_name = "My model"
model_version = "1.0"
clf = svm.SVC(gamma=0.001)

# Split data into 50% train and 50% test subsets
X_train, X_test, y_train, y_test = train_test_split(data, digits.target, test_size=0.5, shuffle=False)

# Learn the digits on the train subset
clf.fit(X_train, y_train)

# Predict the value of the digit on the test subset
predicted = clf.predict(X_test)


def make_plot(case_id):
    image = X_test[case_id].reshape(8, 8)
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.imshow(image, cmap=plt.cm.gray_r, interpolation="nearest")
    ax.set_title(f"Prediction: {predicted[case_id]}")
    return fig


def analysis_plot(survey_data):
    keywords = [data["value"] for data in survey_data.values()]
    series = sum([xx.split("\n") for xx in keywords], [])
    fig = px.histogram(series)
    fig.update_layout(title="Keyword Frequency")
    return fig

# Insulin-Dosage-Prediction
This project predicts insulin dosage and risk of hypoglycemia using a hybrid ANN + RNN model. It takes inputs like sugar level, prescribed dose, and calorie intake, and predicts adjusted insulin doses for meals, ensuring accurate and personalized diabetes management.

# Overview
This project focuses on predicting the insulin dose required for diabetic patients and assessing the risk of hypoglycemia after meals using a hybrid ANN + RNN deep learning model. The goal is to provide an accurate and personalized insulin adjustment recommendation to help in better diabetes management.

# Workflow
Input Collection
Users provide details such as:

Sugar Level (before meal)

Prescribed Insulin Dose

Calorie Intake

# Model Prediction
A hybrid Artificial Neural Network (ANN) and Recurrent Neural Network (RNN) model processes the inputs to:

Predict the after-meal sugar level.

Determine if the patient is at risk of hypoglycemia.

Suggest an adjusted insulin dose if necessary.

# Evaluation
The model's performance is evaluated using metrics such as Mean Absolute Error (MAE), Root Mean Square Error (RMSE), and R² Score.

Deployment
The system is deployed as a Python Flask web application, where users can input their details, get real-time predictions, and view their history.

# Technologies Used
Python

TensorFlow / Keras

Flask (for the web app)

Pandas, NumPy

Matplotlib, Seaborn

Features
Predicts insulin dosage per meal (breakfast, lunch, dinner).

Assesses hypoglycemia risk post-meal.

Suggests personalized dosage adjustments.

Saves prediction history for each user.

# Performance Metrics
Mean Absolute Error (MAE)

Root Mean Square Error (RMSE)

R² Score

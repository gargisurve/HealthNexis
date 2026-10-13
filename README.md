# HealthNexis — Cloud-Integrated Lifestyle Disease Risk Prediction and Monitoring System Using ML

HealthNexis is a cloud-integrated web application developed to estimate lifestyle disease risk using machine learning. The system collects lifestyle and health-related parameters, processes them through a trained Logistic Regression model, and presents risk estimates through an interactive interface.

The project combines machine learning, web development, database management, and cloud computing to demonstrate a practical implementation of predictive analytics.

## Project Overview

Lifestyle-related health risks can be influenced by factors such as diet, physical activity, sleep, stress, smoking, alcohol consumption, and family medical history.

HealthNexis uses these inputs to generate an estimated risk score and categorize the result into low, moderate, or high risk according to the application's configured thresholds.

**Important:** HealthNexis is an academic demonstration project. Its outputs are not medical diagnoses and should not replace professional medical assessment.

## Key Features

### 1. Lifestyle Risk Assessment
- Collects health and lifestyle parameters through a web form.
- Processes numerical and categorical inputs.
- Generates a predicted risk score using the trained machine learning pipeline.

### 2. Machine Learning
- Uses Logistic Regression for classification.
- Applies numerical feature scaling and categorical feature encoding.
- Processes input features through a Scikit-learn pipeline.
- Displays an approximate model accuracy of 90% as reported in the project report.

### 3. Risk Analysis
- Categorizes predicted risk into low, moderate, and high levels.
- Displays important risk-related features based on the model coefficients.
- Provides population-average comparisons when database records are available.
- Presents general lifestyle recommendations based on configured risk thresholds.

### 4. PDF Report Generation
- Generates a downloadable assessment report.
- Includes the predicted risk score, risk category, input summary, and recommendation.

### 5. Database Integration
- Uses MySQL to store prediction records and associated input parameters.
- Supports retrieval of assessment history and aggregate statistics.

### 6. Administrative Dashboard
- Displays assessment counts and average predicted risk.
- Visualizes risk distribution using charts.
- Provides an administrative interface for viewing analytics.

### 7. Cloud Deployment
- Uses Amazon EC2 to host the web application.
- Uses Amazon RDS for cloud-hosted database management.
- Demonstrates the integration of machine learning with cloud infrastructure.

## Technology Stack

| Component | Technologies |
|---|---|
| Programming language | Python |
| Backend | Flask |
| Frontend | HTML, CSS, JavaScript |
| Machine learning | Scikit-learn, Logistic Regression |
| Data processing | Pandas |
| Database | MySQL |
| Cloud infrastructure | AWS EC2, Amazon RDS |
| PDF reports | ReportLab |
| Data visualization | Chart.js |

## Machine Learning Methodology

The machine learning workflow consists of the following stages:

1. **Data collection:** Uses a lifestyle dataset containing health and lifestyle attributes.
2. **Data preprocessing:** Prepares the dataset for model training.
3. **Feature processing:** Applies `StandardScaler` to numerical features and `OneHotEncoder` to categorical features.
4. **Model training:** Trains a Logistic Regression classifier using a Scikit-learn pipeline.
5. **Model evaluation:** Evaluates performance on a held-out test split.
6. **Prediction:** Processes user inputs to generate a predicted class and probability-based risk score.
7. **Result presentation:** Displays the result and generates a downloadable PDF report.

The reported accuracy is approximately 90%, as stated in the academic project report. Performance may vary with the dataset, validation method, and deployment conditions.

## Project Workflow

Lifestyle Input → Data Processing → Logistic Regression Pipeline → Risk Estimate → Result Dashboard → PDF Report

Prediction records are stored in the MySQL database to support history retrieval and administrative analytics.

## Research Publication

The HealthNexis project report identifies the following related research work:

**Title:** Applications of AI and Machine Learning in Predictive Healthcare and Personalized Medicine: Insights from Lifestyle Disease Data

**Publication date:** December 2025

This project translates concepts explored in the research work into a practical web application integrating predictive analytics, database management, and cloud infrastructure.

*Add the publication venue, author list, DOI, or official publication URL here once verified.*

## Limitations

- The model's performance depends on the quality and representativeness of its training data.
- A predicted risk score is not a clinically validated diagnosis.
- The reported accuracy requires independent evaluation before any real-world healthcare use.
- Secure deployment requires appropriate authentication, access control, database protection, and privacy safeguards.

## Future Scope

- Evaluate the model on independent and representative datasets.
- Improve model validation and performance reporting.
- Strengthen authentication and database security.
- Improve accessibility and the user experience.
- Extend monitoring and analytics capabilities.

## Academic Project

**Project:** HealthNexis — Cloud-Integrated Lifestyle Disease Risk Prediction and Monitoring System Using ML

**Author:** Gargi Ashish Surve

**Project Guide:** Prof. Radhika Fulzele

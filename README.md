# Loan Prediction Application

## Project Overview

The Loan Prediction Application leverages Big Data technologies and machine learning to predict the approval status of loan applications. It processes applicant data in real-time, providing precise predictions using advanced models. The system is designed for scalability, reliability, and secure data handling, fully deployed on Google Cloud Platform (GCP).

---

## Objectives

- **Efficient Data Management**: Handle large datasets in distributed environments.
- **Scalability**: Support increasing loan application volumes with cloud resource scaling.
- **Real-Time Processing**: Process data instantly using GCP services like Pub/Sub and Firestore.
- **Model Optimization**: Enhance accuracy with Random Forest and Gradient Boosting models.
- **Security**: Ensure secure data transmission and storage.

---

## System Architecture
![image](https://github.com/user-attachments/assets/508e7bb6-b731-461b-965f-1ceedb6ca04c)

### Data Flow
1. **User Input**: Loan application data is submitted through a web app.
2. **Data Messaging**: Backend sends data to a Pub/Sub topic for processing.
3. **Prediction Processing**: Google Cloud Functions trigger ML model predictions.
4. **Storage**: Results stored in Firestore under a unique application ID.
5. **Result Retrieval**: Predictions are displayed to users in real-time.

### Technical Components
- **Frontend**: User-friendly web interface for data submission and result display.
- **Backend**:
  - **Google Cloud Pub/Sub**: Message broker for asynchronous data processing.
  - **Google Cloud Functions**: Prediction processing and storage.
  - **Google Firestore**: Real-time data syncing and storage.

---

## Features

### Dataset
Key features include:
- Gender, Marital Status, Dependents, Education, Employment, Loan Amount, Loan Term, Credit History, Property Area, Total Income.

### Prediction Results
- Loan approval probability (e.g., 85%)
- Risk category (e.g., Low Risk)

---

## Technology Stack

### Backend
- **Python**: ETL and data processing scripts.
- **Flask**: Web framework for dashboard and API.
- **Pandas**: Data manipulation and analysis.

### Machine Learning
- Random Forest and Gradient Boosting models for classification.

### Cloud Services
- **Google Cloud Functions**: Event-driven data processing.
- **Google Pub/Sub**: Data messaging.
- **Google Firestore**: Real-time database.

---

## Deployment

The application is deployed on **Google Cloud Platform** using services like Cloud Functions, Pub/Sub, and Firestore. It supports real-time processing and secure data handling.

---

## Future Enhancements

- **Advanced Analytics**: Integrate BI tools like Tableau for visualization.
- **Streaming**: Use tools like Apache Flink for instant predictions.
- **Security**: Implement stricter IAM policies and data encryption.
- **Alerts**: Email notifications for anomalies or processing failures.

---

## Contributors

- **Pavani Racham (G23AI2032)**
- **Naresh Krishna Vemuri (G23AI2025)**
- **Neha Challa (G23AI2067)**

Under the guidance of **Dr. Dip Sankar Banerjee**, Department of Artificial Intelligence, IIT Jodhpur.

---

## Conclusion

This project demonstrates a scalable, efficient, and secure application for loan prediction, addressing key challenges in Big Data processing and machine learning.

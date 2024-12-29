from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_cors import CORS
import json
import uuid
from google.cloud import pubsub_v1
import os
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.secret_key = 'your-secret-key-here'  # Required for flashing messages

# Configure Pub/Sub
project_id = "vccproject-436306"
publisher = pubsub_v1.PublisherClient()

# Map numeric values to string values
GENDER_MAP = {0: 'Male', 1: 'Female'}
MARRIED_MAP = {0: 'No', 1: 'Yes'}
DEPENDENTS_MAP = {0: '0', 1: '1', 2: '2', 3: '3+'}
EDUCATION_MAP = {0: 'Not Graduate', 1: 'Graduate'}
SELF_EMPLOYED_MAP = {0: 'No', 1: 'Yes'}
PROPERTY_AREA_MAP = {0: 'Urban', 1: 'Rural', 2: 'Semiurban'}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            # Generate a unique request ID
            request_id = str(uuid.uuid4())
            
            # Get form data and map to string values
            data = {
                'request_id': request_id,
                'gender': GENDER_MAP[int(request.form['gender'])],
                'married': MARRIED_MAP[int(request.form['married'])],
                'dependents': DEPENDENTS_MAP[int(request.form['dependents'])],
                'education': EDUCATION_MAP[int(request.form['education'])],
                'self_employed': SELF_EMPLOYED_MAP[int(request.form['self_employed'])],
                'loan_amount': request.form['loan_amount'],
                'loan_amount_term': request.form['loan_amount_term'],
                'credit_history': request.form['credit_history'],
                'property_area': PROPERTY_AREA_MAP[int(request.form['property_area'])],
                'total_income': request.form['total_income']
            }
            
            # Publish message to Pub/Sub
            topic_path = publisher.topic_path(project_id, 'loan-applications')
            message_data = json.dumps(data).encode('utf-8')
            
            try:
                # Publish message
                publish_future = publisher.publish(topic_path, message_data)
                message_id = publish_future.result()  # Wait for message to be published
                flash('Loan application submitted successfully! Request ID: ' + request_id, 'success')
                print(f"Published message with ID: {message_id}")
            except Exception as e:
                app.logger.error(f"Error publishing message: {str(e)}")
                flash('Error submitting loan application. Please try again.', 'error')
                
        except Exception as e:
            app.logger.error(f"Error processing form data: {str(e)}")
            flash('Error processing form data. Please check your inputs.', 'error')
        
        return redirect(url_for('home'))
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

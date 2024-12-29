import base64
import json
import pandas as pd
import pickle
import functions_framework
import traceback
import logging
from google.cloud import firestore
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('function.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Firestore client
db = firestore.Client()

@functions_framework.cloud_event
def hello_pubsub(cloud_event):
    """
    Cloud Function triggered by a Cloud Pub/Sub event.
    Args:
        cloud_event: The Cloud Event that triggered this function
    """
    try:
        if not cloud_event.data:
            msg = "No data received in cloud event"
            logger.error(msg)
            return msg, 400
            
        # Decode the Pub/Sub message
        pubsub_message = base64.b64decode(cloud_event.data["message"]["data"]).decode()
        logger.info(f"Received Pub/Sub message: {pubsub_message}")
        
        try:
            data = json.loads(pubsub_message)
            logger.info(f"Parsed JSON message: {data}")
        except json.JSONDecodeError:
            msg = "Invalid JSON format in message"
            logger.error(msg)
            return msg, 400

        try:
            # Create DataFrame with the same structure as training data
            df = pd.DataFrame({
                'Gender': [1 if data['gender'].lower() == 'female' else 0],
                'Married': [1 if data['married'].lower() == 'yes' else 0],
                'Dependents': [3 if str(data['dependents']) == '3+' else int(data['dependents'])],
                'Education': [1 if data['education'].lower() == 'graduate' else 0],
                'Self_Employed': [1 if data['self_employed'].lower() == 'yes' else 0],
                'LoanAmount': [float(data['loan_amount'])],
                'Loan_Amount_Term': [float(data['loan_amount_term'])],
                'Credit_History': [int(data['credit_history'])],
                'Property_Area': [{'urban': 0, 'rural': 1, 'semiurban': 2}[data['property_area'].lower()]],
                'Total_Income': [float(data['total_income'])]
            })
            logger.info(f"Created DataFrame: {df.to_dict()}")
        except KeyError as e:
            msg = f"Missing required field: {str(e)}"
            logger.error(msg)
            return msg, 400
        except ValueError as e:
            msg = f"Invalid value in data: {str(e)}"
            logger.error(msg)
            return msg, 400

        try:
            # Load model and make prediction
            logger.info('Loading model...')
            try:
                with open('rfc.pkl', 'rb') as file:
                    model = pickle.load(file)
                logger.info('Model loaded successfully')
            except FileNotFoundError:
                error_message = "Model file 'rfc.pkl' not found in the current directory"
                logger.error(error_message)
                return error_message, 500
            except Exception as e:
                error_message = f"Error loading model: {str(e)}\n{traceback.format_exc()}"
                logger.error(error_message)
                return error_message, 500
            
            prediction = bool(model.predict(df)[0])
            prediction_proba = float(model.predict_proba(df)[0][1])  # Probability of approval
            logger.info(f'Prediction: {prediction}, Probability: {prediction_proba}')
            
            response = {
                'loan_approved': prediction,
                'approval_probability': prediction_proba,
                'request_id': data.get('request_id', '')
            }
            
            # Store prediction data in Firestore
            try:
                predictions_ref = db.collection('loan_predictions')
                prediction_data = {
                    'request_id': data.get('request_id', ''),
                    'loan_approved': prediction,
                    'approval_probability': prediction_proba,
                    'input_data': data,
                    'timestamp': datetime.now(),
                }
                predictions_ref.add(prediction_data)
                logger.info(f"Prediction data stored in Firestore with request_id: {data.get('request_id', '')}")
            except Exception as e:
                logger.error(f"Error storing data in Firestore: {str(e)}")
                # Continue execution even if database storage fails
                pass
            
            return json.dumps(response), 200
            
        except Exception as e:
            error_message = f"Error in model prediction: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_message)
            return error_message, 500
        
    except Exception as e:
        error_message = f"Error processing Pub/Sub message: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_message)
        return error_message, 500

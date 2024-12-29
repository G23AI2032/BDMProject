import functions_framework
from google.cloud import firestore
from flask import jsonify
import logging

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

@functions_framework.http
def fetch_predictions(request):
    """
    HTTP Cloud Function to fetch prediction data from Firestore.
    Args:
        request (flask.Request): The request object
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
    """
    try:
        # Set CORS headers for the preflight request
        if request.method == 'OPTIONS':
            # Allows GET requests from any origin with the Content-Type
            # header and caches preflight response for 3600s
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '3600'
            }
            return ('', 204, headers)

        # Set CORS headers for the main request
        headers = {
            'Access-Control-Allow-Origin': '*'
        }

        # Get query parameters
        request_id = request.args.get('request_id')
        limit = request.args.get('limit', default=10, type=int)

        # Query Firestore
        predictions_ref = db.collection('loan_predictions')
        
        if request_id:
            # Fetch specific prediction by request_id
            query = predictions_ref.where('request_id', '==', request_id)
        else:
            # Fetch latest predictions
            query = predictions_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit)

        # Execute query
        docs = query.stream()
        
        # Convert to list of dictionaries
        predictions = []
        for doc in docs:
            prediction_data = doc.to_dict()
            # Convert timestamp to string for JSON serialization
            if 'timestamp' in prediction_data:
                prediction_data['timestamp'] = prediction_data['timestamp'].isoformat()
            predictions.append(prediction_data)

        logger.info(f"Successfully fetched {len(predictions)} predictions")
        
        return (jsonify(predictions), 200, headers)

    except Exception as e:
        error_message = f"Error fetching predictions: {str(e)}"
        logger.error(error_message)
        return (jsonify({'error': error_message}), 500, headers)

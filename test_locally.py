import base64
import json
import requests

# Sample loan application data
test_data = {
    "gender": "Male",
    "married": "Yes",
    "dependents": "2",
    "education": "Graduate",
    "self_employed": "No",
    "loan_amount": "140",
    "loan_amount_term": "360",
    "credit_history": "1",
    "property_area": "Urban",
    "total_income": "5849",
    "request_id": "test-123"
}

# Convert to JSON and encode in base64
json_data = json.dumps(test_data)
message_data = base64.b64encode(json_data.encode()).decode()

# Create Cloud Event message structure
pubsub_message = {
    "message": {
        "data": message_data
    }
}

# Send request to local Functions Framework server
try:
    response = requests.post(
        "http://localhost:8080",  # Default Functions Framework port
        json=pubsub_message,
        headers={
            "Content-Type": "application/json",
            "ce-id": "123451234512345",
            "ce-specversion": "1.0",
            "ce-time": "2020-01-02T12:34:56.789Z",
            "ce-type": "google.cloud.pubsub.topic.v1.messagePublished",
            "ce-source": "//pubsub.googleapis.com/projects/sample-project/topics/gcf-test"
        }
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {str(e)}")

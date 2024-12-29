from google.cloud import pubsub_v1
import json
import time

# Initialize the Pub/Sub publisher client
publisher = pubsub_v1.PublisherClient()

# Your Google Cloud project ID and Pub/Sub topic name
project_id = "vccproject-436306"
topic_name = "loan-applications"
topic_path = publisher.topic_path(project_id, topic_name)

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
    "request_id": f"test-{int(time.time())}"  # Unique request ID
}

# Convert the message to JSON string
message_json = json.dumps(test_data)
message_bytes = message_json.encode('utf-8')

try:
    # Publish the message
    future = publisher.publish(topic_path, message_bytes)
    message_id = future.result()
    print(f"Message published with ID: {message_id}")
    print(f"Test data sent: {test_data}")
except Exception as e:
    print(f"An error occurred: {e}")

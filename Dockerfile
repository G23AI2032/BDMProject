# Use an official Python runtime as a parent image
FROM python:3.9.0-slim

# Set the working directory in the container
WORKDIR /DEPLOYML
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



# Copy the current directory contents into the container at /app
COPY . .

EXPOSE 5000
# Run app.py when the container launches
CMD ["python", "app.py"]

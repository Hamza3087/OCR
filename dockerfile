# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Set the environment variable to tell Flask it's running in production
ENV FLASK_ENV=production

# Expose port 5000 for the app to run
EXPOSE 5000

# Define the command to run your Flask app
CMD ["flask", "run", "--host=0.0.0.0"]

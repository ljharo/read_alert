# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Expose the port the app runs on (if any, though telegram bots usually don't need this unless it's a webhook bot)
# In this case, it's a long-polling bot, so no port needs to be exposed for inbound connections.
# But it's good practice to have it commented out if needed later.
# EXPOSE 80

# Run main.py when the container launches
CMD ["python", "main.py"]
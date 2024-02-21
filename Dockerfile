# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --default-timeout=120 -r requirements.txt

ENV MODEL_BASE_PATH /app/Models/

EXPOSE 5000


# Run app.py when the container launches
CMD ["python", "app.py"]


# Python image
FROM python:latest

# Set the working directory
WORKDIR /app

# Copy the local working directory contents into the container at /app
COPY . /app

# Create virtual environment and install dependencies
RUN pip install --upgrade pip
RUN pip install .

# Run app.py when the container launches
CMD ["swpc_monitoring"]

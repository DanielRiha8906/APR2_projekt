FROM python:3.10-alpine

# Set working directory
WORKDIR /

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD python app.py

FROM python:3.11

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install other necessary tools
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && apt-get clean

# Set the working directory
WORKDIR /workspace
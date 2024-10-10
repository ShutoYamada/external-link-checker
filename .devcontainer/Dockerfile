FROM python:3.11

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Chrome and ChromeDriver for Selenium
RUN apt-get update && apt-get install -y \
    curl \
    git \
    chromium \
    chromium-driver \
    fonts-noto-cjk \
    && apt-get clean

# Install Selenium
RUN pip install selenium
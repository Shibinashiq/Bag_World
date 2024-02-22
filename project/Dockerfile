# Use an image with Python  3.9 installed
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE  1
ENV PYTHONUNBUFFERED  1

# Create the working directory and set it as the working directory
RUN mkdir -p /watch web/project/project
WORKDIR /watch web/project/project

# Copy only the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run migrations (if applicable)
CMD ["python", "manage.py", "migrate"]

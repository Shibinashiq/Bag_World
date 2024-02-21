# Use the official Python image as a base image
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /watch web/project/project

# Copy only the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run migrations
CMD ["python", "manage.py", "migrate"]

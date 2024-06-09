# Description: Dockerfile for the FastAPI app
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

# Set the working directory in the container
WORKDIR /app

# Copy the FastAPI app to the container
COPY . /app/

# Copy the FastAPI app to the container
COPY gunicorn_conf.py /app/gunicorn_conf.py
# Copy the requirements file to the container
COPY requirements.txt /app/requirements.txt
# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt     

# Expose port 8000
EXPOSE 80
# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "app.app:app", "--host", "localhost", "--port", "80"]



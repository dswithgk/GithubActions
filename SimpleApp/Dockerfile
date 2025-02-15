# Use the official Python image
FROM python:3.10  

# Set the working directory
WORKDIR /app  

# Copy only requirements file first (for caching dependencies)
COPY requirements.txt .  

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt  

# Copy all files except .github (handled via .dockerignore)
COPY . .  

# Expose the port FastAPI runs on
EXPOSE 8000  

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]  


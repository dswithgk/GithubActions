## Host API In EC2
---

## **Step 1: Write a Dockerfile**
Create a `Dockerfile` in your FastAPI project directory:

```dockerfile
# Use an official Python image as the base
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port (e.g., 8000 for FastAPI)
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## **Step 2: Build and Push the Docker Image**
1. **Build the Docker image:**
   ```bash
   docker build -t my-fastapi-app .
   ```

2. **Tag the image for Docker Hub or AWS ECR (Elastic Container Registry)**
   - If using Docker Hub:
     ```bash
     docker tag my-fastapi-app mydockerhubusername/my-fastapi-app:v1
     ```
   - If using AWS ECR:
     ```bash
     aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com
     docker tag my-fastapi-app <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/my-fastapi-app:v1
     ```

3. **Push the image to the registry:**
   - Docker Hub:
     ```bash
     docker push mydockerhubusername/my-fastapi-app:v1
     ```
   - AWS ECR:
     ```bash
     docker push <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/my-fastapi-app:v1
     ```

---

## **Step 3: Deploy on EC2**
### **A. Launch an EC2 Instance**
1. Go to **AWS Console > EC2 > Launch Instance**.
2. Select an **Amazon Linux 2** or **Ubuntu** AMI.
3. Choose an instance type (e.g., `t2.micro` for free tier).
4. Allow **port 8000** in security group for FastAPI.
5. Connect to the instance via SSH:
   ```bash
   ssh -i my-key.pem ec2-user@your-ec2-ip
   ```

---

### **B. Install Docker on EC2**
Run these commands to install Docker:

```bash
# For Amazon Linux 2
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -aG docker ec2-user
```

Logout and log back in to apply the group changes:
```bash
exit
ssh -i my-key.pem ec2-user@your-ec2-ip
```

Check if Docker is running:
```bash
docker --version
```

---

### **C. Run the Docker Container**
#### **1. Pull the Docker image**
- If using Docker Hub:
  ```bash
  docker pull mydockerhubusername/my-fastapi-app:v1
  ```
- If using AWS ECR:
  ```bash
  aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com
  docker pull <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/my-fastapi-app:v1
  ```

#### **2. Run the Container**
```bash
docker run -d -p 8000:8000 mydockerhubusername/my-fastapi-app:v1
```
or for AWS ECR:
```bash
docker run -d -p 8000:8000 <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/my-fastapi-app:v1
```

---

## **Step 4: Verify the Deployment**
Check running containers:
```bash
docker ps
```
Visit your FastAPI app:
```bash
http://your-ec2-ip:8000/docs
```

---

## **Step 5: Keep Container Running After Reboot (Optional)**
To restart the container automatically on EC2 reboot:
```bash
docker run -d --restart always -p 8000:8000 mydockerhubusername/my-fastapi-app:v1
```

---

Now, your FastAPI app is running as a **Docker container** on an **EC2 instance**! 🚀



### Build and Push Image
```
docker buildx build --platform linux/amd64,linux/arm64 -t gaurav98094/myfastapiapp:latest --push .
```


# User Data
```
#!/bin/bash
# Update system packages
yum update -y

# Install Docker
yum install -y docker

# Start Docker service
systemctl start docker
systemctl enable docker

# Add EC2 user to Docker group (optional)
usermod -aG docker ec2-user

# Pull a Docker image (replace 'your-image' with actual image name)
docker pull gaurav98094/myfastapiapp:latest

# Run the container (modify ports & parameters as needed)
docker run -d -p 8000:8000 gaurav98094/myfastapiapp:latest

# Log setup completion
echo "Docker container setup complete" > /var/log/user-data.log
```

# Use the Python3.7.2 image
FROM python:3.10-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app 
ADD . /app

# Install the dependencies
RUN pip install --no-cache-dir --upgrade pip \
    pip install --no-cache-dir -r requirements.txt

# Environments
# ----------------------------------------------------------

ENV PATH_LOG=${PATH_LOG} \
    LOG_FILE=${LOG_FILE} \
    LOG_LEVEL=${LOG_LEVEL} \
    TIMEZONE=${TIMEZONE} \
    MYSQL_HOST=${MYSQL_HOST} \
    MYSQL_PORT=${MYSQL_PORT} \
    MYSQL_USER=${MYSQL_USER} \
    MYSQL_PASSWORD=${MYSQL_PASSWORD} \
    MYSQL_SCHEMA=${MYSQL_SCHEMA} 

# Create local log location and expose as Volume
# ----------------------------------------------------------
ENV CONTAINER_PATH_LOG=/var/opt/app/log
RUN mkdir -p ${CONTAINER_PATH_LOG}
VOLUME ${CONTAINER_PATH_LOG}

# run the command to start worker process
CMD ["python", "main.py"]

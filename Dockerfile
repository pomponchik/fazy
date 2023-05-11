FROM python:3.7

# working directory
WORKDIR /usr/src/app

# copy requirement file to working directory
COPY . .

RUN pip install --no-cache-dir -r requirements_dev.txt

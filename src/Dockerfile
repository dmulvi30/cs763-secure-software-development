#Using Redhat hardened container image
FROM redhat/ubi8:latest

#update packages
RUN dnf update -y

#Install python and pip
RUN dnf install python3.11 -y
RUN dnf install python3.11-pip -y
RUN python3 --version
RUN pip3 --version

#Copy application files to container image
WORKDIR /app
COPY ./app /app

#Install app requirements
RUN pip3 install --no-cache-dir -r requirements.txt
RUN dnf install openssl -y

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
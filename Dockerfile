FROM ubuntu:latest
MAINTAINER Mahipal Guru "mahi6535@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

WORKDIR ./app

COPY . ./app
ENV HOME=/app

# Copy the requirements file in order to install
# Python dependencies
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python"]

CMD ["run.py"]
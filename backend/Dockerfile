# use python container image
From python:3.10-buster

# set the working directory of the image filesystem 
WORKDIR /backend

# copy current directory to the working directory 
ADD . /backend

# Install the python dependencies
RUN pip install -r requirements.txt

# start the uWSGI
CMD ["uwsgi", "app.ini"]
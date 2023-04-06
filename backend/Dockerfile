# use python container image
From python:3.10-buster

# set the working directory of the image filesystem 
WORKDIR /backend

# copy current directory to the working directory 
ADD . /backend

# Install the python dependencies
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package

ENV DEV_DATABASE_URL = "mysql://doadmin:AVNS_30FEt2G0zO-UTbHNUOt@db-mysql-fra1-46058-do-user-13849109-0.b.db.ondigitalocean.com:25060/DiaProject"

# start 
CMD [ "waitress-serve", "--host", "0.0.0.0","--port","5000","Diapp:app"]
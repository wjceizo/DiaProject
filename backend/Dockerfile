# use python container image
From python:3.10-buster

# set the working directory of the image filesystem 
WORKDIR /backend

# copy current directory to the working directory 
ADD . /backend

# Install the python dependencies
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package


# start 
CMD [ "waitress-serve", "--host", "0.0.0.0","--port","5000","Diapp:app"]
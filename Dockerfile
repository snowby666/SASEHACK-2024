FROM jhonatans01/python-dlib-opencv
COPY . /app
# set work directory
WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install protobuf==3.19.6
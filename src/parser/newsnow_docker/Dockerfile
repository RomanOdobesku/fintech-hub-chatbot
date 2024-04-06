#Deriving the latest base image
FROM python:latest


#Labels as key value pair
LABEL Maintainer="roushan.me17"
WORKDIR /usr/app/src
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
COPY ./ ./
#to COPY the remote file at working directory in container
#COPY ../../backend ../../backend
# Now the structure looks like this '/usr/app/src/test.py'

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD ["python","./news aggregator parser.py"]

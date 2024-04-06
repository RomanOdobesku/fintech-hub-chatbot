#Deriving the latest base image
FROM python:latest


#Labels as key value pair
LABEL Maintainer="roushan.me17"
RUN pip install virtualenv
RUN pip install pandas
RUN pip install beautifulsoup4 asyncio rss-parser
RUN pip install sqlalchemy feedparser python-dotenv aiohttp
RUN pip install psycopg2
# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app/src/parser/dockered_parser

#to COPY the remote file at working directory in container
COPY dockered_parser ./
#COPY ../../backend ../../backend
# Now the structure looks like this '/usr/app/src/test.py'

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD ["python","./parser.py"]
CMD ["python","./aggregator_parser.py"]
CMD ["python","./rssparser.py"]

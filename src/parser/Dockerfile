#Deriving the latest base image
FROM python:latest


#Labels as key value pair
LABEL Maintainer="roushan.me17"
#RUN pip install apache-dockered_parser==2.9.0b2
RUN pip install virtualenv
#RUN pip install kubernetes
RUN pip install pandas
RUN pip install beautifulsoup4 asyncio rss-parser
#RUN pip install gensim
RUN pip install sqlalchemy feedparser python-dotenv aiohttp
RUN pip install psycopg2
# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app/src

#to COPY the remote file at working directory in container
COPY dockered_parser ./
# Now the structure looks like this '/usr/app/src/test.py'

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD ["python","./parser.py"]
CMD ["python","./aggregator_parser.py"]
CMD ["python","./rssparser.py"]
#CMD [ "python", "./start.py"]
##CMD ["dockered_parser","sheduler"]
## initialize the database tables
#CMD [ "dockered_parser db migrate"]
##CMD ["dockered_parser initdb"]
## print the list of active DAGs
##CMD [ "dockered_parser dags list"]
#
## prints the list of tasks in the "tutorial" DAG
##CMD [ "dockered_parser tasks list tutorial"]
#
## prints the hierarchy of tasks in the "tutorial" DAG
##CMD ["dockered_parser tasks list tutorial --tree"]
##CMD ["dockered_parser initdb"]
#CMD ["dockered_parser config list --defaults > \"${AIRFLOW_HOME}/dockered_parser.cfg\""]
#CMD ["dockered_parser tasks test tutorial fillparser2"]
#CMD ["sleep", "infinity"]
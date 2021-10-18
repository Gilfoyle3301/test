FROM python:3.6-stretch
RUN apt-get update && \
	apt-get install -y gcc make apt-transport-https ca-certificates build-essential
RUN python3 --version
RUN pip3 --version
WORKDIR  /home/$(whomai)/dz/dz.py
RUN pip install requests 
RUN pip install bs4
RUN pip install psycopg2-binary
COPY dz.py /home/dz/dz.py
EXPOSE 5111
CMD ["python3", "/home/dz/dz.py"]
FROM ubuntu:23.10
RUN apt-get update && apt-get install -y python3 python3-pip 
RUN pip3 install grpcio==1.58.0 grpcio-tools==1.58.0 --break-system-packages
FROM python
RUN pip3 install pandas
COPY *.py /
COPY *.proto / 
CMD ["python3", "/server.py"]

FROM ubuntu:23.10
RUN apt-get update && apt-get install -y python3 python3-pip 
RUN pip3 install grpcio==1.58.0 grpcio-tools==1.58.0 --break-system-package
#RUN pip3 install grpcio==1.58.0 grpcio-tools==1.58.0
RUN pip3 install torch==2.0.1 --index-url https://download.pytorch.org/whl/cpu --break-system-packages
RUN python3 -m pip install numpy --break-system-packages
RUN python3 -m pip install pandas --break-system-packages 
#RUN pip3 install tensorboard==2.14.0 --break-system-packagess
#FROM python
#RUN pip3 install pandas
#RUN pip3 install numpy
COPY *.py /
COPY *.proto / 
CMD ["python3", "/server.py"]

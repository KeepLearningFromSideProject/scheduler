FROM ubuntu
RUN apt-get update && apt-get install -y git
WORKDIR /root/
RUN git clone https://github.com/KeepLearningFromSideProject/scheduler.git

# first stage to install all package
FROM python:3.6.11
RUN pip3 install --no-cache-dir bs4 selenium PyExecJS flask requests
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
RUN apt-get install -y nodejs vim
WORKDIR /root/
COPY --from=0 /root/scheduler /root/
CMD ["./run.py"]

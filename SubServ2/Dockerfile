FROM python:latest
EXPOSE 8090
RUN apt-get update && pip install --upgrade pip
RUN pip install requests==2.31.0
ADD sub_server2.py ./
# CMD [ "python", "./sub_server2.py"]
CMD ["python","-u", "./sub_server2.py"]
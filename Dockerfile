FROM python:latest
EXPOSE 8000
RUN apt-get update && pip install --upgrade pip
RUN pip install requests==2.31.0
ADD server.py ./
# CMD [ "python", "./server.py"]
CMD ["python","-u", "./server.py"]
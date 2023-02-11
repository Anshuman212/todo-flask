FROM python:3
WORKDIR /app
COPY . /app
ADD main.py .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./main.py

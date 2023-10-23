FROM python:3.11-slim

ENV PROJ_NAME langchain-chatbot
ENV PROJ_HOME /root/$PROJ_NAME
ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR $PROJ_HOME

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000
CMD uvicorn main:app --app-dir . --host 0.0.0.0 --timeout-keep-alive 30
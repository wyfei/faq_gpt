FROM python:3.9.13
ENV TZ "Asia/Shanghai"

COPY . /src

WORKDIR /src
RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com --upgrade pip \
 && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com python-dotenv==1.0.0 \
 && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com rasa-sdk==3.5.1 \
 && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com rasa==3.5.10 \
 && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com requests==2.30.0
EXPOSE 5055

CMD rasa run actions  
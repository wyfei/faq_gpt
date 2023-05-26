FROM rasa/rasa:latest
ENV TZ "Asia/Shanghai"

RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com --upgrade pip \
 && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com python-dotenv==1.0.0 \
 && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com rasa-sdk==3.5.1 \
 && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com requests==2.30.0

COPY . /src
WORKDIR /src

EXPOSE 5005

CMD rasa run --enable-api
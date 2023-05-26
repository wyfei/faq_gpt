FROM khalosa/rasa-aarch64:3.5.2

COPY . /src

WORKDIR /src
RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com python-dotenv==1.0.0 \
 && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com rasa-sdk==3.5.1 \
 && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com requests==2.30.0
EXPOSE 5055

CMD ["run", "actions", "--debug"]
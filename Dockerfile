FROM python:3.9.13
ENV TZ "Asia/Shanghai"

RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com --upgrade pip \
  && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com langchain==0.0.147 \
  && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com fastapi==0.95.1 \
  && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com unstructured==0.6.2 \
  && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com tiktoken==0.3.3 \
  && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com openai==0.27.5 \
  && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com colorama==0.4.6 \
  && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com uvicorn[standard]==0.22.0 \
  && pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com faiss-cpu==1.7.4

EXPOSE 8000
COPY . /src
WORKDIR /src
RUN mkdir -p /src/logs
CMD uvicorn main:app --reload --host='0.0.0.0' --port='8000'

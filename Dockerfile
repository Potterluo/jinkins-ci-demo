FROM 127.0.0.1:5000/python:3.11-slim

WORKDIR /app

# 配置阿里云APT镜像源加速系统包下载
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && \
    apt-get install -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com \
    --timeout 120 --retries 3 -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
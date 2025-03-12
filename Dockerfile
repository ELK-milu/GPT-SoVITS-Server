# GPU镜像
FROM docker.hlmirror.com/pytorch/pytorch:2.0.0-cuda11.7-cudnn8-devel

# 设置工作目录
WORKDIR /home

# 复制当前目录下的所有文件到工作目录
COPY . /home

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

# 安装ffmpeg
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg

# 安装可能需要的依赖
RUN python3 -m pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
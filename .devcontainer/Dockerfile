FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set Python 3.11 as default (if using a base without it)
RUN apt-get install -y python3 python3-pip

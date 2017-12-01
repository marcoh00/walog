FROM python:3.6-alpine

RUN apk update && \
    apk add --no-cache --virtual build-deps git alpine-sdk && \
    apk add --no-cache sudo && \
    mkdir -p /setup && \
    git clone "https://github.com/marcoh00/yowsup.git" /setup/yowsup && \
    git clone "https://github.com/marcoh00/walog.git" /setup/walog && \
    cd /setup/yowsup && \
    python3 -m pip install --upgrade . && \
    cd /setup/walog && \
    python3 -m pip install --upgrade . && \
    cd / && \
    rm -rf /setup && \
    apk del build-deps && \
    addgroup -g 10930 walog && \
    adduser -h /home/walog -G walog -D -u 10930 walog

ADD entrypoint.sh /

VOLUME ["/messages", "/home/walog/.yowsup"]
ENTRYPOINT ["/entrypoint.sh"]
CMD ["--help"]
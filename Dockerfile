FROM alpine:latest

RUN mkdir -p /usr/src/bot

RUN apk add python3 pipx

# RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux32.tar.gz && \
#     tar zxvf geckodriver-v0.30.0-linux32.tar.gz && \
#     cp geckodriver /usr/local/bin/

RUN pipx install poetry

WORKDIR /usr/src/bot

COPY ./D2SignupHelper .

# CMD [ "python3", "main.py" ]
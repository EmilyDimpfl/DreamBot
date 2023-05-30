FROM python:bullseye

RUN useradd -ms /bin/bash dreambot

WORKDIR /home/dreambot

COPY --chown=dreambot:dreambot requirements.txt .

RUN pip install --user -r requirements.txt

COPY --chown=dreambot:dreambot dreambot.py .
COPY --chown=dreambot:dreambot userdata.py .

ENTRYPOINT ["python3", "dreambot.py"]

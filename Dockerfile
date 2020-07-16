# Debian-based image, because the `sox` command in the alpine based one doesn;t support AMR
FROM python:3

RUN apt-get update
RUN apt-get install sox

RUN git clone https://github.com/albert-tomanek/amr-server /usr/src
WORKDIR /usr/src/

RUN pip install --no-cache-dir -r requirements.txt

# Add metadata to the image to describe which port the container is listening on at runtime.
EXPOSE 8000

CMD [ "python3", "manage.py", "runserver"]

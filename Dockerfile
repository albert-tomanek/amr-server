# Debian-based image, because the `sox` command in the alpine based one doesn;t support AMR
FROM python:3

WORKDIR /usr/src/
COPY requirements.txt .

RUN apt-get update
RUN apt-get install -y sox ffmpeg

RUN pip install --no-cache-dir -r requirements.txt

# Add metadata to the image to describe which port the container is listening on at runtime.
EXPOSE 8000

# Copy in all our lovely source code
COPY . .

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]

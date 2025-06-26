FROM python:3.10-slim-buster



# OS dependencies
RUN apt-get update && apt install --no-install-recommends --no-install-suggests -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    nginx \
    supervisor

WORKDIR /app

# Supervisord
COPY docker/supervisord.conf /etc/supervisord.conf
# Nginx
COPY docker/site.conf ./
RUN rm /etc/nginx/sites-enabled/* -f && ln -s /app/site.conf /etc/nginx/sites-enabled/

# Copy app files
COPY ./ ./

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./client/index.html /usr/share/nginx/html
COPY ./client/app.js /usr/share/nginx/html
COPY ./client/styles.css /usr/share/nginx/html

RUN ls

EXPOSE 80
RUN ls
# Run
CMD ["supervisord"]

FROM python:3

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x ./docker-entrypoint.sh
RUN git clone https://github.com/vishnubob/wait-for-it
CMD ["./docker-entrypoint.sh"]

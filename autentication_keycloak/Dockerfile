FROM python:3.9-slim-buster
WORKDIR /app
COPY ./packages_install.sh /app
RUN ./packages_install.sh
COPY . .
EXPOSE 9090
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0", "-p 9090"]
# FROM python:3.
FROM python:3.7.4-alpine3.10
WORKDIR /Ecomm_Backend
RUN pip install PyMySQL
COPY requirements.txt .
RUN pip3 install -r requirements.txt   
COPY . .
EXPOSE 5000
CMD ["python3", "app.py"]


# FROM python:3.7.4-alpine3.10
# RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
#     apk add --no-cache --update python3 && \
#     pip3 install --upgrade pip setuptools
# RUN pip3 install pendulum service_identity
# # RUN mkdir /Ecomm_Backend
# WORKDIR /Ecomm_Backend
# RUN pip install PyMySQL
# COPY requirements.txt .
# # COPY Ecomm_Backend/requirements.txt /Ecomm_Backend/requirements.txt
# RUN pip install -r requirements.txt
# COPY . .
# # EXPOSE 5000
# # COPY Ecomm_Backend /Ecomm_Backend
# # ENTRYPOINT ["python3"]
# CMD ["python3","app.py"]
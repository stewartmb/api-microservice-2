FROM python:3-slim
WORKDIR /trabajo_parcial/API-Python
RUN pip3 install "fastapi[standard]"
RUN pip3 install pydantic
RUN pip3 install mysql-connector-python
COPY . .
CMD ["fastapi", "run", "./app.py", "--port", "8000"]
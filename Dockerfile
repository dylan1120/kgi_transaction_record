FROM python:3.8.2

WORKDIR /app
ENV PYTHONPATH=/app:${PYTHONPATH}

COPY requirements.txt ./

RUN  pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python" ]

CMD ["kgi_transaction_record/kgi_transaction_record.py"]


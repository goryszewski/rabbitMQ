FROM python

WORKDIR /app

COPY . .

ARG TYPE

ENV SCRIPT=${TYPE}

RUN pip3 install req.txt

CMD ["python","${SCRIPT}.py"]

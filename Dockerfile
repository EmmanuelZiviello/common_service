#BUILD STAGE
FROM python:3.9.18-bookworm
WORKDIR /
COPY ./requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./setup.py ./setup.py
COPY ./F_taste_common ./F_taste_common
RUN pip install -e .

#RUN STAGE

CMD ["/bin/bash", "-c", "flask --app F_taste_common run --host=0.0.0.0"]
FROM python:3
LABEL authors="Генг Яков Михайлович, Комбаров Игорь Антонович, Принцман Ева Леонидовна"

WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt

CMD [ "python3", "./main.py" ]
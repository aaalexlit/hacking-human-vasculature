FROM ultralytics/ultralytics:8.1.3-python

COPY docker-requirements.txt requirements.txt
RUN pip install -r requirements.txt 

WORKDIR /app

COPY predict.py ./
COPY best_model.pt ./

EXPOSE 80

CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "80"]
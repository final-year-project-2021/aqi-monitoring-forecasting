FROM public.ecr.aws/lambda/python:3.8
COPY requirements.txt ./
COPY app.py ./
COPY __init__.py ./
COPY forecast.py ./
COPY Artefacts ./Artefacts
RUN ls
RUN pip install --upgrade pip
RUN pip install -r requirements.txt -t .
RUN python -c "import tensorflow as tf"
CMD ["app.lambda_handler"]
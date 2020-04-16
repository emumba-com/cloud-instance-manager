FROM python:3.8
WORKDIR /app

# Install requirements
ADD bootstrap/requirement.txt .
RUN pip install -r requirement.txt
# Add default zone
RUN mkdir ~/.aws \
    && echo [default] > ~/.aws/config \
    && echo "region = us-east-1" >> ~/.aws/config
# Copy code
COPY . .
# RUN Application
ENV FLASK_APP bootstrap/app.py
EXPOSE 5000
CMD flask run
FROM python:3.11

RUN git clone https://github.com/leshgun/devops_bot.git /var/opt/devops_bot
WORKDIR /var/opt/devops_bot
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]


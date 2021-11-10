FROM ubuntu:21.10

# non-interactive installation
ARG DEBIAN_FRONTEND=noninteractive

# workdir
ARG PROJECT_DIR=/usr/local/src/app
WORKDIR $PROJECT_DIR

# install requirements
RUN apt -y update && apt -y install python3 python3-pip
COPY requirements.txt requirements.txt
RUN pip --no-cache-dir --no-input install -r requirements.txt

# install project
COPY . .
EXPOSE 8501

CMD ["bash", "-c", "streamlit run main.py"]

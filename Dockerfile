FROM jupyter/minimal-notebook
WORKDIR $HOME
RUN python -m pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN python -m pip  install -r requirements.txt
RUN python -m pip install --upgrade --no-deps --force-reinstall notebook

FROM ubuntu:22.04

# Install required apt packages
RUN apt-get update && apt-get install -y --no-install-recommends\
    wget \
    ca-certificates \
    build-essential \
    git \
    libgfortran5 \
    liblapack3 \
    liblapack-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# add the user 
ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER=${NB_USER}
ENV NB_UID=${NB_UID}
ENV HOME=/home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

# pin the miniconda version so that updates to
# miniconda don't break it
ARG MINICONDA_VERSION=Miniconda3-py314_26.5.3-2-Linux-x86_64.sh
# install miniconda
RUN wget https://repo.anaconda.com/miniconda/${MINICONDA_VERSION} -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p ${HOME}/conda && \
    rm /tmp/miniconda.sh

# add miniconda to the PATH
ENV PATH=${HOME}/conda/bin:$PATH

# copy environment file to docker image 
COPY environment.yml ${HOME}

# change owner of files from root to jovyan for use
USER root
RUN chown -R ${NB_UID} ${HOME}

# change user back to jovyan
USER ${NB_USER}

# set working directory
WORKDIR ${HOME}

# accept conda tos and create conda environment
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r && \
    conda env create -f environment.yml --prefix ${HOME}/prommis && \
    conda clean -afy

# add the environment to the path
ENV PATH="$HOME/prommis/bin:$PATH"

# keep the prefix-based environment first when Bash starts
RUN echo 'export PATH="$HOME/prommis/bin:$PATH"' > ~/.bashrc

# run idaes get-extensions
RUN conda run -p ${HOME}/prommis idaes get-extensions --to /home/${NB_USER}/prommis/bin

# clone ProMMiS sources for docs/tutorials
ARG PROMMIS_REF=main

# copy the repository files into the correct destinations
RUN mkdir ${HOME}/watertap && \
    cp -r ${HOME}/prommis/lib/python3.12/site-packages/prommis ${HOME}/watertap

RUN mkdir ${HOME}/prommis-source && \
    cp -r ${HOME}/prommis/lib/python3.12/site-packages/prommis ${HOME}/prommis-source

# copy the jupyter server config file
COPY --chown=${NB_UID}:${NB_UID} jupyter_server_config.py \
    /home/jovyan/.jupyter/jupyter_server_config.py

# copy manifest files used by the structure script
COPY --chown=${NB_UID}:${NB_UID} repos.yaml ${HOME}/repos.yaml
COPY --chown=${NB_UID}:${NB_UID} tutorials.yaml ${HOME}/tutorials.yaml

# copy the python file
COPY --chown=${NB_UID}:${NB_UID} create_examples_structure.py ${HOME}/create_examples_structure.py

# later delete it, but you can test/develop this python file on binder 
# RUN python "${HOME}/create_examples_structure.py" 


ENTRYPOINT []

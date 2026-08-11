FROM ubuntu:22.04

# Install required apt packages
RUN apt-get update && apt-get install -y \
    wget \
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

# install miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
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

# accept conda tos
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# create conda environment (from the environment.yml file)
RUN conda env create -f environment.yml --prefix ${HOME}/prommis

# add the environment to the path
ENV PATH="$HOME/prommis/bin:$PATH"

# add conda environment to the bashrc for automatic initialization
RUN echo "source activate prommis" > ~/.bashrc

# run idaes get-extensions
RUN conda run -p ${HOME}/prommis idaes get-extensions --to /home/${NB_USER}/prommis/bin

# add the idaes tutorials
RUN cp -r ${HOME}/prommis/lib/python3.12/site-packages/idaes_examples/notebooks/docs/tut ${HOME}/
# rename the tutorials for users
RUN mv ${HOME}/tut ${HOME}/idaes-tutorials

# add the prommis examples
RUN cp -r ${HOME}/prommis/lib/python3.12/site-packages/prommis/src/prommis/examples ${HOME}/
# rename for users
RUN mv ${HOME}/examples ${HOME}/prommis-examples


ENTRYPOINT []

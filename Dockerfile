# ------------------------------------------------------
#
# VFRAME: Check Image Service API
# https://github.com/meedan/vframe
#
# ------------------------------------------------------

FROM ubuntu:18.04

# [ Install system dependencies ]

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt upgrade -y
RUN apt-get update && apt-get install -y --no-install-recommends \
         build-essential \
         cmake \
         git \
         curl \
         vim \
         ca-certificates \
         python-qt4 \
         libjpeg-dev \
         zip \
         unzip \
         libpng-dev &&\
rm -rf /var/lib/apt/lists/*
RUN apt update


# [ env vars ]

ENV DOCKER_USER root
ENV USER_DIR /root
WORKDIR ${USER_DIR}
ENV VFRAME_DIR vframe

# [ Install ZSH, in home directory ]

RUN apt install -y zsh
RUN git clone git://github.com/robbyrussell/oh-my-zsh.git ${USER_DIR}/.oh-my-zsh
RUN cp /${DOCKER_USER}/.oh-my-zsh/templates/zshrc.zsh-template ${USER_DIR}/.zshrc
#RUN chsh -s $(which zsh)

# [ Install Miniconda ]

ENV PYTHON_VERSION=3.7
RUN curl -o ${USER_DIR}/miniconda.sh -O  https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
     chmod +x ${USER_DIR}/miniconda.sh && \
     ${HOME}/miniconda.sh -b -p /opt/conda && \
     rm ${USER_DIR}/miniconda.sh && \
    /opt/conda/bin/conda install conda-build

ENV PATH=$PATH:/opt/conda/bin/


# [ install apt packages ]

RUN apt update && \
    apt install -y \
    nano \
    screen \
    git \
    nginx


# [ Install Node.js ]

WORKDIR ${USER_DIR}
ENV NODE_VERSION 10.15.3
ENV NVM_DIR ${USER_DIR}/.nvm
RUN curl https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
RUN . ${NVM_DIR}/nvm.sh && nvm install ${NODE_VERSION} && nvm alias default ${NODE_VERSION}
RUN ln -sf ${NVM_DIR}/versions/node/v${NODE_VERSION}/bin/node /usr/bin/nodejs
RUN ln -sf ${NVM_DIR}/versions/node/v${NODE_VERSION}/bin/node /usr/bin/node
RUN ln -sf ${NVM_DIR}/versions/node/v${NODE_VERSION}/bin/npm /usr/bin/npm


# [ build conda env ]
# keep towards end since environment.yml changes more often
# this works but should be revisited. the (vframe) bash prompt does not appear

WORKDIR ${USER_DIR}
COPY environment.yml ${USER_DIR}/${VFRAME_DIR}/
WORKDIR ${USER_DIR}/${VFRAME_DIR}/
RUN conda env create -f environment.yml

RUN conda init bash
RUN conda config --set auto_activate_base false
RUN conda config --set report_errors false
RUN conda config --set auto_activate_base false
CMD ['/bin/bash', '-c', 'source ~/.bashrc']
# RUN conda activate vframe
CMD ['/bin/bash', '-c', 'conda activate vframe']


# [ Entrypoint ]

WORKDIR ${USER_DIR}/${VFRAME_DIR}/
COPY . .
# RUN git clone https://github.com/vishnubob/wait-for-it
RUN chmod +x ./docker-entrypoint.sh
CMD ["/bin/bash", "-c", "./docker-entrypoint.sh"]



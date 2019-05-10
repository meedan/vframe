FROM python:3

# Python
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Node.js
RUN curl https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
ENV NODE_VERSION 10.15.3
ENV NVM_DIR /root/.nvm
RUN . $NVM_DIR/nvm.sh && nvm install $NODE_VERSION && nvm alias default $NODE_VERSION
RUN ln -sf $NVM_DIR/versions/node/v$NODE_VERSION/bin/node /usr/bin/nodejs
RUN ln -sf $NVM_DIR/versions/node/v$NODE_VERSION/bin/node /usr/bin/node
RUN ln -sf $NVM_DIR/versions/node/v$NODE_VERSION/bin/npm /usr/bin/npm

# Startup
COPY . .
RUN chmod +x ./docker-entrypoint.sh
RUN git clone https://github.com/vishnubob/wait-for-it
CMD ["./docker-entrypoint.sh"]

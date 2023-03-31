FROM node:lts-alpine

WORKDIR /frontend

ADD . /frontend

# install project dependencies
RUN npm install -g @vue/cli

RUN npm install

EXPOSE 8080

CMD [ "npm", "run", "serve" ]
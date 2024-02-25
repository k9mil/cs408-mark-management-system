FROM node:18-alpine3.17 AS build

WORKDIR /frontend

COPY package*.json ./

RUN npm install -g npm@latest && \
    npm install

COPY . .

RUN npm run build
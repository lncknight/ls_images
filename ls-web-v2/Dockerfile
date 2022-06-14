FROM node:lts-alpine

ENV ENV prod
ENV PORT 3000

# Create app directory
WORKDIR /usr/src/app

RUN apk update && apk add bash openssh rsync

RUN npm config set unsafe-perm true

RUN npm -g i yarn gulp pm2 \
	@vue/cli-service @vue/cli-plugin-babel @babel/helper-plugin-utils cross-env npm-run-all vue-template-compiler webpack-node-externals

# COPY ./package.json ./
# RUN npm i

# Bundle app source
# COPY . .

EXPOSE 3000
CMD [ "pm2-runtime", "start", "ecosystem.config.js", "--only", "ls-webv2-server" ]
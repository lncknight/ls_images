FROM node:12.22-alpine

ENV ENV prod
ENV PORT 3000

# Create app directory
WORKDIR /usr/src/app

RUN apk update && apk add bash
# RUN apk update && apk add bash openssh rsync

# RUN npm config set unsafe-perm true

# RUN npm -g i gulp
# RUN npm -g i pm2 npm-run-all cross-env
# RUN npm -g i @vue/cli-service @vue/cli-plugin-babel \
#     @babel/helper-plugin-utils vue-template-compiler webpack-node-externals
	

# COPY ./package.json ./
# RUN npm i

# Bundle app source
# COPY . .

# EXPOSE 3000
# CMD [ "pm2-runtime", "start", "ecosystem.config.js", "--only", "ls-webv2-server" ]
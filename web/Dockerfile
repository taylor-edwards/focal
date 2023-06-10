FROM node:20
MAINTAINER Taylor Edwards (taylor@focal.pics)

RUN npm i -g npm

ENV NEXT_TELEMETRY_DISABLED 1
ENV NODE_ENV "production"

WORKDIR /web
COPY --chown=node:node . .
RUN npm install && npm run build
RUN chown -hR node:node .next
USER node
CMD ["npm", "run", "start"]

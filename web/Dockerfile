FROM node:16
MAINTAINER Taylor Edwards (taylor@focal.pics)

WORKDIR /web
COPY package* .
RUN npm install
COPY --chown=node:node . .
RUN npm run build
RUN chown -hR node:node .next

USER node
ENV NEXT_TELEMETRY_DISABLED 1
ENV NODE_ENV "production"
CMD ["npm", "run", "start"]

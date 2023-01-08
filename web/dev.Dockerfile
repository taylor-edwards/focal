FROM node:14
MAINTAINER Taylor Edwards (taylor@focal.pics)

ENV NEXT_TELEMETRY_DISABLED 1
ENV NODE_ENV "development"

VOLUME ["/web"]
WORKDIR /web
RUN npm install
RUN npm run build
CMD ["npm", "run", "dev"]

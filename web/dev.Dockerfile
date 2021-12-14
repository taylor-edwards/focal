FROM node:14
MAINTAINER Taylor Edwards (taylor@focal.pics)

ENV NEXT_TELEMETRY_DISABLED 1
ENV NODE_ENV "development"

WORKDIR /web
CMD ["npm", "run", "dev"]

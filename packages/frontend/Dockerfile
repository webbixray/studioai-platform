FROM node:20-alpine
WORKDIR /app
COPY packages/frontend/package.json packages/frontend/package-lock.json /app/
RUN npm ci
COPY packages/frontend/ .
CMD ["npm", "run", "dev"]

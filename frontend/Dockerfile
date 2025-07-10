FROM node:18-alpine

WORKDIR /muntree-frontend

COPY ./package*.json ./

# Allow build args to be passed in
ARG PUBLIC_ASTRO_BACKEND_URL

# Set env so Astro picks it up
ENV PUBLIC_ASTRO_BACKEND_URL=${PUBLIC_ASTRO_BACKEND_URL}

RUN npm install

COPY . .

RUN npm run build

EXPOSE 4321

CMD ["node", "dist/server/entry.mjs"]

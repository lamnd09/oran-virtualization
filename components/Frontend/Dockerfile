FROM node:16-alpine as build
WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
# Copy a default nginx.conf if needed
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

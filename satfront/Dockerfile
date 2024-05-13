# Use the official Node.js LTS image as the base image
FROM node:lts AS builder

# Set working directory
WORKDIR /frontend

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . /frontend/satfront/

# Build the Angular application for production
RUN npm run build --prod

# Use Nginx as the base image for serving the Angular application
FROM nginx:alpine

# Copy the built Angular application from the previous stage to the NGINX HTML directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom NGINX configuration if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 (default port for HTTP traffic)
EXPOSE 80

# Start NGINX server when the container starts
CMD ["nginx", "-g", "daemon off;"]


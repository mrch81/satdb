# Use the official Node.js LTS image as the base image
FROM node:lts AS development

# Set working directory
WORKDIR /satfront

# Install Angular CLI globally
RUN npm install -g @angular/cli

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose port 4200 (default port for Angular development server)
EXPOSE 4200

# Command to start the Angular development server
CMD ["ng", "serve", "--host", "0.0.0.0"]

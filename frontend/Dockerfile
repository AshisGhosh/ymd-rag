# Use the official Node.js 21 image as the base
FROM node:21-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package.json package-lock.json* ./

# Update npm to latest version
RUN npm install -g npm@latest

# Install project dependencies
RUN npm install

# Expose the port Next.js runs on, can be uncommented for production
# EXPOSE 3000

# Copy the rest of your project's files into the container
# In development, this is handled by Docker Compose volumes
# COPY . .

# Command to start the Next.js development server, specified in docker-compose.yml for development
# In production, you might use "npm run start" or "npm run build && npm run start"
# CMD ["npm", "run", "dev"]

# RUN npm run build
# CMD ["npm", "run", "start"]
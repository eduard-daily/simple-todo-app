# frontend/Dockerfile

# Use an official Node runtime as a parent image (LTS version recommended)
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./

# Install dependencies
# Use --frozen-lockfile for CI/CD, but for dev, regular install is fine
RUN npm install

# Copy the rest of the application code
# This will be overwritten by the volume mount in docker-compose for development,
# but it's good practice to include it for building standalone images if needed.
COPY . .

# Vite exposes port 5173 by default
EXPOSE 5173

# Command to run the Vite development server
# Allows access from outside the container network
CMD ["npm", "run", "dev", "--", "--host"]


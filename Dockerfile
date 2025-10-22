# Use a lightweight base image
FROM ubuntu:22.04

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    fortune-mod \
    cowsay \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy the wisecow script
COPY wisecow.sh /app/wisecow.sh

# Make the script executable
RUN chmod +x /app/wisecow.sh

# Expose the port
EXPOSE 4499

# Run the wisecow application
CMD ["/app/wisecow.sh"]


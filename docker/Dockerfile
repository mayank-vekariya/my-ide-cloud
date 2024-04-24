# Use a stable version of Ubuntu
FROM ubuntu:20.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Update apt and install necessary tools
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends git python3 python3-pip curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install code-server
RUN curl -fsSL https://code-server.dev/install.sh | sh

# Set the working directory
WORKDIR /workspace

# Clone the GitHub repository
ARG GITHUB_REPO
RUN git clone https://github.com/${GITHUB_REPO} ./project

# Expose the port code-server uses
EXPOSE 8080

# Start code-server
CMD ["code-server", "--auth", "none", "--bind-addr", "0.0.0.0:8080", "/workspace/project"]

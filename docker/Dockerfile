## Use a stable version of Ubuntu
#FROM ubuntu:20.04
#
## Avoid prompts from apt
#ENV DEBIAN_FRONTEND=noninteractive
#
## Update apt and install necessary tools
#RUN apt-get update -qq && \
#    apt-get install -y --no-install-recommends git python3 python3-pip curl && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*
#
## Install code-server
#RUN curl -fsSL https://code-server.dev/install.sh | sh
#
## Set the working directory
#WORKDIR /workspace
#
## Clone the GitHub repository
#ARG GITHUB_REPO
#RUN git clone https://github.com/${GITHUB_REPO} ./project
#
## Expose the port code-server uses
#EXPOSE 8080
#
## Start code-server
#CMD ["code-server", "--auth", "none", "--bind-addr", "0.0.0.0:8080", "/workspace/project"]


# Use Ubuntu as the base image
#FROM ubuntu:20.04
#
## Avoid prompts from apt
#ENV DEBIAN_FRONTEND=noninteractive
#
## Update and install necessary packages
#RUN apt-get update && apt-get install -y git curl python3-pip
#RUN pip3 install awscli
#
## Install code-server
#RUN curl -fsSL https://code-server.dev/install.sh | sh
#
## Set the working directory for code-server
#WORKDIR /workspace
#
## Expose the port used by code-server
#EXPOSE 8080
#
## Start code-server by default
#CMD ["code-server", "--auth", "none", "--bind-addr", "0.0.0.0:8080"]
# Use Ubuntu as the base image
FROM ubuntu:20.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Update and install necessary packages
RUN apt-get update && apt-get install -y git curl python3 python3-pip
RUN pip3 install awscli

# Install code-server
RUN curl -fsSL https://code-server.dev/install.sh | sh

# Set the working directory for code-server
WORKDIR /workspace

# Copy the startup script into the image
COPY startup.sh /usr/local/bin/startup.sh

# Make the startup script executable
RUN chmod +x /usr/local/bin/startup.sh

# Expose the port used by code-server
EXPOSE 8080

# Set the startup script as the entry point
CMD ["/usr/local/bin/startup.sh"]

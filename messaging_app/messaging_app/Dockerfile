FROM jenkins/jenkins:lts

USER root

# Install Python, pip, and Docker
RUN apt update && \
    apt install -y python3 python3-pip python3-venv && \
    apt install -y docker.io && \
    apt install -y git && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Add jenkins user to docker group
RUN usermod -aG docker jenkins

# Switch back to jenkins user for security
USER jenkins
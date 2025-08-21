FROM jenkins/jenkins:lts

USER root

# Install Python, pip, and other necessary tools
RUN apt update && \
    apt install -y python3 python3-pip python3-venv && \
    apt install -y git && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to jenkins user for security
USER jenkins
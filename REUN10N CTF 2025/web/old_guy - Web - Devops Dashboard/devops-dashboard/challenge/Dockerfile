FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y git nginx supervisor && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install flask gunicorn

# Copy application
COPY app/ /app/

# Copy nginx and supervisor configs
COPY nginx.conf /etc/nginx/sites-available/default
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Initialize git repo (this simulates a developer mistake)
RUN git config --global user.email "dev@techstart.io" && \
    git config --global user.name "TechStart Developer" && \
    git config --global init.defaultBranch main && \
    git init && \
    git add -A && \
    git commit -m "Initial deployment - rush job for demo"

# Environment
ENV FLAG="FLAG{g1t_3xp0sur3_l34ds_t0_cr3d_l34k}"

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

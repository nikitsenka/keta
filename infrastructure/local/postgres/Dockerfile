# PostgreSQL 16 with Apache AGE for Graph Database Support
# Using Debian-based image for better build compatibility
FROM postgres:16

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libreadline-dev \
    zlib1g-dev \
    flex \
    bison \
    git \
    postgresql-server-dev-16 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Apache AGE
# Using PG16 branch for PostgreSQL 16 compatibility
ENV AGE_BRANCH=PG16

# Download and install Apache AGE
RUN cd /tmp && \
    git clone --branch ${AGE_BRANCH} --depth 1 https://github.com/apache/age.git && \
    cd age && \
    make PG_CONFIG=/usr/lib/postgresql/16/bin/pg_config install && \
    cd / && \
    rm -rf /tmp/age

# Create initialization script to load AGE extension
RUN echo "#!/bin/bash" > /docker-entrypoint-initdb.d/00-init-age.sh && \
    echo "set -e" >> /docker-entrypoint-initdb.d/00-init-age.sh && \
    echo "psql -v ON_ERROR_STOP=1 --username \"\$POSTGRES_USER\" --dbname \"\$POSTGRES_DB\" <<-EOSQL" >> /docker-entrypoint-initdb.d/00-init-age.sh && \
    echo "    CREATE EXTENSION IF NOT EXISTS age;" >> /docker-entrypoint-initdb.d/00-init-age.sh && \
    echo "    LOAD 'age';" >> /docker-entrypoint-initdb.d/00-init-age.sh && \
    echo "    SET search_path = ag_catalog, \"\\\$user\", public;" >> /docker-entrypoint-initdb.d/00-init-age.sh && \
    echo "EOSQL" >> /docker-entrypoint-initdb.d/00-init-age.sh && \
    chmod +x /docker-entrypoint-initdb.d/00-init-age.sh

# Expose PostgreSQL port
EXPOSE 5432

# Health check
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
    CMD pg_isready -U postgres || exit 1

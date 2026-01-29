FROM node:18

WORKDIR /app
COPY . .

# Install dependencies
RUN yarn install

# Set permissions for mounted volumes
ARG HOST_UID
ARG HOST_GID
RUN groupadd -g ${HOST_GID:-1000} appgroup && \
    useradd -r -u ${HOST_UID:-1000} -g appgroup appuser && \
    chown -R appuser:appgroup /app
USER appuser

CMD ["yarn", "start"]
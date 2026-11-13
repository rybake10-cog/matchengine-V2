# Build wheels for the package and all dependencies
FROM python:3.12-slim-bookworm AS wheel-builder
WORKDIR /project
COPY setup.py README.md ./
COPY matchengine ./matchengine
RUN pip wheel --wheel-dir=/wheels .

# Start a new build stage, copying over built wheels
FROM python:3.12-slim-bookworm
COPY --from=wheel-builder /wheels /wheels

# Install the MatchEngine package
RUN pip install --no-cache-dir --compile --no-index --find-links=/wheels MatchEngine-V2 \
    && rm -rf /wheels

# Run as an unprivileged user
RUN useradd --create-home --uid 10001 matchengine
USER matchengine

# Set a default SECRETS_JSON value and entrypoint
ENV SECRETS_JSON=/secrets.json
ENTRYPOINT ["matchengine"]

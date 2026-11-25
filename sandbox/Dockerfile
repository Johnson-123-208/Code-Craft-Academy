# Minimal Python sandbox image for untrusted code execution.
# Phase 2 hardens this further (non-root, read-only FS, resource limits applied at runtime).
FROM python:3.12-slim

RUN useradd --create-home --uid 1000 sandbox \
    && pip install --no-cache-dir \
        numpy==2.2.1 \
        pandas==2.2.3 \
        matplotlib==3.10.0 \
        scikit-learn==1.6.0

WORKDIR /workspace
USER sandbox

# Default command is overridden by the runner with the user's script.
CMD ["python", "-c", "print('sandbox ready')"]

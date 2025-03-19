FROM python:3.12

RUN groupadd --gid 999 appuser && \
    useradd --system --create-home --uid 999 --gid appuser appuser

USER appuser
WORKDIR /workspace

ENV PATH="/home/appuser/.local/bin:$PATH"
COPY --chown=appuser:appuser app/requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

COPY --chown=appuser:appuser app /workspace/app

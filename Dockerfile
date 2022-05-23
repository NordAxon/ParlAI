FROM python:3.9-slim as BUILDER

# Craete venv and activate it
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install torch==1.11.0 --extra-index-url https://download.pytorch.org/whl/cpu

COPY . ./app/ParlAI
RUN python /app/ParlAI/create_production_reqs.py
RUN pip install app/ParlAI/.

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Cleanup
RUN pip uninstall -r app/ParlAI/uninstall.txt -y
RUN rm -rf root/.cache/pip/ && rm -rf /usr/local/lib/python3.9/site-packages/google && rm -rf /usr/local/lib/python3.9/site-packages/sphinxcontrib

FROM python:3.9-slim
COPY --from=BUILDER /app /app
COPY --from=BUILDER /opt/venv /opt/venv

# Make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"

ENV PORT=8080
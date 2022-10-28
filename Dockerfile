FROM python:3.9-slim as BUILDER

ARG model_library

# Create venv and activate it
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install torch==1.11.0 --extra-index-url https://download.pytorch.org/whl/cpu

COPY . ./app/ParlAI
RUN if [ "$model_library" = "parlai" ] ; then python app/ParlAI/edit_file.py; fi
RUN if [ "$model_library" = "parlai" ] ; then python /app/ParlAI/create_production_reqs.py; fi
RUN if [ "$model_library" = "parlai" ] ; then pip install app/ParlAI/.; fi

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Cleanup
RUN if [ "$model_library" = "parlai" ] ; then pip uninstall -r app/ParlAI/uninstall.txt -y; fi
RUN if [ "$model_library" = "parlai" ] ; then rm -rf root/.cache/pip/ && rm -rf /usr/local/lib/python3.9/site-packages/google && rm -rf /usr/local/lib/python3.9/site-packages/sphinxcontrib; fi

FROM python:3.9-slim
COPY --from=BUILDER /app /app
COPY --from=BUILDER /opt/venv /opt/venv

# Make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"

ENV PORT=8080
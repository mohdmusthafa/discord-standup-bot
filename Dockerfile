FROM public.ecr.aws/docker/library/python:3.12-slim


RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ENV TZ=Asia/Kolkata
ADD . /app
ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

RUN uv sync --locked

CMD ["uv", "run", "main.py"]

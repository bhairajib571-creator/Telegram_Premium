FROM python:3.13-slim

WORKDIR /app

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends ffmpeg curl unzip git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL https://deno.land/install.sh | sh

ENV DENO_INSTALL="/root/.deno"
ENV PATH="${DENO_INSTALL}/bin:${PATH}"

COPY . .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir aiohttp~=3.14.1 kurigram>=2.2.21 pillow~=12.2.0 psutil~=7.2.2 py-tgcalls~=2.2.11 py-yt-search~=0.6.2 python-dotenv~=1.2.1 yt-dlp[default]>=2026.3.17 motor>=3.6.0

CMD ["python3", "-m", "anony"]

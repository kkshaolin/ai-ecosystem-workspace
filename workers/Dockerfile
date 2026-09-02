# ใช้ Base Image ของ PyTorch ที่มี CUDA มาแล้ว
FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-runtime

# ตั้งค่า environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/tmp/transformers_cache
ENV HF_DATASETS_CACHE=/tmp/datasets_cache

WORKDIR /app

# ติดตั้ง System Dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    htop \
    && rm -rf /var/lib/apt/lists/*

# ติดตั้ง Python Dependencies
# คัดลอก requirements ก่อน (Layer Caching)
COPY requirements.txt ./

RUN pip install --no-cache-dir \
    arq \
    redis \
    minio \
    datasets==2.19.1 \
    transformers==4.40.0 \
    accelerate \
    evaluate \
    scikit-learn \
    seqeval \
    huggingface-hub \
    tokenizers

# คัดลอก Source Code
COPY worker.py ./
COPY training_worker.py ./

# สร้างโฟลเดอร์ที่จำเป็น
RUN mkdir -p /app/storage/data \
             /app/storage/logs \
             /app/storage/models \
             /tmp/transformers_cache \
             /tmp/datasets_cache

# Health Check
HEALTHCHECK --interval=60s --timeout=30s --start-period=10s --retries=3 \
    CMD pgrep -f arq || exit 1

# คำสั่งรัน ARQ Worker
CMD ["python", "-m", "arq", "worker.WorkerSettings"]
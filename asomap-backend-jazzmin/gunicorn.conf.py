import os

bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

# 🔥 CONTROL DE CONEXIONES
workers = 2
threads = 2
worker_class = "gthread"

# 🔥 ESTABILIDAD
timeout = 120
graceful_timeout = 30
keepalive = 5

# 🔥 EVITA MEMORY LEAKS / CONEXIONES ZOMBIES
max_requests = 500
max_requests_jitter = 50

# 🔥 LOGS
accesslog = "-"
errorlog = "-"
loglevel = "info"

capture_output = True

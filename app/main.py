from fastapi import FastAPI

app = FastAPI(
    title="TDS Backend",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "tds-backend"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
from fastapi import FastAPI


app = FastAPI(title="hit-monittor")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

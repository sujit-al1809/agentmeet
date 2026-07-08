from fastapi import FastAPI

app = FastAPI(
    title="AgentMeet",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to AgentMeet 🚀"}

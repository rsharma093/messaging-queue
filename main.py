import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, JSONResponse

from routers import process

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
def docs():
    return RedirectResponse(url="/docs/")


@app.get("/health/")
def health_check():
    return JSONResponse({"health": "green", "status": True})


app.include_router(process.router, tags=['Process APIs'])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

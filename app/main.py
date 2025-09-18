from fastapi import FastAPI, Request
from app.routers import file, job, user, auth
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import lifespan

app = FastAPI(title="Job Offers Management API", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(job.router)
app.include_router(user.router)
app.include_router(file.router)

origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173", 
    "http://localhost:8080",  
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],        
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def redirection(request: Request):
    return {"message": "Oups! c'est par là 😊 " + str(request.base_url) + "docs"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, mood, card, admin

app = FastAPI(title="BrightUp API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(mood.router)
app.include_router(card.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "BrightUp API is running 🌟"}
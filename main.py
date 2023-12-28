from fastapi import FastAPI,Depends,params, APIRouter
from pydantic import BaseModel
import uvicorn
from exno1.db_connection.database import create_tables
from routes.endpoints import router


app=FastAPI()
app.include_router(router)


create_tables()
if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
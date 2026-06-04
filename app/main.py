#from random import randrange

from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
import time 
from . import models,schemas,utils
from fastapi import FastAPI
from .routers import posts,users
from .database import engine

models.Base.metadata.create_all(bind=engine)

app=FastAPI()



# my_data=[{"title" :"food","content":"pizza","id":1},{"title" :"game","content":"gta","id":2}]

# def find_post(id):
#     for i in my_data:
#         if i["id"]==id:
#             return i

# def find_index(id):
#     for i,n in enumerate(my_data):
#         if n["id"]==id:
#             return i

# while True:    
#     try:
#         conn=psycopg2.connect(host='localhost',database='fastapi_database',user='postgres',password='818818',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Data base connected succesfully")
#         break
#     except Exception as e:
#         print("Database not connected",e)
#         time.sleep(2)


    
    
@app.get("/")
def root():
    return ("Hello")


app.include_router(posts.router)
app.include_router(users.router)





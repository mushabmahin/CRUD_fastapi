#from random import randrange
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import Depends, FastAPI,Response,HTTPException,status
from pydantic import BaseModel
import time 
from . import models
from sqlalchemy.orm import Session
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app=FastAPI()



my_data=[{"title" :"food","content":"pizza","id":1},{"title" :"game","content":"gta","id":2}]

def find_post(id):
    for i in my_data:
        if i["id"]==id:
            return i

def find_index(id):
    for i,n in enumerate(my_data):
        if n["id"]==id:
            return i

while True:    
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi_database',user='postgres',password='818818',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Data base connected succesfully")
        break
    except Exception as e:
        print("Database not connected",e)
        time.sleep(2)


class Post(BaseModel):
    title:str
    content:str
    published:bool =False
    rating:Optional[int]=None
    
@app.get("/")
def root():
    return ("Hello")


@app.get("/sqlalchemy")
def test(db:Session =Depends(get_db)):
    return ("Success")
@app.get("/posts")
def get_posts():   
    cursor.execute("select * from posts")   
    post=cursor.fetchall()               #Read all
    return {"posts":post}

@app.get("/posts/{id}")
def get_post(id:int):                #Read one specific post
    cursor.execute("select * from posts where post_id=%s",str(id))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    return ({"data": post})

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute("insert into posts (title,content,published) values (%s,%s,%s) returning * ",(post.title,post.content,post.published))
    new_post=cursor.fetchone()
    conn.commit()
    return {"new_post":new_post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)  #Deleting a post (204 cant return anything)
def delete_post(id:int):
    cursor.execute("delete from posts where post_id=%s returning *",str(id))
    deleted_post=cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not present")
    
    return (Response(status_code=status.HTTP_204_NO_CONTENT))

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute("update posts set title=%s,content=%s,published=%s where post_id=%s returning *",(post.title,post.content,post.published,str(id)))
    updated_post=cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not present")
    
    return (updated_post)



from websockets import Router

from .. import models,schemas
from fastapi import Depends, FastAPI,Response,HTTPException,status,APIRouter
from ..database import engine,get_db
from sqlalchemy.orm import Session
from typing import List


router=APIRouter()

@router.get("/posts",response_model=List[schemas.PostResponse])
def get_posts(db:Session =Depends(get_db)):   
   # cursor.execute("select * from posts")   
   # post=cursor.fetchall()               #Read all
    posts=db.query(models.Post).all()
    return posts

@router.get("/posts/{id}",response_model=schemas.PostResponse)
def get_post(id:int,db:Session =Depends(get_db)):                #Read one specific post
    #cursor.execute("select * from posts where post_id=%s",str(id))
    #post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    return  post

@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post:schemas.CreatePost,db: Session = Depends(get_db)):
    #cursor.execute("insert into posts (title,content,published) values (%s,%s,%s) returning * ",(post.title,post.content,post.published))
    #new_post=cursor.fetchone()
    #conn.commit()
    
    new_post=models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)  #Deleting a post (204 cant return anything)
def delete_post(id:int,db:Session=Depends(get_db)):
    #cursor.execute("delete from posts where post_id=%s returning *",str(id))
    #deleted_post=cursor.fetchone()
    #conn.commit()
    deleted_post=db.query(models.Post).filter(models.Post.id==id)

    if  deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not present")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return (Response(status_code=status.HTTP_204_NO_CONTENT))

@router.put("/posts/{id}",response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.CreatePost,db:Session=Depends(get_db)):
    #cursor.execute("update posts set title=%s,content=%s,published=%s where post_id=%s returning *",(post.title,post.content,post.published,str(id)))
    #updated_post=cursor.fetchone()
    #conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id == id)
    updated_post=post_query.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not present")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
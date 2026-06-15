
from typing import Optional
from .. import models,schemas,oauth2
from fastapi import Depends,Response,HTTPException,status,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List


router=APIRouter(prefix="/posts",tags=['Posts'])

@router.get("/",response_model=List[schemas.PostResponse])
def get_posts(db:Session =Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit :int=10 ,skip:int=0,search: Optional[str]=""):   
   # cursor.execute("select * from posts")      
   # post=cursor.fetchall()               #Read all
    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/{id}",response_model=schemas.PostResponse)
def get_post(id:int,db:Session =Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):                #Read one specific post
    #cursor.execute("select * from posts where post_id=%s",str(id))
    #post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    return  post

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post:schemas.CreatePost,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute("insert into posts (title,content,published) values (%s,%s,%s) returning * ",(post.title,post.content,post.published))
    #new_post=cursor.fetchone()
    #conn.commit()
    print(current_user.email)
    
    new_post=models.Post(user_id=current_user.id,**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)  #Deleting a post (204 cant return anything)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute("delete from posts where post_id=%s returning *",str(id))
    #deleted_post=cursor.fetchone()
    #conn.commit()
    deleted_post=db.query(models.Post).filter(models.Post.id==id)
    deleted=deleted_post.first()
    if  deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not present")
    
    if deleted.user_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to delete")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return (Response(status_code=status.HTTP_204_NO_CONTENT))

@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.CreatePost,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute("update posts set title=%s,content=%s,published=%s where post_id=%s returning *",(post.title,post.content,post.published,str(id)))
    #updated_post=cursor.fetchone()
    #conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id == id)
    updated_post=post_query.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not present")
    
    if updated_post.user_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to delete")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
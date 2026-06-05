from fastapi import status, Depends,APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas,models,utils,oauth2
router=APIRouter(tags=["Login"])

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm =Depends(),db: Session = Depends(get_db)):

    # OAuth2PasswordRequestForm storage format
    # {
    #     "username":"afaad",
    #     "password":"Afeqfe"
    # }  so we have to change email to user (next sentence)
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials")

    verification = utils.verify(
        user_credentials.password,
        user.password
    )

    if not verification:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    access_token=oauth2.create_token(data={"user_id":user.id})
    return {"token": access_token,"token_type":"bearer"}
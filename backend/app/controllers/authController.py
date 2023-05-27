from fastapi import HTTPException, status
from ..utils import verify, check_admin_role
from . import oauth2



def login_user(user_credentials, db, model, role):
    if not (role and check_admin_role(type=role)):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    user = db.query(model).filter(model.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!")
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invaild Credentials")
    access_token = oauth2.create_access_token({"user_id": user.id, "role": role})
    return {"access_token": access_token, "token_type": "bearer"} 
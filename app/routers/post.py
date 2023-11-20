from app import oauth2
from .. import models, schemas
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func


router = APIRouter(
    prefix='/posts', tags=['posts']
)


@router.get('/',response_model=List[schemas.PostOut] )
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = '',):
    posts = db.query(models.Post).filter(models.Post.title.contains(
        search)).limit(limit=limit).offset(offset=skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(
        search)).limit(limit=limit).offset(offset=skip).all()

    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return results


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # cursor.execute(
    #     """INSERT INTO posts(title, content, published ) values (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')

    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # cursor.execute(
    #     """DELETE FROM posts where id = %s RETURNING *""", (str(id),))
    # post = cursor.fetchone()
    # conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform action ')

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}',  response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id),))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_val = post_query.first()

    if post_val == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')

    if post_query.first() != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform action ')

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()

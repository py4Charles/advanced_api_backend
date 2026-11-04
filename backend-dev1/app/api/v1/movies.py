from fastapi import FastAPI, HTTPException, APIRouter, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import text, select,insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel, field_validator
from datetime import datetime
from jose import JWTError
import uuid

from app.api.v1 import users
from app.core.database import get_db
from app.models.movies import CreateMovieMock, MovieList
from app.core.security import verify_token
from app.core.database import init_db

security = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()
db = get_db()


@field_validator('title')
@classmethod
def validate_title(cls, v):
    if len(v) < 5:
        raise ValueError("title has to be atleast 5 characters")
    return v
    
@field_validator('rating')
@classmethod
def validate_rating(cls, v):
    if v > 10.0:
        raise ValueError("rating can not be more than 10.0")
    return v
    ``
@field_validator('duration')
@classmethod
def validate_duration(cls, v):
    if v < 70:
        raise ValueError("duration can not be less than 1hr 10mins")
    return v
    
 
async def get_current_user(credentials = Depends(security)):
    
    token = credentials
    
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        role = payload.get("role")
        
        if user_id is None:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "Invalid authenttication token: missing subject (sub)",
                headers= {"WWW-Authentication": "Bearer"}
            )
        
        return {"user": user_id, "role": role}
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Could not validate credentials",
            headers= {"WWW-Authentication": "Bearer"}
        )
 
@router.get("/", response_model= dict)
async def get_all_movies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieList))
    movies = result.scalars().all()
    
    return {
        "success": True,
        "data": [{
            "id": movie.id,
            "title": movie.title,
            "category": movie.category,
            "description": movie.description,
            "poster_url": movie.poster_url,
            "trailer_url": movie.trailer_url,
            "duration": movie.duration,
            "release_year": movie.release_year,
            "rating": movie.rating,
            "cast_members": movie.cast_members,
            "producer": movie.producer,
            "views": movie.views,
            "created_at": movie.created_at.isoformat() if movie.created_at is not None else None,
            "updated_at": movie.updated_at.isoformat() if movie.updated_at is not None  else None
        } for movie in movies]
    }
       

@router.get("/{movie_id}")
async def get_movie_by_id(
    movie_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(MovieList).filter(MovieList.id == movie_id))
    movie = result.scalar_one_or_none()
    
    if not movie:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "movie not found"
        )
    
    return {
        "success": True,
        "data": {
            "id": movie.id,
            "title": movie.title,
            "category": movie.category,
            "description": movie.description,
            "poster_url": movie.poster_url,
            "trailer_url": movie.trailer_url,
            "duration": movie.duration,
            "release_year": movie.release_year,
            "rating": movie.rating,
            "cast_members": movie.cast_members,
            "producer": movie.producer,
            "views": movie.views,
            "created_at": movie.created_at.isoformat() if movie.created_at is not None else None,
            "updated_at": movie.updated_at.isoformat() if movie.updated_at is not None else None
        }
    }


@router.post("/", response_model= dict)       
async def create_movie(
    request: CreateMovieMock,
    db: AsyncSession = Depends(get_db)
):
    movie = MovieList(
        title=request.title,
        category=request.category if hasattr(request, 'category') else None,
        description=request.description if hasattr(request, 'description') else None,
        poster_url=request.poster_url if hasattr(request, 'poster_url') else None,
        trailer_url=request.trailer_url if hasattr(request, 'trailer_url') else None,
        duration=request.duration if hasattr(request, 'duration') else None,
        release_year=request.release_year if hasattr(request, 'release_year') else None,
        rating=request.rating if hasattr(request, 'rating') else None,
        cast_members=request.cast_members if hasattr(request, 'cast_members') else None,
        producer=request.producer if hasattr(request, 'producer') else None
    )
    
    db.add(movie)
    await db.commit()
    await db.refresh(movie)
    
    return {
        "message": "Movie added successfully to database",
        "data": {
            "id": movie.id,
            "title": movie.title,
            "category": movie.category
        }
    }
    
    
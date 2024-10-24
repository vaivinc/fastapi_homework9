from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI()


@app.get("/")
async def docs():
    return RedirectResponse("/docs")


class Movie(BaseModel):
    id: int = Field(min_length=1)
    title: str
    director: str
    release_year: int = Field(min_length=1, max_length=2024)
    rating: float = Field(min_length=1, max_length=5)


class ListMovie(BaseModel):
    movies: list[Movie]
    count_movies: int


movie_db = [
    Movie(id=1, title="Inception", director="Christopher Nolan", release_year=2010, rating=8.8),
    Movie(id=2, title="The Matrix", director="Wachowski Sisters", release_year=1999, rating=8.7),
    Movie(id=3, title="Interstellar", director="Christopher Nolan", release_year=2014, rating=8.6)
]


@app.get("/movies", response_model=ListMovie)
async def get_movie():
    return ListMovie(movies=movie_db, count_movies=len(movie_db))


@app.post("/movies", response_model=Movie)
async def create_movie(movie: Movie):
    if movie.id not in movie_db:
        movie_db.append(movie)
        return movie
    raise HTTPException(status_code=404, detail="Movie not found")


@app.get("/movies/{id}", response_model=Movie)
async def get_movie_by_id(id: int):
    for movie in movie_db:
        if movie.id == id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")


@app.delete("/movies/{id}", response_model=Movie)
async def get_movie_by_id(id: int):
    for movie in movie_db:
        if movie.id == id:
            movie_db.remove(movie)
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

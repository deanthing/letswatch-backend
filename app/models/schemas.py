# Model Schemas
from app import ma

# from .user import User
from .models import Group, User, Movie, Genre, ReleasePeriod, Like

# short hand for ma objects
Fields = ma.fields
Nested = ma.fields.Nested
Schema = ma.SQLAlchemyAutoSchema


class GroupSchema(Schema):
    class Meta:
        model = Group

    users = Nested("UserSchema")
    likes = Nested("LikeSchema")
    genres = Nested("GenresSchema", exclude=("groups", "movies"))


class UserSchema(Schema):
    class Meta:
        model = User


class LikeSchema(Schema):
    class Meta:
        model = Like


class MovieSchema(Schema):
    class Meta:
        model = Movie

    genres = Nested("GenresSchema", exclude=("groups, movies"))
    likes = Nested("LikeSchema")


class GenreSchema(Schema):
    class Meta:
        model = Genre

    movies = Nested("MovieSchenma", exclude=("genres", "likes"))
    groups = Nested("GroupScehma", exclude=("genres", "release_periods"))


class ReleasePeriodSchemas(Schema):
    class Meta:
        model = ReleasePeriod

    groups = Nested("GroupScehma", exclude=("genres, release_periods"))

from app import db

Column = db.Column
Model = db.Model
relationship = db.relationship

# many to many insertion
# p = Movie()
# c = genre()
# p.children.append(c)
# db.session.add(p)
# db.session.commit()

group_genre_table = db.Table('group_genre_table', db.Model.metadata,
                             db.Column('group_id', db.Integer,
                                       db.ForeignKey('group.id'), primary_key=True),
                             db.Column('genre_id', db.Integer,
                                       db.ForeignKey('genre.id'), primary_key=True)
                             )

group_release_table = db.Table('group_release_table', db.Model.metadata,
                               db.Column('group_id', db.Integer,
                                         db.ForeignKey('group.id'), primary_key=True),
                               db.Column('release_id', db.Integer,
                                         db.ForeignKey('releaseperiod.id'), primary_key=True)
                               )


class Group(Model):
    __tablename__ = 'group'
    id = Column(db.Integer, primary_key=True)
    users = relationship("User", backref="group", lazy=True)
    likes = relationship("Like", backref="group", lazy=True)
    genres = db.relationship(
        "Genre", secondary=group_genre_table, back_populates="groups", lazy=True)
    release_periods = db.relationship(
        "ReleasePeriod", secondary=group_release_table, lazy=True, back_populates="groups")
    in_waiting_room = Column(db.Boolean, nullable=False)

    def all_liked_movies(self):
        movies_dict = dict()
        for like in self.likes:
            if like.movie_id not in movies_dict:
                movies_dict[like.movie_id] = 1
            else:
                movies_dict[like.movie_id] += 1

        num_users = len(self.users)
        found_movies = []
        for movie in movies_dict.keys():
            if movies_dict[movie] == num_users:
                found_movies.append(movie)

        return found_movies


class User(Model):
    __tablename__ = 'user'
    id = Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    isOwner = db.Column(db.Boolean)
    group_id = Column(db.Integer, db.ForeignKey('group.id'), nullable=False)


class Like(Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    group_id = Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    movie_id = Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)


movie_genre_table = db.Table('movie_genre_table', db.Model.metadata,
                             db.Column('movie_id', db.Integer,
                                       db.ForeignKey('movie.id'), primary_key=True),
                             db.Column('genre_id', db.Integer,
                                       db.ForeignKey('genre.id'), primary_key=True)
                             )


class Movie(Model):
    __tablename__ = 'movie'
    id = Column(db.Integer, primary_key=True)
    tmdb_id = Column(db.Integer, nullable=False)
    title = db.Column(db.String(80))
    blurb = db.Column(db.String(500))
    picture = db.Column(db.String(80))
    release_period_id = Column(db.Integer, db.ForeignKey('release.id'))
    genres = relationship(
        "Genre", secondary=movie_genre_table, back_populates="movies", lazy=True)
    likes = relationship("Like", backref="movie", lazy=True)


class Genre(Model):
    __tablename__ = 'genre'
    id = Column(db.Integer, primary_key=True)
    genre_name = Column(db.String(64), unique=True)
    movies = relationship(
        "Movie", secondary=movie_genre_table, back_populates="genres", lazy=True)
    groups = relationship(
        "Group", secondary=group_genre_table, back_populates="genres", lazy=True)


class ReleasePeriod(Model):
    __tablename__ = 'releaseperiod'
    id = Column(db.Integer, primary_key=True)
    release_period_name = Column(db.String(64), unique=True, nullable=False)
    lower_bound = Column(db.Integer)
    upper_bound = Column(db.Integer)
    groups = relationship(
        "Group", secondary=group_release_table, back_populates="release_periods", lazy=True)

from data_manager import DataManagerInterface
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# Models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    director = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_url="sqlite:///movies.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def get_all_users(self):
        with self.Session() as session:
            return session.query(User).all()

    def get_user_movies(self, user_id):
        # Implement this method based on user-movie relationships if applicable
        raise NotImplementedError("This method is not implemented yet.")

    def add_user(self, user):
        with self.Session() as session:
            session.add(user)
            session.commit()

    def delete_user(self, user_id):
        with self.Session() as session:
            user = session.get(User, user_id)
            if user:
                session.delete(user)
                session.commit()
                return True
            return False

    def add_movie(self, movie):
        with self.Session() as session:
            session.add(movie)
            session.commit()

    def update_movie(self, movie_id, movie_data):
        with self.Session() as session:
            movie = session.get(Movie, movie_id)
            if movie:
                movie.name = movie_data.get('name', movie.name)
                movie.director = movie_data.get('director', movie.director)
                movie.year = movie_data.get('year', movie.year)
                movie.rating = movie_data.get('rating', movie.rating)
                session.commit()
                return movie
            return None

    def delete_movie(self, movie_id):
        with self.Session() as session:
            movie = session.get(Movie, movie_id)
            if movie:
                session.delete(movie)
                session.commit()
                return True
            return False

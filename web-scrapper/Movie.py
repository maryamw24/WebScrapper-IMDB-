class Movie:
    def __init__(self, title: str, year: int, certificate: str, duration: int, genre: str, rating: float,
                 description: str, director: str, votes: int) -> None:
        self.__title: str = title
        self.__year: int = year
        self.__certificate: str = certificate
        self.__duration: int = duration
        self.__genre: str = genre
        self.__rating: float = rating
        self.__description: str = description
        self.__director: str = director
        self.__votes: int = votes

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def year(self):
        return self.__year

    @year.setter
    def releaseYear(self, value):
        self.__year = value

    @property
    def certificate(self):
        return self.__certificate

    @certificate.setter
    def certificate(self, value):
        self.__certificate = value

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        self.__duration = value

    @property
    def genre(self):
        return self.__genre

    @genre.setter
    def genre(self, value):
        self.__genre = value

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        self.__rating = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    @property
    def director(self):
        return self.__director

    @director.setter
    def director(self, value):
        self.__director = value

    @property
    def votes(self):
        return self.__votes

    @votes.setter
    def votes(self, value):
        self.__votes = value

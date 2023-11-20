
from uuid import uuid4

from errors.errors import DBError, ObjectNotFound, Unauthorized
from server.envconfig import confdb
from server.instance import server

app, api, db = server.app, server.api, server.db

class Guest_DB(db.Model):
    __tablename__   = 'guest'
    __bind_key__    = confdb.db_santa_name
    link            = db.Column(db.String(36), primary_key=True, unique=True)
    secret_santa_id = db.Column(db.Integer, db.ForeignKey('secret_santa.id'), nullable=False)
    name            = db.Column(db.String(64), nullable=False)
    email           = db.Column(db.String(64), nullable=False)
    target          = db.Column(db.String(64), nullable=False)
    target_email    = db.Column(db.String(64), nullable=False)

    def __str__(self) -> str:
        return f"{self.link} - {self.name} - {self.email} - {self.target} - {self.target_email}"
    
    def to_dict(self) -> dict:
        return {
            "link": self.link,
            "name": self.name,
            "email": self.email,
            "target": self.target,
            "target_email": self.target_email
        }

    def get(self) -> dict:
        try:
            guest = db.session.query(self.__class__).get(self.link)
        except:
            raise DBError("Error database consulting")
        if guest:
            return guest.to_dict()
        else:
            raise ObjectNotFound(f"Error : No guest find for link {self.link}")

    def create(self) -> None:
        self.link = str(uuid4())
        for i in range(3):
            if db.session.query(self.__class__).get(self.link):
                if i == 2:
                    raise DBError("Error during creation of new guest")
                self.link = str(uuid4())
                continue
            break

        if not db.session.query(self.__class__).get(self.link):
            db.session.add(self)
            db.session.commit()
        else:
            raise DBError(f"Error during creation of new guest: ID [{self.link}]")

class Secret_santa_DB(db.Model):
    __tablename__   = 'secret_santa'
    __bind_key__    = confdb.db_santa_name
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator         = db.Column(db.String(64), nullable=False)
    name            = db.Column(db.String(64), nullable=False)
    date_end        = db.Column(db.Date, nullable=False)

    def __str__(self) -> str:
        return f"{self.link} - {self.name} - {self.email} - {self.target} - {self.target_email}"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "creator": self.creator,
            "name": self.name,
            "date_end": str(self.date_end),
        }

    def get(self) -> dict:
        try:
            secret_santa:Secret_santa_DB = db.session.query(self.__class__).get(self.id)
        except:
            raise DBError("Error database consulting")
        if not secret_santa:
            raise ObjectNotFound(f"Error : No secret santa find for id {self.id}")
        return secret_santa.to_dict()

    def create(self) -> int:
        try:
            db.session.add(self)
            db.session.commit()
        except:
            raise DBError("Error during creation of new secret santa")
        return self.id

    def delete(self) -> None:
        secret_santa = self.get()
        if not secret_santa:
            raise ObjectNotFound(f"Error : No secret santa find for id {self.id}")
        if secret_santa.creator != self.creator:
            raise Unauthorized("Error : You're not authorized to delete this secret santa")
        try:
            for guest in secret_santa.list_guests():
                db.session.delete(guest)
            db.session.delete(secret_santa)
            db.session.commit()
        except:
            raise DBError("Error during suppression of secret santa")

    def list_guests(self) -> list[Guest_DB]:
        try:
            guests = db.session.query(Guest_DB).filter_by(secret_santa_id=self.id).all()
        except:
            raise DBError("Error database consulting")
        guests.sort(key=lambda guest:guest.name)
        return guests

try:
    with app.app_context():
        db.create_all(bind_key=confdb.db_santa_name)
except Exception as e:
    print(e)
    pass
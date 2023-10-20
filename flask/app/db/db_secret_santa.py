
from uuid import uuid4

from errors.errors import DBError, ObjectNotFound
from server.envconfig import confdb
from server.instance import server

app, api, db = server.app, server.api, server.db

class Guest_DB(db.Model):
    __tablename__   = 'guest'
    __bind_key__    = confdb.db_santa_name
    link            = db.Column(db.String(36), primary_key=True, unique=True)
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

    def add_guest(guest:dict) -> dict:
        link = str(uuid4())
        for i in range(3):
            if db.session.query(Guest_DB).get(link):
                if i == 2:
                    raise DBError(f"Error during creation of new guest")
                link = str(uuid4())
                continue
            break

        new_guest = Guest_DB(
            link=link,
            name=guest.get("name"),
            email=guest.get("email"),
            target=guest.get("target"),
            target_email=guest.get("target_email")
        )
        new_guest.to_dict()

        if not db.session.query(Guest_DB).get(new_guest.link):
            db.session.add(new_guest)
            db.session.commit()
        else:
            raise DBError(f"Error during creation of new guest: ID [{new_guest.link}]")
        return new_guest.to_dict()

    def get_guest(link:str) -> dict:
        try:
            guest = db.session.query(Guest_DB).get(link)
        except:
            raise DBError(f"Error database consulting")
        if guest:
            return {"name": guest.name, "email": guest.email, "target": guest.target, "target_email": guest.target_email}
        else:
            raise ObjectNotFound(f"Error : No guest find for link {link}")


class User(db.Model):
    __bind_key__ = confdb.db_santa_name
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "id: %i, name: %s" % (self.id, self.name)

    def add_user(self):
        if not db.session.query(User).get(self.id):
            db.session.add(self)
            db.session.commit()
        else:
            raise DBError("Un element avec la meme clé primaire existe déjà")

try:
    with app.app_context():
        db.create_all(bind_key=confdb.db_santa_name)
except Exception as e:
    print(e)
    pass

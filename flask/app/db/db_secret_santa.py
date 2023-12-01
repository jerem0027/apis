
from core.colors import red
from errors.errors import DBError, ObjectNotFound, Unauthorized
from server.envconfig import confdb
from server.instance import server

app, api, db = server.app, server.api, server.db

class Guest_DB(db.Model):
    __tablename__   = 'guest'
    __bind_key__    = confdb.db_home_name
    link            = db.Column(db.String(36), primary_key=True, unique=True)
    secret_santa_id = db.Column(db.Integer, db.ForeignKey('secret_santa.id'), nullable=False)
    name            = db.Column(db.String(64), nullable=False)
    email           = db.Column(db.String(64), nullable=False)
    target_link     = db.Column(db.String(36), nullable=False, unique=True)
    user            = db.Column(db.String(64), db.ForeignKey('users.pseudo'), nullable=True)
    gift1           = db.Column(db.String(36), nullable=True)
    gift2           = db.Column(db.String(36), nullable=True)
    gift3           = db.Column(db.String(36), nullable=True)
    gift4           = db.Column(db.String(36), nullable=True)
    gift5           = db.Column(db.String(36), nullable=True)

    def to_dict(self) -> dict:
        return {
            "link": self.link,
            "name": self.name,
            "email": self.email,
            "target_link": self.target_link,
            "gift_list": [
                self.gift1 if self.gift1 else "",
                self.gift2 if self.gift2 else "",
                self.gift3 if self.gift3 else "",
                self.gift4 if self.gift4 else "",
                self.gift5 if self.gift5 else ""
            ],
            "user": self.user
        }

    def get(self) -> "Guest_DB":
        try:
            guest = db.session.query(self.__class__).get(self.link)
        except:
            raise DBError("Error database consulting")
        if not guest:
            raise ObjectNotFound(f"Error : No guest find for link {self.link}")
        return guest

    def update(self) -> None:
        try:
            guest = db.session.query(self.__class__).get(self.link)
        except:
            raise DBError("Error database consulting")
        if not guest:
            raise ObjectNotFound(f"Error : No guest find for link {self.link}")
        for i in range(1,6):
            guest_gift = getattr(guest, f"gift{i}")
            self_gift = getattr(self, f"gift{i}")
            if guest_gift != self_gift and self_gift != None:
                setattr(guest, f"gift{i}", self_gift)
        if self.user != None:
            guest.user = self.user
        try:
            db.session.add(guest)
            db.session.commit()
        except:
            raise DBError("Error during update of user")

    def create(self) -> None:
        if not db.session.query(self.__class__).get(self.link):
            db.session.add(self)
            db.session.commit()
        else:
            raise DBError(f"Error during creation of new guest: ID [{self.link}]")

    def list_guest(self) -> list["Guest_DB"]:
        try:
            guest = db.session.query(self.__class__).filter_by(user=self.user).all()
        except:
            raise DBError("Error database consulting")
        guest.sort(key=lambda guest:guest.secret_santa_id, reverse=True)
        return guest

    def get_guest_from_sesa(self) -> "Guest_DB":
        try:
            guest = db.session.query(self.__class__).filter_by(user=self.user, secret_santa_id=self.secret_santa_id).first()
        except:
            raise DBError("Error database consulting")
        return guest

class Secret_santa_DB(db.Model):
    __tablename__   = 'secret_santa'
    __bind_key__    = confdb.db_home_name
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator         = db.Column(db.String(64), db.ForeignKey('users.pseudo'), nullable=False)
    name            = db.Column(db.String(64), nullable=False)
    date_end        = db.Column(db.Date, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "creator": self.creator,
            "name": self.name,
            "date_end": str(self.date_end),
        }

    def get(self) -> "Secret_santa_DB":
        try:
            secret_santa:Secret_santa_DB = db.session.query(self.__class__).get(self.id)
        except:
            raise DBError("Error database consulting")
        if not secret_santa:
            raise ObjectNotFound(f"Error : No secret santa find for id {self.id}")
        return secret_santa

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

    def update(self) -> None:
        secret_santa = self.get()
        if not secret_santa:
            raise ObjectNotFound(f"Error : No secret santa find for id {self.id}")
        if secret_santa.creator != self.creator:
            raise Unauthorized("Error : You're not authorized to update this secret santa")
        for key in ["name", "date_end"]:
            if getattr(self, key):
                setattr(secret_santa, key, getattr(self, key))
        try:
            db.session.add(secret_santa)
            db.session.commit()
        except:
            raise DBError("Error during update of secret santa")

    def list_guests(self) -> list[Guest_DB]:
        try:
            guests = db.session.query(Guest_DB).filter_by(secret_santa_id=self.id).all()
        except:
            raise DBError("Error database consulting")
        guests.sort(key=lambda guest:guest.name)
        return guests

    def list_secret_santa(self) -> list["Secret_santa_DB"]:
        try:
            secret_santa = db.session.query(self.__class__).filter_by(creator=self.creator).all()
        except:
            raise DBError("Error database consulting")
        secret_santa.sort(key=lambda sesa:sesa.date_end)
        return secret_santa

try:
    with app.app_context():
        db.create_all(bind_key=confdb.db_home_name)
except Exception as e:
    print(red(e))
    pass
from ipaddress import IPv4Address

from pydantic import BaseModel, Extra, Field, validator

class Model(BaseModel):
    constructeur: str = Field (
        description="Marque de la voiture",
        title="Marque",
        max_length=11,
        pattern="[A-Z][a-z]+"
    )
    modele: str

    class Config:
        extra = Extra.forbid

    @validator('modele', always=True)
    def check_special(cls, v, values):
        if v == "Playstation 6" and values["constructeur"] == "Sony":
            return "Playstation 5"
        return v

class Console(BaseModel):
    nom: Model = Field (
        title="Nom",
        description="Constructeur et modele de la console",
    )
    annee: int = Field (
        title="Puissance du Moteur",
        description="Annee de sortie de la console",
        ge=2000
        )
    couleur: str = Field (
        title="Couleur",
        description="Couleur de la console",
        max_length=10,
        pattern="[A-Z][a-z]+"
    )

class Consoles(BaseModel):
    consoles: list[Console] = Field(
        max_items=10,
        # unique_items=True
    )

class ItemsParams:
    def __init__(self, skip: int = 0, limit: int = 2):
        self.skip = skip
        self.limit = limit

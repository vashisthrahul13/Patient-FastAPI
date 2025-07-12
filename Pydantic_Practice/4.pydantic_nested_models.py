from pydantic import BaseModel

class Address(BaseModel):

    city:str
    state:str
    pin:str


class Patient(BaseModel):

    name:str
    gender:str
    age:int
    address: Address


address_dict = {'city':'new delhi','state':'delhi','pin':'110043'}

address1 = Address(**address_dict)

patient = {'name':'rahul','gender':'male','age':'26','address':address1}    #nested model

patient1 = Patient(**patient)

print(patient1)
print(patient1.address.city)
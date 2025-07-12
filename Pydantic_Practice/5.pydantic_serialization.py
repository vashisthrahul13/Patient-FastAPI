from pydantic import BaseModel

class Address(BaseModel):

    city:str
    state:str
    pin:str


class Patient(BaseModel):

    name:str = 'NoBody'
    gender:str
    age:int
    address: Address


address_dict = {'city':'new delhi','state':'delhi','pin':'110043'}

address1 = Address(**address_dict)

patient = {'gender':'male','age':'26','address':address1}

patient1 = Patient(**patient)

temp = patient1.model_dump()   #converts model to python dictionary
print(temp)
print(type(temp))
print('*'* 50)

temp1 = patient1.model_dump_json()
print(temp1)
print(type(temp1))
print('*'* 50)

temp2 = patient1.model_dump(include=['name'])
print(temp2)
print(type(temp2))
print('*'* 50)

temp3 = patient1.model_dump(exclude={'address':['state']})
print(temp3)
print(type(temp3))
print('*'* 50)

temp4 = patient1.model_dump(exclude_unset=True) #exclude variables whose value has been explicitly set
print(temp4)
print(type(temp4))
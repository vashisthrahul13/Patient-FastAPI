from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator, model_validator
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):

    name:str
    email : EmailStr
    linkedin : AnyUrl
    age:int 
    allergies: List[str]    
    allergies2:List[str] 
    weight:float  
    married :bool
    contact_details : Dict[str,str]

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains = ['gmail.com','yahoo.com']

        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        
        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()
    
    @field_validator('age',mode='after')    #mode = after -> value received is after type conversion
    @classmethod
    def validate_age(cls,value):
        if 0<value<120:
            return value
        else:
            raise ValueError('Age should be between 0 and 120')
    
    #model validator
    @model_validator(mode = 'after')
    def validate_emergency_contact(cls,model):
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have emergency contact details')
        return model


def insert_patient_data(patient : Patient):

    print(patient.name)
    print(patient.age)
    print('Inserted')


def update_patient_data(patient : Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print('updated')

patient_info = {'name':'rahul',
                'email':'rahul@gmail.com',
                'age':88,
                'weight':72,
                'married':True,
                'allergies':['Dust'],
                'allergies2':['lala'],
                'contact_details':{'email':'test@123','PH':'123455','emergency':'9883'},
                'linkedin' : 'http://linkedin.com/1234'}

patient1 = Patient(**patient_info)

update_patient_data(patient1)
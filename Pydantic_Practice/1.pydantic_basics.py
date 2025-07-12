from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):

    name: Annotated[str,Field(max_length=50,title='name of the patient',examples=['Rahul','Test'])] #Annotated method is used to add meta deta -> it will also be shown in fast api documentation
    email : EmailStr
    linkedin : AnyUrl
    age:int = Field(gt=0,lt=130)
    allergies: Optional[List[str]] = None    #typing.List is used to so that even the datatype of items in list can be specified ; None is the default value
    allergies2: Annotated[Optional[List[str]], Field(default=None,max_length=5)]   #typing.List is used to so that even the datatype of items in list can be specified ; None is the default value
    weight:float = Annotated[float,Field(gt=0 , strict=True)]  #gt -> greater than ; Strict = True will not allow auto type conversion from '76.2' to float 76.2
    married : Annotated[bool,Field(default=False, description='Martial status of the patient')] #default value
    contact_details : Dict[str,str]

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
                'age':30,
                'weight':72,
                'married':True,
                'allergies':['Dust'],
                'allergies2':['lala'],
                'contact_details':{'email':'test@123','PH':'123455'},
                'linkedin' : 'http://linkedin.com/1234'}

patient1 = Patient(**patient_info)

update_patient_data(patient1)
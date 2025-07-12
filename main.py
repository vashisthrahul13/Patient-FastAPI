from fastapi import FastAPI,HTTPException,Path,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,field_validator, Field,computed_field
from typing import Annotated,Literal


app = FastAPI()

#pydantic model
class Patient(BaseModel):

    id : Annotated[str,Field(...,description = 'Patient ID' ,examples = ['POO1'])]
    name : Annotated[str,Field(...,description='Name of the patient')]
    city : Annotated[str,Field(title='City where the patient is living')]
    age: Annotated[int,Field(...,description='Age of the patient',gt=0,lt=120)]
    gender : Annotated[Literal['male','female','other'],Field(...,description='Gender of the patient')]
    height : Annotated[float, Field(...,description='Height of the Patient') ]
    weight : Annotated[float, Field(...,description='Weight of the patient')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str :
        if self.bmi <18.5:
            return 'Underweight'
        elif self.bmi <25:
            return 'Normal'
        elif self.bmi<30:
            return 'Overweight'
        else:
            return 'Obese'




def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
        return data
    
def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

    
@app.get('/')
def home():
    return {'message' : 'Patient Management System API'}

@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}

@app.get('/view')
def view():
    data = load_data()
    return (data)

@app.get('/patient/{patient_id}')   #path parameter demo
def view_patient(patient_id:str = Path(...,description='ID of the patient in the DB',example='P001')):

    data = load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404,detail='Not Found. Patient not found') #404 = Not found , Resource doesnt exist
    
@app.get('/sort')
def sort_patients(sort_by:str = Query(...,description='Sort on the basis of height/weight/bmi'), order:str = Query(default='asc',description='sort in asc/desc order')):

    valid_fields = ['height','weight','bmi']
    sort_order = True if order=='desc' else False
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'Bad Request. Select from {valid_fields}')    #400 = Bad Request: Malformed or invalid Request
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Bad Request. Select between asc/desc')
    
    data = load_data()  #load data
    print('/' * 50)
    print(type(data))   #
    sorted_data = sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order) #sort the data

    return sorted_data

@app.post('/create')
def create_patient(patient : Patient):

    #load existing data
    data = load_data()

    #check if the patient already exist
    if patient.id in data:
        print('Patient matched if condition')
        raise HTTPException(status_code=400, detail='Patient already exists')
    
    #add new patient to database
    data[patient.id] = patient.model_dump(exclude=['id'])

    #save data to json file
    save_data(data)

    return JSONResponse(status_code=201, content='Data Successful added to DB')
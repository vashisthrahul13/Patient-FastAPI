from fastapi import FastAPI,HTTPException,Path,Query
import json

app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
        return data
    
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
from fastapi import FastAPI, Path, HTTPException, Query 
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal,  Optional

app = FastAPI()

class Patient(BaseModel) :

      id: Annotated[str, Field(..., description='id of the patient', examples=['P001'])]
      name: Annotated[str, Field(..., description='name of patient')]
      city: Annotated[str, Field(..., description='city of patient')]
      age: Annotated[int, Field(..., gt=0 , lt=120 ,description='age of patient')]
      gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='gender')]
      height: Annotated[float, Field(...,gt=0, description='city of patient')]
      weight: Annotated[float, Field(...,gt=0, description='city of patient')]

      @computed_field
      @property
      def bmi(self) -> float:
            bmi = round((self.weight)/(self.height**2),2)
            return bmi
      
      @computed_field
      @property
      def verdict(self)-> str:
            if self.bmi <18.5:
                  return 'underweight'
            elif self.bmi<25:
                  return 'normal'
            elif self.bmi<30:
                  return 'normal'
            else: 
                  return 'obeese'
            

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal["male", "female"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
      with open('patients.json', 'r') as f:
            data = json.load(f)

      return data  

#saving the uploaded data

def save_data(data):
      with open('patients.json', 'w') as f:
            json.dump(data, f)

@app.get("/")
def hello():
      return {'meg': 'hello'}

@app.get('/about')
def about():
     return {'message': 'this a demo and start of agni alert project'} 

@app.get ('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., descreption='ID of the patient in the DB', example='P001')) :
      #load all the patients
      data = load_data()

      if patient_id in data:
            return data[patient_id]
      raise HTTPException(status_code=404, detail= 'patient not found') 

@app.get ('/sort')
def sort_patients(sort_by: str = Query(..., description= 'sort on basis of height,weight or bmi'), order: str = Query('asc', description='sort in asc or decs order')):

      validate_fields = ['height', 'weight' , 'bmi']

      if sort_by not in validate_fields:
            raise HTTPException(status_code=404, detail=f'invalid field select from{validate_fields}')
      
      if order not in ['asc', 'desc']:
            raise HTTPException(status_code=400, detail='invalid order')
      
      data = load_data()

      sort_order = True if order=='desc' else False

      sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse=sort_order)

      return sorted_data 


@app.post ('/create')
def create_patient(patient: Patient):

      data = load_data()
      #check if the patient already exists
      if patient.id in data:
            raise HTTPException(status_code= 400, detail= 'patient already exists')
      #new patinet add to the DB
      data[patient.id] = patient.model_dump(exclude=['id'])

      #save into json 
      save_data(data)

      return JSONResponse(status_code=201, content={'message':'patient created successfully '})


#put 
@app.put ('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate): 
      
      data = load_data()
      if patient_id not in data:
            raise HTTPException(status_code=404, detail='patient not fount')
      
      existing_patient_info = data[patient_id]

      updated_patient_info =   patient_update.model_dump(exclude_unset = True) #unset exclude keeps only those who are given by user 

      for key , value  in updated_patient_info.items():
            existing_patient_info[key] = value
      #existing patient info to pydantic onj then update bmi and verdict
      existing_patient_info['id'] = patient_id
      
      patient_pydantic_obj = Patient(**existing_patient_info)
      #pydantic obj to dictionary
      existing_patient_info =  patient_pydantic_obj.model_dump(exclude='id')
      #add this dictionary to data
      data[patient_id] = existing_patient_info 

      #save data
      save_data(data)      


      return JSONResponse(status_code=200 , content={'message' : 'patient updated'})

#delete
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'patient deleted'})


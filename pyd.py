from pydantic import BaseModel

class Patient(BaseModel):

      name: str
      age: int
      weight: int


def insert_patient_data(patient: Patient):

      print(patient.name)
      print(patient.age)
      print('inserted')

      patient_info = {'name' : 'mohit' , 'age' : 25}
      patient1 = Patient(**patient_info)

      insert_patient_data(patient1)
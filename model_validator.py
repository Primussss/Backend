from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):

      name: str
      email: EmailStr
      age: int
      weight: float = Field(gt = 0 )
      married: bool
      allergies: List[str] #all elements in list are strings as well
      contact_details: Dict[str, str]

      @model_validator(mode = 'after')
      def validate_emergnecy_contact(cls,model):
              if model.age > 60 and 'emergency' not in model.contact_details:
                      raise ValueError('patients odler than 60 must have an eme_con')
              return model



def update_patient_data(patient: Patient):
            print(patient.name)
            print(patient.age)
            print(patient.allergies)
            print(patient.married)
            print('updated')

            patient_info = {'name':'nitesh', 'email':'dgf@hdfc.com','age':'30', 'weight':75.3 ,'married':True , 'allergies':['pollen', 'dust'], 'contact_details': '545481245' }

            patient1 = Patient(**patient_info)

            update_patient_data(patient1)     
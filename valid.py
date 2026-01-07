from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated
#pyd gives special data type built in for data validation which may not be py data types
#Emailstr, 
#filed func is used to add meta data 
class Patient(BaseModel):

      name: str
      email: EmailStr
      age: int
      weight: float = Field(gt = 0 )
      married: bool
      allergies: List[str] #all elements in list are strings as well
      contact_details: Dict[str, str]

      @field_validator('email')
      @classmethod
      def email_vaidator(cls, value):

            valid_domains = [ 'hdfc.com', 'icici.com']

            domain_name = value.split('@')[-1] 

            if domain_name not in valid_domains:
                  raise ValueError('not in valid domain')
            
            return value
      
def update_patient_data(patient: Patient):
            print(patient.name)
            print(patient.age)
            print(patient.allergies)
            print(patient.married)
            print('updated')

            patient_info = {'name':'nitesh', 'email':'dgf@hdfc.com','age':'30', 'weight':75.3 ,'married':True , 'allergies':['pollen', 'dust'], 'contact_details': '545481245' }

            patient1 = Patient(**patient_info)

            update_patient_data(patient1)
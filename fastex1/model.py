from pydantic import BaseModel, field_validator,EmailStr,conlist,HttpUrl, \
    model_validator,Field,computed_field,AliasChoices
from typing import Dict,Optional,List,Any
from pydantic_settings import BaseSettings,SettingsConfigDict
import os
def area_vali(a:str):
    return a.upper()

def pin_check(b:int):
    if len(str(b)) != 5:
        raise ValueError("Enter length in 5 digits")
    return b

class Creature(BaseModel):
    name: str
    country: str
    area: str
    pin: int
    desc: str
    aka: str


    @field_validator("area")
    def _validate_area(cls, b):
        return area_vali(b)

    @field_validator('pin')
    def _validate_pin(cls, d):
        return pin_check(d)

    @field_validator('country')
    @classmethod
    def _validate_coun(cls,v:str)->str:
        return v.upper()



a=Creature(name="aa", country="asa", area="aW", pin=13182, desc="asa", aka="awq")

print(a.area)
print(a.model_json_schema())  #{'properties': {'name': {'title': 'Name', 'type': 'string'}, 'country': {'title': 'Country', 'type': 'string'}, 'area': {'title': 'Area', 'type': 'string'}, 'pin': {'title': 'Pin', 'type': 'integer'}, 'desc': {'title': 'Desc', 'type': 'string'}, 'aka': {'title': 'Aka', 'type': 'string'}}, 'required': ['name', 'country', 'area', 'pin', 'desc', 'aka'], 'title': 'Creature', 'type': 'object'}
print(a.model_dump()) #{'name': 'aa', 'country': 'asa', 'area': 'AW', 'pin': 13182, 'desc': 'asa', 'aka': 'awq'}

#example 2 (Nested onjects)

class Places(BaseModel):
    name: str
    spots: Optional[List[str]]=None

class Ident(BaseModel):
    country: str
    data: List[Places]   #Nested the Places model here, but its optional


#creating instances,

dump_data=Ident(country="India",
                data=[Places(name='kanniyakumari',spots=['falls','beach'])])
print(dump_data.model_dump())
dump_data1=Ident(country="India",
                data=[{"name":"Chennai","spots":['Beach','zoo']}])
print(dump_data1.model_dump())


## Email Str

class Emplyee(BaseModel):
    name: str
    email: EmailStr
    url: HttpUrl

class Org(BaseModel):
    name: str
    empl_details: List[Emplyee]

#instanting the object

emp_a=Org(name='xyzcorp',empl_details=[{'name':'warner','email':'check@yo.om','url':'https://www.xyz.com'}])
print(emp_a)


##Model Validator
class Details(BaseModel):
    name: str
    email: EmailStr

    @model_validator(mode='before')
    @classmethod
    def check_variables(cls,data: Any):
        if 'password' in data:
            raise ValueError(" shouls not include")
        return data
    @model_validator(mode='after')
    def check_var(self)-> 'Details':
        if " " not in self.name:
            raise "Please provide space"
        return self

d=Details(name='rered rer',email='asda@fr.com')
print(d)

##Field

class Store(BaseModel):
    name: str= Field(..., alias='storename')
    add: str

st=Store(storename='janson',add='123 downtown')
print(st)
print(st.model_dump(by_alias=True))
print(st.model_dump(by_alias=False))

#field constraints

class Name(BaseModel):
    name: str
    age: int=Field(..., gt=0)
    password: str = Field(..., min_length=6)

    @model_validator(mode='before')
    @classmethod
    def pass_vali(cls,data: Dict):
        special_chartrer=['@','#','$']
        if not any(char in special_chartrer for char in data.get('password')):
            raise ValueError('Missing special charater')
        return data


a=Name(name='john',age=32,password='ader@43Q')
print(a)

#compute field
from datetime import datetime
class Renas(BaseModel):
    name: str
    dob: int=2000

    @computed_field
    @property
    def age(self)->int:
        current_year=datetime.now().year
        cc=current_year-self.dob
        return cc

dd=Renas(name='derds',dob=1992)
print(dd.age)


##pydantic settings

#fetching value from varible
os.environ['PROD_NAME']='JIX'
os.environ['PROD_API_KEY']='adshajkdha'
os.environ['DEP_API_KEY']='adadenfn'
os.environ['ALTERNATE']="12312"

class Testset(BaseSettings):
    model_config =SettingsConfigDict(env_prefix='prod_')
    name: str
    api_key: str=Field(..., alias='API_KEY')
    alt: str=Field(..., validation_alias=AliasChoices('alternate','bente'))


test1=Testset(name='rame')
print(test1.model_dump())



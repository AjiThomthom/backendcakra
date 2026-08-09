from pydantic import BaseModel, Field
class AccountModel(BaseModel):
    username : str = Field(...,description="Wajib diisi!")
    password : str = Field(...,description="Wajib diisi!")


class ProfileModel(BaseModel):
    fullname : str = Field(None)
    role : str = Field(default="VISITOR")
    email : str = Field(...)
    number_phone : str = Field(...)
    
class UpdateProfileModel(BaseModel):
    role: str = Field(...)    
class RegisterProfile(ProfileModel,AccountModel):
    pass 
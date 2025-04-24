# -------------------------------------------------------- Pydantic ---------------------------------------------------------- #
x = 10 # Just a declaration of variable ( without type specification )

x = 'hello' # Reassigning the variable to a string or override variable


from pydantic import BaseModel # Pydantic is a data validation and settings management library for Python

class User(BaseModel): # BaseModel is a class from Pydantic that provides data validation and serialization
    name: str
    email: str
    account_id: int

user = User(
    name='Salah',
    email="salah@gmail.com",
    account_id=12345
) # Creating an instance of the User class with the provided data
'''
if the account_id is not an integer, it will convert it to integer automatically
if it is possible to convert it to an integer, otherwise it will raise a validation error.
'''

user_data = {
    'name': 'Salah',
    'email': "salah@gmail.com",
    'account_id': 12345
}

user = User(**user_data) # Unpacking the dictionary into the User class constructor

print(user.name)
print(user.email)
print(user.account_id)

from pydantic import EmailStr,field_validator # EmailStr is a Pydantic type that validates email addresses
# email address should be in this form : example@domain.com it make sure that the form is valid
# field_validator is used to make a custom validation for a field in the model

class User(BaseModel):
    name: str
    email: EmailStr # Using EmailStr to validate the email address
    account_id: int

    @field_validator("account_id")
    def check_account_id(cls, v): # Custom validation for account_id field
        if v < 0:
            raise ValueError("account_id must be a positive integer")
        return v
    

# user = User(name = 'Ali', email = 'ali', account_id = 1234) # This will raise a validation error because the email is not valid
# print(user)


# user = User(name = 'Ali', email = 'ali', account_id = -12) # This will raise a validation error because the account_id is not valid
# print(user) 


user_json_str = user.model_dump_json() # Convert the user object to a JSON string
print(user_json_str) # Print the JSON string

jsong_str = {"mane":"Ali","email":"ali@gmail.com","account_id":1234}
user = user.parse_raw(jsong_str) # Convert the JSON string back to a User object


'''
usually developers use the pydantic instead of dataclass because it is more powerful and flexible
and it is more easy to use and it is more readable and it is more maintainable
and it is more efficient and it is more secure and it is more scalable and it is more portable
'''
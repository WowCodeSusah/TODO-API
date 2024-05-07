from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randint

class User(BaseModel):
    name: str
    password: str
    role: str
    dateOfBirth: str 

class UpdateUser(BaseModel):
    name: str
    password: str
    role: str
    dateOfBirth: str 
    email: str

app = FastAPI()

baseUser = [{"name": "Michael Bengawan", "password": "12345678", "role": "admin", "dateOfBirth": "31/12/2003", "email": "michael.bengawan@moringa.com", "id": 1}]

# Create a new ID
def getNewID(baseUser):
    newNumber = randint(1, 10000)
    check = False
    for x in baseUser:
        if x['id'] == newNumber:
           check = True  
    if check == True:
        return getNewID(baseUser)
    else:
        return newNumber 
    
# Create a new Email
def getNewEmail(baseUser, username):
    formattedUsername = username.lower().replace(" ", ".")
    newEmail = formattedUsername + "@moringa.com"
    check = False
    for x in baseUser:
        if x['email'] == newEmail:
            check = True
    if check == True:
        extraDigit = randint(1, 10)
        formattedUsername = formattedUsername + extraDigit.__str__()
        return getNewEmail(baseUser, formattedUsername)
    else:
        return newEmail
    
# Search Users by ID
def searchID(baseUser, id):
    for x in baseUser:
        if x['id'] == id:
            return x
    return None

# Search Users Index
def searchIndex(baseUser, id):
    for x, y in enumerate(baseUser, 0):
        if y['id'] == id:
            return x
    return None

@app.get("/users")
def get_all_users():
    return {"all_user": baseUser}

@app.get("/users/{id}")
def get_user(id: int):
    if searchID(baseUser, id) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"user": searchID(baseUser, id)}

@app.post("/users", status_code=status.HTTP_201_CREATED)
def add_user(data: User):
    newUser = data.model_dump()
    newUser['email'] = getNewEmail(baseUser, data.name)
    newUser['id'] = getNewID(baseUser)

    baseUser.append(newUser)
    return {"User has been added" : data.name,
            "With Email": newUser['email'],
            "With ID": newUser['id']
            }

@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    if searchIndex(baseUser, id) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    baseUser.pop(searchIndex(baseUser, id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/users/{id}")
def update_user(id: int, user: UpdateUser):
    if searchIndex(baseUser, id) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    userData = user.model_dump()
    userData['id'] = id
    baseUser[searchIndex(baseUser, id)] = userData
    return {"Updated User" : userData}
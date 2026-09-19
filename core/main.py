from fastapi import FastAPI, Query, status, HTTPException, Path, Form, Body, File, UploadFile
from fastapi.responses import JSONResponse
import random
from typing import Optional, Annotated, List
from contextlib import asynccontextmanager
from dataclasses import dataclass
from schemas import PersonCreatSchemas, PersonReasponsSchemas


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("** stating app")
    yield
    print("shuntdon app **")

app = FastAPI(lifespan=lifespan)


names_list = [
    {"id":1, "name":"ali"},
    {"id":2, "name":"mohammad"},
    {"id":3, "name":"zahra"},
    {"id":4, "name":"amirhossein"},
    {"id":5, "name":"fateme"},
    {"id":6, "name":"mohammad"},
    {"id":7, "name":"mohammad"},
]



# return names
@app.get("/names", status_code = 200, response_model=PersonReasponsSchemas)
# def retreivs_name_list(q: str = None):
# def retreivs_name_list(q: str | None = None):
# def retreivs_name_list(q: Annotated[str | None, Query(max_length=50)] = None):
def retreivs_name_list(q: str | None = Query(alias="search",
                                            description="it will be searched with the title your provided!",
                                            example="ali",
                                            default=None,
                                            max_length=50)):
    if q:
        return [item for item in names_list if item["name"] == q]
    return names_list


# search name with id
@app.get("/names/{name_id}")
# def retreivs_name_with_id(name_id:int = Path(alias="Name_ID", title="object id", description="the id of the name in names_list")):
def retreivs_name_with_id(name_id:int):
    for name in names_list:
        if name["id"] == name_id:
            return name
    raise HTTPException(status_code=404, detail="Object not found!")



# # # create a new name  ---- Metod 1

# @app.post("/names", status_code= status.HTTP_201_CREATED)
# def creat_name(name: str = Body(embed=True)):
#     name_obj = {"id": random.randint(6,100), "name": name }
#     names_list.append(name_obj)
#     return name_obj
#     # raise HTTPException(status_code=404, detail="Object not found!")




# create a new name with dataclass  --- Metod 2
# @dataclass
# class Student:
#     name: str
#     age: int

# @dataclass
# class Student2:
#     id: int 
#     name: str
#     age : int

# @app.post("/names", status_code= status.HTTP_201_CREATED, response_model=Student2)
# def creat_name(student: Student):
#     name_obj = {"id": random.randint(6,100), "name": student.name}
#     names_list.append(name_obj)
#     return name_obj



# # # create a new name with pydantic model  --- Metod 3
@app.post("/names", status_code= status.HTTP_201_CREATED, response_model=PersonReasponsSchemas)
def creat_name(person: PersonCreatSchemas):
    name_obj = {"id": random.randint(6,100), "name": person.name}
    names_list.append(name_obj)
    return name_obj


# remove name with id
@app.delete("/names/{name_id}", status_code= status.HTTP_204_NO_CONTENT)
def del_name(name_id:int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            # return {"Detail": "object removed"}
            return JSONResponse(content={'message':'remove suscseefuly'}, status_code = status.HTTP_200_OK)
    # return {"detail":"not found"}
    raise HTTPException(status_code=404, detail="Object not found!")


# update name with id
@app.put("/names/", status_code= status.HTTP_202_ACCEPTED)
def update_name(name_id:int = Path(alias="new_name"), name = Form()):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = name
            return item 
    # return {"detail: ": "object not found!"}
    # return "not found"
    raise HTTPException(status_code=404, detail="Object not found!")


@app.get("/")
def root():
    # return {"messege" : "Hello World!!! "}
    return JSONResponse(content={'message':'Hello world!'}, status_code = status.HTTP_200_OK)



@app.post("/uploadfile1/")
def upload_file_1(file: bytes = File(...)):
    print(file)
    return {"file_size": len(file)}


# @app.post("/uploadfile2/")
# async def upload_file_2(file: UploadFile = File(...)):
#     content = await file.read()
#     print(file.__dict__)
#     return {"file_name": file.filename, "content_type": file.content_type, "file_size": len(content)}


@app.post("/upload-multiple/")
async def upload_multiple(files: List[UploadFile]= File(...)):
    return [{"file_name":file.filename, "content_type": file.content_type} for file in files
    ]

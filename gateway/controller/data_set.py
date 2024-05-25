from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from database.model.setup import get_db
from gateway.functions.authentication import get_active_user
from gateway.functions.s3 import upload_file_to_s3
from schema import user
from schema.data_set import DataSet, DataSetInternal, DataSetCreate, DataType
from database.interfaces.data import DataSetInterface
from database.sql.data_set import DataSetImplementation

data_router = APIRouter(prefix="/data-set", tags=["data_set"])


@data_router.post("/upload", response_model=DataSet)
def create_data_set(data_set: DataSetCreate, current_user: Annotated[user.User, Depends(get_active_user)],
                    db: Session = Depends(get_db)):
    # remove file parameter from above since no file is actually being uploaded
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not Authenticated")

    # upload the file to amazon s3 using boto3

    # setting the path to a random string just to show how it works
    # normally, path would be returned from an upload to s3 function

    # also setting the type to default since no file is being uploaded.
    # Would normally check to detect the file type
    path = upload_file_to_s3()
    d_internal = DataSetInternal(
        name=data_set.name,
        created_by=current_user,
        path=path,
        type=DataType.Default
    )

    r: DataSetInterface = DataSetImplementation()
    data = r.create_dataset(db, d_internal, current_user.id)
    if data is None:
        raise HTTPException(status_code=500, detail="Dataset could not be created")

    return data


@data_router.get("/{uid}", response_model=DataSet)
def get_data_set(uid: int, db: Session = Depends(get_db)):
    r: DataSetInterface = DataSetImplementation()
    data_set = r.fetch_dataset_by_id(db, uid)
    if data_set is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return data_set


@data_router.patch("/{did}", response_model=DataSet)
def update_data_set(did: int, data_set: DataSetCreate, current_user: Annotated[user.User, Depends(get_active_user)],
                    db: Session = Depends(get_db)):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not Authenticated")

    r: DataSetInterface = DataSetImplementation()
    data = r.fetch_dataset_by_id(db, did)
    if data is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    if data.created_by.id != current_user.id:
        raise HTTPException(status_code=401, detail="Not Authorized")

    path = upload_file_to_s3()
    d_internal = DataSetInternal(
        name=data_set.name,
        type=DataType.Default.name,
        path=path,
    )

    resp_data = r.update_dataset(db, d_internal, did)
    if resp_data is None:
        raise HTTPException(status_code=500, detail="Dataset could not be updated")

    return resp_data


@data_router.delete("/{uid}")
def delete_data_set(uid: int, current_user: Annotated[user.User, Depends(get_active_user)],
                    db: Session = Depends(get_db)):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not Authenticated")

    r: DataSetInterface = DataSetImplementation()
    data_set = r.fetch_dataset_by_id(db, uid)
    if data_set is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    if data_set.created_by.id != current_user.id:
        raise HTTPException(status_code=401, detail="Not Authorized")

    status = r.delete_dataset(db, uid)
    if not status:
        raise HTTPException(status_code=500, detail="Dataset could not be deleted")

    return

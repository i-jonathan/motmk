from fastapi import APIRouter
from gateway.controller.authentication import auth_router
from gateway.controller.groups import group_router
from gateway.controller.data_set import data_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(group_router)
router.include_router(data_router)

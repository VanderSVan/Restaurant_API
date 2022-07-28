from datetime import time, date

from fastapi import Depends, Query, Path, status
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from ..schemes.schedule.base_schemes import (ScheduleGetSchema,
                                             SchedulePatchSchema,
                                             SchedulePostSchema)
from ..schemes.schedule.response_schemes import (ScheduleResponsePatchSchema,
                                                 ScheduleResponseDeleteSchema,
                                                 ScheduleResponsePostSchema)

from ..crud_operations.schedule import ScheduleOperation
from ..utils.dependencies import get_db
from ..utils.responses.main import get_text

# Unfortunately attribute 'prefix' in InferringRouter does not work correctly (duplicate prefix).
# So I have a prefix in each function.
router = InferringRouter(tags=['schedule'])


@cbv(router)
class Schedule:
    db: Session = Depends(get_db)

    def __init__(self):
        self.schedule_operation = ScheduleOperation(db=self.db)

    @router.get("/schedules/", response_model=list[ScheduleGetSchema], status_code=status.HTTP_200_OK)
    def get_all_schedules(self, day: str | date = Query(default=None,
                                                        description="Weekday or date"),
                          open_time: time = Query(default=None,
                                                  description="HH:MM"),
                          close_time: time = Query(default=None,
                                                   description="HH:MM"),
                          break_start_time: time = Query(default=None,
                                                         description="HH:MM"),
                          break_end_time: time = Query(default=None,
                                                       description="HH:MM")):
        return self.schedule_operation.find_all_by_params(day=day,
                                                          open_time=open_time,
                                                          close_time=close_time,
                                                          break_start_time=break_start_time,
                                                          break_end_time=break_end_time
                                                          )

    @router.get("/schedules/{schedule_id}", response_model=ScheduleGetSchema, status_code=status.HTTP_200_OK)
    def get_schedule(self, schedule_id: int = Path(..., ge=1)):
        return self.schedule_operation.find_by_id_or_404(schedule_id)

    @router.patch("/schedules/{schedule_id}", response_model=ScheduleResponsePatchSchema,
                  status_code=status.HTTP_200_OK)
    def patch_schedule(self, schedule: SchedulePatchSchema, schedule_id: int = Path(..., ge=1)):
        self.schedule_operation.update_model(schedule_id, schedule)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": get_text('patch').format(
                                self.schedule_operation.response_elem_name, schedule_id
                            )})

    @router.delete("/schedules/{schedule_id}", response_model=ScheduleResponseDeleteSchema,
                   status_code=status.HTTP_200_OK)
    def delete_schedule(self, schedule_id: int):
        self.schedule_operation.delete_model(schedule_id)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": get_text('delete').format(
                                self.schedule_operation.response_elem_name, schedule_id
                            )})

    @router.post("/schedules/create", response_model=ScheduleResponsePostSchema, status_code=status.HTTP_201_CREATED)
    def add_schedule(self, schedule: SchedulePostSchema):
        schedule = self.schedule_operation.add_model(schedule)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"message": get_text('post').format(
                                self.schedule_operation.response_elem_name, schedule.id
                            )})

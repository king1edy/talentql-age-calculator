from typing import Union
from datetime import date, datetime

import uvicorn
from fastapi import FastAPI, HTTPException

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address, default_limits=["3/minute"])
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/howold")
# @limiter.limit("3/minute")
async def cal_dob(dob):
    if dob is not datetime.strptime(dob, "%Y-%m-%d").strftime('%Y-%m-%d'):
        raise HTTPException(
            status_code=400,
            detail="Not a valid timestamp",
            headers={"X-Error": "Requires a valid timestamp but {dobType} was provided".format(dobType=type(dob))}
        )
    return CalculateDob(dob)


def CalculateDob(dateofbirth):
    today = date.today()
    print(dateofbirth)
    age = today. year - dateofbirth.year - ((today.month, today.day) < (dateofbirth.month, dateofbirth.day))
    print(age)
    return age


if __name__ == "__main__":
    uvicorn.run("main:app", debug=True, reload=True)
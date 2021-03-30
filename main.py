from fastapi import FastAPI, Form, Request 
from deta import Deta

from fastapi.responses import RedirectResponse
import starlette.status as status

from datetime import datetime, date

today = date.today()
now = datetime.now()

current_date = today.strftime("%d/%m/%Y")
current_time = now.strftime("%H:%M:%S")

deta = Deta() # DetaBase instance
db = deta.Base("akane-contact") # Name of the data base

app = FastAPI() # FastAPI instance

@app.get('/')
async def index():
    return {'message':'ok'}

@app.post('/form')
async def email(
    request: Request,
    name: str = Form(...), 
    email: str = Form(...), 
    message: str = Form(...)):
    try:
        insert = db.insert({
                'nombre':name, 
                'email':email, 
                'mensaje':message,
                'fecha':current_date,
                'hora':current_time
                })
    except:
        return {'message':'something went wrong'}
    return RedirectResponse(url='https://akane.ga', status_code=status.HTTP_302_FOUND)
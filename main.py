from fastapi import FastAPI, Form, Request 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import starlette.status as status
from deta import Deta
from datetime import datetime, date
from mail.mail import sender
from uuid import uuid4
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

deta = Deta() # DetaBase instance
db = deta.Base("akane-contact") # Name of the data base

app = FastAPI() # FastAPI instance

# Rate limit instance
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get('/')
async def index(request: Request):
    return {'message':'ok'}

@app.post('/form')
@limiter.limit("5/minute") # Decorator for the rate limit time / 5 request per minute
async def email(
    request: Request,
    name: str = Form(...), 
    email: str = Form(...), 
    message: str = Form(...)):
    today = date.today()
    now = datetime.now()
    current_date = today.strftime("%d/%m/%Y")
    current_time = now.strftime("%H:%M:%S")
    key = str(uuid4())
    try:
        if db.get(key) == None:
            insert = db.insert({
                'key':key,
                'nombre':name, 
                'email':email, 
                'mensaje':message,
                'fecha':current_date,
                'hora':current_time
                })
            send = sender()

    except:
        return {'message':'something went wrong'}
    # Redirect to akane.ga in this casebut can be redirected to any website
    return RedirectResponse(url='http://akane.ga', status_code=status.HTTP_302_FOUND)
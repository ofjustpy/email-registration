# ======================= first set the logging ======================
import logging
import os

if os:
    try:
        os.remove("launcher.log")
    except:
        pass

import sys
if sys:
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename="launcher.log",
                        level=logging.DEBUG, format=FORMAT)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    

# ================================ end ===============================

import ofjustpy as oj
from email_registration.views import  register_new_user, wp_user_login
from addict import Dict
import sqlalchemy  as sa
import models
from py_tailwind_utils import *

from csrf_middleware import CSRFMiddleware
from starlette.middleware import Middleware
#from asgi_signing_middleware import SerializedSignedCookieMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser, requires
)
import binascii
import base64


engine = sa.create_engine("sqlite+pysqlite:///:memory:", echo=True)
models.Base.metadata.create_all(engine)
models.Base.metadata.create_all(engine)

SECRET_KEY="Pls use a good professional secret key"
csrf_cookie_name = "csrftoken"
csrf_secret='shhshh2'

# csrf token is necessary

csrf_middleware = Middleware(CSRFMiddleware,
                                secret=csrf_secret,
                                field_name = csrf_cookie_name)

# we also need SignedCookie Middleware
from asgi_signing_middleware import SerializedSignedCookieMiddleware

signed_cookie_middleware = Middleware(SerializedSignedCookieMiddleware,
                               secret=b'a very, very secret thing',  
                               state_attribute_name='messages',  
                               cookie_name='my_cookie',
                               cookie_ttl=60 * 5,  
                               )

class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        logger.debug("Auth Middleware:BEGIN")

        if "Authorization" not in conn.headers:
            logger.debug("No authorization header in conn.headers")
            logger.debug("Auth Middleware:END")
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            logger.debug("recieved authentication credentials..eventually verify it")
            logger.debug(f"scheme={scheme} credentials={credentials}")
            if scheme.lower() != 'basic':
                logger.debug("auth scheme not basic: no authorization begin done")
                return
            decoded = base64.b64decode(credentials).decode("ascii")
            logger.debug(f"decoded = {decoded}")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            logger.debug("authentication ran into exception")
            raise AuthenticationError('Invalid basic auth credentials')
        logger.debug("authentication done: user is verified")
        return AuthCredentials(["authenticated"]), SimpleUser("user")

    
auth_middleware =     Middleware(AuthenticationMiddleware,
                                 backend=BasicAuthBackend(),
                                 on_error=lambda _, exc: PlainTextResponse("error during authentication", status_code=401)
                                 )


#app = oj.build_app()
engine = sa.create_engine("sqlite+pysqlite:///:memory:", echo=True)
models.Base.metadata.create_all(engine)
app = oj.build_app([auth_middleware,
                    signed_cookie_middleware,
                    csrf_middleware
                    ])

# request = Dict()
# request.session_id = "abc"
# wp = wp_user_login(request)
# _sm = wp.session_manager
# _ss = _sm.stubStore
# _ss.inputbox_email.target.value = "spoofemail@monallabs.in"
# _ss.inputbox_password.target.value = "mypass1"

# msg = Dict()
# msg.page = wp
# _ss.myform.target.on_submit(msg)
# sys.exit()

# #app.add_jproute("/register_new_user", register_new_user)
app.add_jproute("/user_login", wp_user_login)



# import asyncio
# from jpcore.justpy_app import uvicorn_server_control_center

# import rpyc
# server_port = 8934
# try:
#     conn = rpyc.connect("localhost", server_port)
# except Exception as e:
#     sys.exit()
#     print("Could not connect ")



# # Start uvicorn server
# async def main():
#     # basically call 
#     # await an_async_func
    
#     # start webserver
#     webserver_controller = uvicorn_server_control_center("localhost", 8000, app)
#     await webserver_controller.start()
#     await asyncio.sleep(1)


#     # from browser connect to the webserver and get content
#     page_source = conn.root.load_page("http://127.0.0.1:8000/user_login", "user_login")
#     #print (page_source)
#     res = conn.root.set_value_element("/inputbox_email", "spoofemail@monallabs.in")
#     print ("res = ", res)
        
#     res = conn.root.set_value_element("/inputbox_password", "sxsdsdfs")
#     print ("res = ", res)
    
#     res = conn.root.submit_element("/myform")
#     print ("res = ", res)

    
#     value = input("Press key to stop uvicorn server:\n")

#     # close webserver
#     await webserver_controller.stop()

#     await asyncio.sleep(10)
    
        
    

# asyncio.run(main())
# # start browser



# # load page via browser





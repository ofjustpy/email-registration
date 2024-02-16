"""
drop down color not working in firefox
"""

from tailwind_tags import *
import ofjustpy as oj
from addict import Dict
import justpy as jp
import traceback
#from wtforms.validators	import DataRequired
from starlette.middleware import Middleware
from asgi_signing_middleware import SerializedSignedCookieMiddleware

app = jp.build_app([Middleware(SerializedSignedCookieMiddleware,
                               secret=b'a very, very secret thing',  
                               state_attribute_name='messages',  
                               cookie_name='my_cookie',
                               cookie_ttl=60 * 5,  
                               )
                    ])

def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    # this is necessary
    # a bug in justpy for input change
    def on_input_change(dbref, msg):
        #traceback.print_stack(file=sys.stdout)
        print (msg)
        pass

    def on_submit_click(dbref, msg):
        #print (msg)

                    #stop_validation = self._run_validation_chain(data, chain)
        # print(dbref.spathMap)
        # for cpath, cbref in dbref.spathMap.items():
        print ("form on_submit called")
        #     print (cpath, cbref)
        pass


            
        
    with oj.sessionctx(session_manager):
        def on_click(dbref, msg):
            print (" obtn clicked")
        obtn_ = oj.Button_("obtn",
                           text="oSubmit",
                           type="submit").event_handle(oj.click, on_click)
        btn_ = oj.Button_("mybtn", text="Submit", type="submit")

        username_input_ = oj.LabeledInput_("username",
                                           "Username",
                                           "username",
                                           
                                           data_validators = [oj.validator.InputRequired()]).event_handle(oj.change,
                                                                                       on_input_change
                                                                                       )

        email_input_ = oj.LabeledInput_("email",
                                           "Email",
                                           "Email",
                                           
                                           data_validators = [oj.validator.Email()]).event_handle(oj.change,
                                                                                       on_input_change
                                                                                       )

        password_ = oj.LabeledInput_("password",
                                     "password",
                                     "Enter Password",
                                     data_validators=[oj.validator.InputRequired()]
                                     ).event_handle(oj.change, on_input_change)
        
        confirm_password_ = oj.LabeledInput_("confirm_password",
                                     "confirm_password",
                                     "Confirm Password",
                                     data_validators=[oj.validator.InputRequired(),
                                                      oj.validator.EqualTo(password_.spath)]
                                     ).event_handle(oj.change, on_input_change)
        
        
        all_inputs_ = oj.StackV_("all_inputs",
                                 cgens = [username_input_,
                                          email_input_,
                                          password_,
                                          confirm_password_]
                                 )
        target_ = oj.Form_("myform", all_inputs_
                           ,btn_, stubStore = session_manager.stubStore
                ).event_handle(oj.submit, on_submit_click)
        # target_ = oj.Halign_(oj.LabeledInput_(
        #                          "labeldinput",
        #                          "Input a value", "30").event_handle(oj.change,
        #                                                              on_input_change
        #                                                              )
        #                      )
        wp_ = oj.WebPage_("oa",
                          cgens =[target_, obtn_],
                          template_file='svelte.html',
                          title="myoa"
                          )
        wp = wp_()
        wp.session_manager = session_manager
        request.state.messages.csrftoken  = "mysecrettoken"
        #wp.cookies["csrftoken"] =  "mysecrettoken2"
    return wp

app.add_jproute("/", launcher, name="root")

#jp.justpy(launcher, start_server=False)


# from starlette.testclient import TestClient
# # client = TestClient(app)
# # response = client.get('/')
# request = Dict()
# request.session_id = "abc"
# wp = launcher(request)
# _sm = wp.session_manager
# _ss = _sm.stubStore
# #print(_ss.labeldinput_input)
# _ss.username_input.target.value = "dssdf"
# _ss.email_input.target.value = "spoofemail@monallabsy.in"
# _ss.password_input.target.value = "mypass1"
# _ss.confirm_password_input.target.value = "mypass1"
# #print(_ss.keys())
# msg = None
# _ss.myform.target.on_submit(msg)

# #wp = launcher.log

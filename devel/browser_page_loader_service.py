
from Browser import Browser
from datetime import date
import sys
import os

import rpyc

# os.mkdir(date_str)


url = "http://nytimes.com"

class PageServer(rpyc.Service):
    def __init__(self, browser):
        self.browser  = browser

    def on__connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        print("client connected")
        pass

    def on_disconnect(self, conn):
        print("client disconnected")
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_load_page(self, url, label):
        print ("called load_page with url = ", url, " ", type(url))
        ph = self.browser.get_page(url, 1, label="test_page")
        page_loaded = ph.__next__()
        page_source = ph.__next__()
        try:
            ph.__next__() #write page_source to file
        except:
            pass
        return page_source

    # def exposed_click_button(def, button_id):
    #     pass

    def exposed_set_value_element(self, element_id, value):
        print ("called set-value = ", element_id, " ", value)
        return self.browser.set_value_element(element_id, value)

    def exposed_submit_element(self, element_id):
        return self.browser.submit_element(element_id)
    

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    with Browser() as _b:
        server_handle = ThreadedServer(PageServer(_b), port=int(sys.argv[1]))
        server_handle.start()
        print("Shutting down proxy server")
    

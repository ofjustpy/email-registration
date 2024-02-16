import rpyc


server_port = 8934
try:
    conn = rpyc.connect("localhost", server_port)
except Exception as e:
    print("Could not connect ")
    
page_source = conn.root.load_page("https://nytimes.com", "nytimes")
print (page_source)


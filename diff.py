import diff_match_patch as dnp

class Client:
    def __init__(self, client_text):
        self.client_text = client_text 
        self.client_shadow = client_text 
        
        self.diff_match = dnp.diff_match_patch()

    def synchronization_step():
        

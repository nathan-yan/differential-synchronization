import diff_match_patch as dnp

"""
class Client:
    def __init__(self, client_text, other = None):
        self.client_text = client_text 
        self.client_shadow = client_text 
        
        self.patcher = dnp.diff_match_patch()

        self.other = other
    
    def set_other(self, other):
        self.other = other

    def synchronization_step(self):
        if self.client_text != self.client_shadow:      # there's nothing to do if there's no change
            patches = self.patcher.patch_make(self.client_shadow, self.client_text)

            # copy the client_text to client_shadow
            self.client_shadow = self.client_text

            # apply the patches to other.client_shadow and other.client_text
            self.other.client_shadow = self.other.patcher.patch_apply(patches, self.other.client_shadow)[0]
            self.other.client_text = self.other.patcher.patch_apply(patches, self.other.client_text)[0]

    def status(self):
        if self.client_text == self.other.client_shadow and self.client_shadow == self.other.client_text:
            return "Synchronized"
        
        return "Desynchronized"

    def __str__(self):
        return "Text: " + self.client_text + "\n" + "Shadow: " + self.client_shadow 


##### CASE WITH TWO DECENTRALIZED USERS #####
shared_text = "hello world, my name is alice!"
    
bob = Client(shared_text)
alice = Client(shared_text)

bob.set_other(alice)
alice.set_other(bob)

bob.client_text = "hello, world, my name is bob, totally!"

bob.synchronization_step()

print('t = 0')
print(str(bob))
print(" ")
print(str(alice))
print(bob.status())
print("\n\n")

alice.client_text = "hello world, actually, my name is alice..."

alice.synchronization_step()

print('t = 1')
print(str(bob))
print(" ")
print(str(alice))
print(bob.status())
print("\n\n")

alice.client_text = "hello world, actually my name is alice rogers"

alice.synchronization_step()

print('t = 2')
print(str(bob))
print(" ")
print(str(alice))
print(bob.status())
print("\n\n")
##########
"""

class Server:
    def __init__(self, server_text, connections = []):
        self.server_text = server_text
        self.server_shadows = {}

        self.connections = {}

        for i in connections:
            self.add_connection(i)

        self.patcher = dnp.diff_match_patch()

    def add_connection(self, other):
        id_ = other.id_ 

        self.connections[id_] = other
        self.server_shadows[id_] = self.server_text

        other.idx = len(self.server_shadows) - 1

    def status(self):
        states = []

        for c in self.connections:
            if self.connections[c].client_text == self.server_shadows[c] and self.connections[c].client_shadow == self.server_text:
                states.append("Synchronized")
            else:
                states.append("Desynchronized")
        
        return states

    def synchronization_step(self):
        for c in self.connections:
            # treat each connection individually

            if self.server_text != self.server_shadows[c]:
                patches = self.patcher.patch_make(self.server_shadows[c], self.server_text)

                self.server_shadows[c] = self.server_text

                # apply the patches
                self.connections[c].client_shadow = self.connections[c].patcher.patch_apply(patches,self.connections[c].client_shadow)[0]
                
                self.connections[c].client_text = self.connections[c].patcher.patch_apply(patches, self.connections[c].client_text)[0]


class Client:
    def __init__(self, client_text, name, other = None):
        self.client_text = client_text 
        self.client_shadow = client_text 
        
        self.patcher = dnp.diff_match_patch()

        self.other = other
        self.id_ = name 

    def set_other(self, other):
        self.other = other

    def synchronization_step(self):
        if self.client_text != self.client_shadow:      # there's nothing to do if there's no change
            patches = self.patcher.patch_make(self.client_shadow, self.client_text)

            # copy the client_text to client_shadow
            self.client_shadow = self.client_text

            # apply the patches to other.server_shadow and other.server_text
            self.other.server_shadows[self.id_] = self.other.patcher.patch_apply(patches, self.other.server_shadows[self.id_])[0]
            self.other.server_text = self.other.patcher.patch_apply(patches, self.other.server_text)[0]

    def status(self):
        if self.client_text == self.other.server_shadow and self.client_shadow == self.other.server_text:
            return "Synchronized"
        
        return "Desynchronized"

    def __str__(self):
        return "Text: " + self.client_text + "\n" + "Shadow: " + self.client_shadow 

##### CASE WITH A CENTRAL SERVER #####
shared_text = "hello world, my name is alice!"

bob = Client(shared_text, 'bob')
alice = Client(shared_text, 'alice')
eve = Client(shared_text, 'eve')

oracle = Server(shared_text, [bob, alice, eve])
bob.set_other(oracle)
alice.set_other(oracle)
eve.set_other(oracle)

import time 

bob.client_text = "hello world, m yname is yes"

s = time.time()

for i in range (2):
    
    bob.synchronization_step()
    if i == 0:
        eve.client_text = """hello world, m yname is eve
        def function(self, new):
            print('this is anew piece of code')"""

    alice.synchronization_step()
    eve.synchronization_step()

    oracle.synchronization_step()

    print("t = " + str(i))
    print(str(bob))
    print(str(alice))
    print(oracle.status())
    print(" ")

    if i == 0:
        alice.client_text = """
        import math
        class test():
            self.test = test 

        def function(self, new):
            print('this is a new piece of code')"""

print(time.time() - s)
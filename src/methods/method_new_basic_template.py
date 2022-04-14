from methods.MethodTemplate import MethodTemplate
# You must import the MethodTemplate abstract class.

"""
|
|
| Import here all the modules you need.
| Remark: Make sure that neither of those modules starts with "method_".
|
|
"""

""" 
|
|
| Put here all the functions that your method uses.
| Remark: Make sure that this file starts with "method_".
|
| def a_function_of_my_method(signal,params):
|   ...
|
|
"""

""" Create here a new class that will encapsulate your method.
This class should inherit the abstract class MethodTemplate.
By doing this, you must then implement the class method: 

def method(self, signal, params)

which should receive the signals and any parameters
that you desire to pass to your method.You can use this file as an example.
"""

class NewMethod(MethodTemplate):
    def __init__(self):
        self.id = 'a_new_method'
        self.task = 'denoising'  # Should be either 'denoising' or 'detection'

    def method(self, signals, params = None): # Implement this method.
        ...

    # def get_parameters(self):            # Use it to parametrize your method.
    #     return [None,]
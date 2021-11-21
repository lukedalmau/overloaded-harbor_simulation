import random_vars as rv

def ship_arrival():
    return rv.exponential_random_variable(1.0/8)

def ship_type():
    return rv.U(0,1)
    
def Small_Load_Time():
    return rv.normal_random_variable(9,1)

def Medium_Load_Time():
    return rv.normal_random_variable(12,2)

def Large_Load_Time():
    return rv.normal_random_variable(18,3)

def tow_to_port():
    return rv.exponential_random_variable(1.0/1)

def tow_to_dock():
    return rv.exponential_random_variable(1.0/2)

def free_tug_movement():
    return rv.exponential_random_variable(1.0/(1/4.0)) 
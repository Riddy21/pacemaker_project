import tkinter as tk

# NOTE: maybe change into an object in the future?

def validate_lrl(lrl):
    try:
        lrl = int(lrl)
    except ValueError:
        return False, "Error: Lower rate limit input must be an integer"

    if  30 <= lrl <= 50 :
        if (lrl % 5) == 0 :
            return True, ''
        else:
            return False, "Error: Lower rate limit must have 5ppm increments between 30 and 50 ppm"
    elif 50 <= lrl <= 90 :
        if (lrl % 1) == 0 :
            return True, ''
        else:
            return False, "Error: Lower rate limit must have 1ppm increments between 50 and 90 ppm"
    elif 90 <= lrl <= 175 :
        if (lrl % 5) == 0 :
            return True, ''
        else:
            return False, "Error: Lower rate limit must have 5ppm increments between 90 and 175 ppm"
    else:
        return False, "Error: Lower rate limit must be between 30 - 175 ppm"


def validate_url(url):
    try:
        url = int(url)
    except ValueError:
        return False, "Error: Upper rate limit must be an integer"

    if 50 <= url <= 175 :
        if (url % 5) == 0 :
            return True, ''
        else:
            return False, "Error: Upper rate limit must have 5ppm increments"
    else:
        return False, "Error: Upper rate limit must be between 50 and 175 ppm"


def validate_regulated_atrial_amp(aa):
    #Multiplies by 10 and converts to int (Consider other methods)
    # NOTE: you can use formatting as such:
    # >>> '%s' % float('%.1g' % 1234)
    # '1000'
    try:
        aa = float(aa)
        aa_int = int(aa*10)
    except ValueError:
        return False, "Error: Atrial amplitude input must be float"
    
    if (aa_int == 0):
        return True, ''
    elif 5 <= aa_int <= 32 :
        if (aa_int % 1) == 0 :
            return True, ''
        else:
            return False, "Error: Atrial amplitude must have 0.1V increments between 0.5 and 3.2 V"
    elif 35 <= aa_int <= 70 :
        if (aa_int % 5) == 0:
            return True, ''
        else: 
            return False, "Error: Atrial amplitude must have 0.5V increments between 3.5 and 7 V"
    else:
        return False, "Error: Atrial amplitude must be in ranges: 0, 0.5-3.2, 3.5-7 V"

def validate_atrial_pw(apw):
    #Multiplies by 100 and converts to int
    try:
        apw = float(apw)
        apw_int = int(apw*100)
    except ValueError:
        return False, "Error: Atrial pulse width input must be float"
    
    if (apw_int == 5):
        return True, ''
    elif 10 <= apw_int <= 190 :
        if (apw_int % 10) == 0 :
            return True, ''
        else: 
            return False, "Error: Atrial pulse width must have 0.1ms increments"
    else:
        return False, "Error: Atrial pulse width be in ranges: 0.05, 0.1-1.9 ms"


def validate_regulated_ventricular_amp(va):
    #Multiplies by 10 and converts to int (Consider other methods)
    try:
        va = float(va)
        va_int = int(va*10)
    except ValueError:
        return False, "Error: Ventricular amplitude input must be a float"

    if (va_int == 0):
        return True, ''
    elif 5 <= va_int <= 32 :
        if (va_int % 1) == 0 :
            return True, ''
        else:
            return False, "Error: Ventricular amplitude must have 0.1V increments between 0.5 and 3.2 V"
    elif 35 <= va_int <= 70 :
        if (va_int % 5) == 0:
            return True, ''
        else: 
            return False, "Error: Ventricular amplitude must have 0.5V increments between 3.5 and 7 V"
    else:
        return False, "Error: Ventricular amplitude must be in ranges : 0, 0.5-3.2, 3.5-7 V"

def validate_ventricular_pw(vpw):
    #Multiplies by 100 and converts to int
    try:
        vpw = float(vpw)
        vpw_int = int(vpw*100)
    except ValueError:
        return False, "Error: Ventricular pulse width nput must be a float"

    if (vpw_int == 5):
        return True, ''
    elif 10 <= vpw_int <= 190 :
        if (vpw_int % 10) == 0 :
            return True, ''
        else: 
            return False, "Error: Ventricular pulse width must have 0.1ms increments"
    else:
        return False, "Error: Ventricular pulse width must be in ranges: 0.05, 0.1-1.9 ms"

def validate_vrp(vrp):
    try:
        vrp = int(vrp)
    except ValueError:
        return False, "Error: VRP input must be an integer"

    if 150 <= vrp <= 500 :
        if (vrp % 10 ) == 0 :
            return True, ''
        else:
            return False, "Error: VRP must have 10 ms increments"
    else:
        return False, "Error: VRP must be between 150 and 500 ms"


def validate_arp(arp):
    try:
        arp = int(arp)
    except ValueError:
        return False, "Error: ARP input must be integer"
    
    if 150 <= arp <= 500 :
        if (arp % 10 ) == 0 :
            return True, ''
        else:
            return False, "Error: ARP must have 10 ms increments"
    else:
        return False, "Error: ARP must be between 150 and 500 ms"

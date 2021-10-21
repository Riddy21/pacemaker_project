import tkinter as tk

# NOTE: maybe change into an object in the future?

def validate_lrl(lrl):
    lrl = int(lrl)
    if  30 <= lrl <= 50 :
        if (lrl % 5) == 0 :
            return True, ''
        else:
            return False, "Error: Must have 5ppm increments between 30 and 50 ppm"
    elif 50 <= lrl <= 90 :
        if (lrl % 1) == 0 :
            return True, ''
        else:
            return False, "Error: Must have 1ppm increments between 50 and 90 ppm"
    elif 90 <= lrl <= 175 :
        if (lrl % 5) == 0 :
            return True, ''
        else:
            return False, "Error: Must have 5ppm increments between 90 and 175 ppm"
    else:
        return False, "Error: Must be between 30 - 175 ppm"


def validate_url(url):
    url = int(url)
    if 50 <= url <= 175 :
        if (url % 5) == 0 :
            return True, ''
        else:
            return False, "Error: Must have 5ppm increments"
    else:
        return False, "Error: Must be between 50 and 175 ppm"


def validate_regulated_atrial_amp(aa):
    #Multiplies by 10 and converts to int (Consider other methods)
    aa_int = int(aa*10)

    if (aa_int == 0):
        return True, ''
    elif 5 <= aa_int <= 32 :
        if (aa_int % 1) == 0 :
            return True, ''
        else:
            return False, "Error: Must have 0.1V increments between 0.5 and 3.2 V"
    elif 35 <= aa_int <= 70 :
        if (aa_int % 5) == 0:
            return True, ''
        else: 
            return False, "Error: Must have 0.5V increments between 3.5 and 7 V"
    else:
        return False, "Error: Must be in ranges: 0, 0.5-3.2, 3.5-7 V"

def validate_atrial_pw(apw):
    #Multiplies by 100 and converts to int
    apw_int = int(apw*100)

    if (apw_int == 5):
        return True, ''
    elif 10 <= apw_int <= 190 :
        if (apw_int % 10) == 0 :
            return True, ''
        else: 
            return False, "Error: Must have 0.1ms increments"
    else:
        return False, "Error: Must be in ranges: 0.05, 0.1-1.9 ms"


def validate_regulated_ventricular_amp(va):
    #Multiplies by 10 and converts to int (Consider other methods)
    va_int = int(va*10)

    if (va_int == 0):
        return True, ''
    elif 5 <= va_int <= 32 :
        if (va_int % 1) == 0 :
            return True, ''
        else:
            return False, "Error: Must have 0.1V increments between 0.5 and 3.2 V"
    elif 35 <= va_int <= 70 :
        if (va_int % 5) == 0:
            return True, ''
        else: 
            return False, "Error: Must have 0.5V increments between 3.5 and 7 V"
    else:
        return False, "Error: Must be in ranges : 0, 0.5-3.2, 3.5-7 V"

def validate_ventricular_pw(vpw):
    #Multiplies by 100 and converts to int
    vpw_int = int(vpw*100)

    if (vpw_int == 5):
        return True, ''
    elif 10 <= vpw_int <= 190 :
        if (vpw_int % 10) == 0 :
            return True, ''
        else: 
            return False, "Error: Must have 0.1ms increments"
    else:
        return False, "Error: Must be in ranges: 0.05, 0.1-1.9 ms"

def validate_vrp(vrp):
    vrp = int(vrp)
    if 150 <= vrp <= 500 :
        if (vrp % 10 ) == 0 :
            return True, ''
        else:
            return False, "Error: must have 10 ms increments"
    else:
        return False, "Error: Must be between 150 and 500 ms"


def validate_arp(arp):
    arp = int(arp)
    if 150 <= arp <= 500 :
        if (arp % 10 ) == 0 :
            return True, ''
        else:
            return False, "Error: must have 10 ms increments"
    else:
        return False, "Error: Must be between 150 and 500 ms"

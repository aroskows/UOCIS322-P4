"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  A date object (arrow)
    Returns:
       A date object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    dist = control_dist_km
    #print("OPEN")
    if dist > brevet_dist_km:
        if dist < ((brevet_dist_km * 0.2) + brevet_dist_km):
            dist = brevet_dist_km
        else:
            #break its too big
            return -1
    
    #print(brevet_start_time)
    data = {200: 34, 400: 32, 600: 30, 1000: 28, 1300: 26}
    prev_keys = []
    for key in data:
        if  dist <= key:
            h, m = helper(dist, brevet_dist_km, data)
            #print("h =", h)
            #print("m =", m)
            break
            prev_keys.appened(key)

    rslt =  brevet_start_time.shift(hours = h, minutes = m)
    #print(rslt)
    return rslt
#open_time(60, 600, arrow.now())

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  A date object (arrow)
    Returns:
       A date object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    data = {60: 20, 200: 15, 400: 15, 600: 15, 1000: 11.428, 1300: 13.333}
    dist = control_dist_km
    if dist > brevet_dist_km:
        if dist <= ((brevet_dist_km * 0.2) + brevet_dist_km):
            dist = brevet_dist_km
        else:
           # print("too big")
            #break its too big
            return -1

    if dist == brevet_dist_km:
        #print("EQUAL")
        if dist == 200:
            h = 13
            m = 30
        elif dist == 400:
            h = 27
            m = 0
        elif dist == 1000:
            h = 75
            m = 0
        elif dist == 600:
            h = 40
            m = 0

    else:
        prev_keys= []
        for key in data:
            if dist  <= key:
                if dist > 200:
                    h, m = 0, 0
                    brev = brevet_dist_km
                    for i in reversed(prev_keys):
                        #tried to do this but it doesn't work sooo :(
                        #this is the weird if its bigger than we have to do the math for 
                        # the smaller ones
                        #print(i, brev, dist)
                        #print(data[brev])
                        th, tm = helper(dist-i, brev, data)
                        dist = dist - (dist- i)
                        #print(th, tm)
                        h += th
                        m += tm
                        brev = i
                    break
                  
                else:
                    h, m  = helper(dist, brevet_dist_km, data)
                    if key == 60:
                        h, m  = helper(dist, 60, data)
                        h += 1
                    #print("h =", h)
                    #print("m =", m)
                    break
            if key != 60:
                prev_keys.append(key)

            
    rslt = brevet_start_time.shift(hours = h, minutes = m)
    #print(rslt)
    return rslt

def helper(dist, brev, data):
    unMathed = (dist)/(data[brev])
    #print(data[brev])
    #print(unMathed)
    h = (dist) // (data[brev])
    m = round((unMathed - h) * 60)
    return (h, m)



#close_time(60, 600, arrow.now())
#print(temp)

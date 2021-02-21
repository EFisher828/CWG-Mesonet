import csv
import urllib.request
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib import cm
import datetime
import math
from datetime import timedelta
from datetime import datetime as dt
import shapefile as shp

def CWGMesonet():

    SCOfile = open('NCSCStations.txt')

    stid_string = ''

    for line in SCOfile:
        stid = line[0:4]
        stid_string = stid_string + stid + ','
    stid_string = stid_string[:-1]

    url = 'https://api.synopticdata.com/v2/stations/latest?stids={0}&vars=air_temp,dew_point_temperature,wind_speed,wind_direction&token=6352e76903434fe2bf18cf47b98589b5'.format(stid_string)
    print(url)
    response = urllib.request.urlopen(url)

    worktime = datetime.datetime.utcnow()
    time = datetime.datetime.now()
    polished = dt.strftime(time,"%I:%M %p")

    count1 = 0
    count2 = 0
    count3 = 0
    q = 0
    datalist = []
    elevlist = []
    dewlist = []
    windlist = []
    dirlist = []
    latlist = []
    lonlist = []
    namelist = []
    u = []
    v = []

    for line in response:
        fullstring = str(line)

        sections = fullstring.split('"STATUS":"ACTIVE"')
        
        for i in sections:
            if count3 > 0:
                tempstr = str(i)
                tempwork1 = tempstr.split('"date_time":"')
                time1 = str(tempwork1[1])
                time2 = time1.split('","')
                time3 = str(time2[0])
                time4 = dt.combine(worktime, dt.strptime(time3,"%Y-%m-%dT%H:%M:%S%z").time())
                minutes = (worktime - time4) // timedelta(minutes=1)
                #print(str(minutes) + ' ' + 'first if')

                if minutes < 120 and minutes > 0:
                    #print("Passed with " + str(minutes))
                    try:
                        tempsplit = (str(i)).split('"dew_point_temperature_value_1d":{"date_time":')
                        tempstr = str(tempsplit[1])
                        tempstr2 = tempstr.split('"value":')
                        tempstr3 = str(tempstr2[1])
                        tempwork1 = tempstr3.split('}')
                        dew1 = ((eval(tempwork1[0]))*(9/5))+32
                        dew2 = round(dew1)

                        try:
                            tempsplit = (str(i)).split('"air_temp_value_1":{"date_time":')
                            tempstr = str(tempsplit[1])
                            tempstr2 = tempstr.split('"value":')
                            tempstr3 = str(tempstr2[1])
                            tempwork1 = tempstr3.split('}')
                            temp1 = ((eval(tempwork1[0]))*(9/5))+32
                            temp2 = round(temp1)

                            try:
                                tempsplit = (str(i)).split('"wind_speed_value_1":{"date_time":')
                                tempstr = str(tempsplit[1])
                                tempstr2 = tempstr.split('"value":')
                                tempstr3 = str(tempstr2[1])
                                tempwork1 = tempstr3.split('}')
                                wind1 = ((eval(tempwork1[0]))*1.94384)
                                wind2 = round(wind1,1)

                                try:
                                    tempsplit = (str(i)).split('"wind_direction_value_1":{"date_time":')
                                    tempstr = str(tempsplit[1])
                                    tempstr2 = tempstr.split('"value":')
                                    tempstr3 = str(tempstr2[1])
                                    tempwork1 = tempstr3.split('}')
                                    dir1 = (eval(tempwork1[0]))
                                    dir2 = dir1
                                    
                                    try:
                                        tempsplit = (str(i)).split('"LATITUDE":"')
                                        tempstr = str(tempsplit[1])
                                        tempstr2 = tempstr.split('"')
                                        lat = eval(tempstr2[0])

                                        try:
                                            tempsplit = (str(i)).split('"LONGITUDE":"')
                                            tempstr = str(tempsplit[1])
                                            tempstr2 = tempstr.split('"')
                                            lon = eval(tempstr2[0])
                                    
                                            if temp2 > dew2 and temp2 > -35 and dew2 > -35:
                                                dewlist.append(dew2)
                                                #print(str(temp2) + ' ' + str(dew2))
                                                datalist.append(temp2)
                                                windlist.append(wind2)
                                                dirlist.append(dir2)
                                                latlist.append(lat)
                                                lonlist.append(lon) 
                                                elevsplit = (str(i)).split('"ELEVATION":"')
                                                tempstr = str(elevsplit[1])
                                                tempwork1 = tempstr.split('",')
                                                elev = eval(tempwork1[0])
                                                elevlist.append(elev)

                                                stidsplit = (str(i)).split('"STID":"')
                                                tempstr = str(stidsplit[1])
                                                tempwork1 = tempstr.split('","')
                                                stid = str(tempwork1[0])
                                                namelist.append(stid)
                                            else:
                                                pass
                                        except:
                                            pass
                                    except:
                                        pass
                                except:
                                    pass
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                    
                else:
                    #print("Failed with " + str(minutes))
                    pass
                
                q = q + 1

            else:
                count3 = count3 + 1
    uf = len(datalist)
    df = len(dewlist)
    hf = len(lonlist)
    jf = len(latlist)
    print("Length plotdata " + str(df))
    print("Length plotdew " + str(uf))
    print("Length x " + str(hf))
    print("Length y " + str(jf))
    f = 0
    for q in dirlist:
        Dir_4 = dirlist[f]
        Speed_4 = windlist[f]
        if Dir_4 < 90:
            offset = 90 - Dir_4
            deg_direction = Dir_4 + 90 + 2*offset
        else:
            offset = 90 - Dir_4
                
        deg_direction = Dir_4 + 90 + 2*offset
        rad_direction = math.radians(deg_direction)
        speed = Speed_4
        u.append(speed*math.cos(rad_direction))
        v.append(speed*math.sin(rad_direction))
        f = f + 1

    print(latlist)
    print(lonlist)
    print(namelist)

    fig = plt.figure(figsize=(13,8))
    ax = plt.axes()
    ax.axis('off')
    ax.barbs(lonlist,latlist,u,v, length=6,color='black',zorder=4)
    p = 0
    for b in lonlist:
        plt.text((lonlist[p])-0.2,(latlist[p])+0.06,datalist[p],color='red',size=9,weight='bold')
        #print("Temp " + str(p))
        plt.text((lonlist[p])-0.2,(latlist[p])-0.1,dewlist[p],color='green',size=9,weight='bold')
        p = p + 1
    ax.set(xlim=(-84.6, -75.2), ylim=(31.82, 37))
    plt.xlim(-84.6, -75.2)
    plt.ylim(31.82, 37)

    sf = shp.Reader("NC & SC Counties.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='grey', linewidth=0.3)

    sf = shp.Reader("NC & SC State.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='dimgrey', linewidth=0.5)

    sf = shp.Reader("NC & SC Highways.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='dimgrey', linewidth=0.3)

    im = plt.imread('CWGLogo.png')
    newax = fig.add_axes([0.65, 0.13, 0.2, 0.2], anchor='SE', zorder=-1)
    newax.imshow(im)
    newax.axis('off')
    
    fig.text(0.5,0.9,f"Valid {polished}",color='black',size=15,ha='center')
    plt.savefig("output/CWGMesonet.png",bbox_inches='tight',dpi=300)

    #WNC

    fig = plt.figure(figsize=(11,5))
    ax = plt.axes()

    xmin = -84.5244
    xmax = -80.2544
    ymin = 34.7489
    ymax = 36.6667
    ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    wnctemp = []
    wncdew = []
    wncelev = []
    wncwind = []
    wncdir = []
    wnclat = []
    wnclon = []
    wncnames = []

    overlapcount = 0
    for i in namelist:
        name_lon = lonlist[overlapcount]
        name_lat = latlist[overlapcount]
        if name_lon < xmax and name_lon > xmin and name_lat < ymax and name_lat > ymin:
            wncnames.append(i)
            wnctemp.append(datalist[overlapcount])
            wncdew.append(dewlist[overlapcount])
            wncwind.append(windlist[overlapcount])
            wncdir.append(dirlist[overlapcount])
            wnclat.append(latlist[overlapcount])
            wnclon.append(lonlist[overlapcount])
        overlapcount = overlapcount + 1

    SCOfile = open('WNCStations.txt')

    stid_string = ''

    for line in SCOfile:
        stid = line[0:4]
        stid_string = stid_string + stid + ','
    stid_string = stid_string[:-1]

    url = 'https://api.synopticdata.com/v2/stations/latest?stids={0}&vars=air_temp,dew_point_temperature,wind_speed,wind_direction&token=6352e76903434fe2bf18cf47b98589b5'.format(stid_string)
    print(url)
    response = urllib.request.urlopen(url)

    worktime = datetime.datetime.utcnow()
    time = datetime.datetime.now()
    polished = dt.strftime(time,"%I:%M %p")

    count1 = 0
    count2 = 0
    count3 = 0
    q = 0
    u = []
    v = []

    for line in response:
        fullstring = str(line)

        sections = fullstring.split('"STATUS":"ACTIVE"')
        
        for i in sections:
            if count3 > 0:
                tempstr = str(i)
                tempwork1 = tempstr.split('"date_time":"')
                time1 = str(tempwork1[1])
                time2 = time1.split('","')
                time3 = str(time2[0])
                time4 = dt.combine(worktime, dt.strptime(time3,"%Y-%m-%dT%H:%M:%S%z").time())
                minutes = (worktime - time4) // timedelta(minutes=1)
                #print(str(minutes) + ' ' + 'first if')

                if minutes < 120 and minutes > 0:
                    #print("Passed with " + str(minutes))
                    try:
                        tempsplit = (str(i)).split('"dew_point_temperature_value_1d":{"date_time":')
                        tempstr = str(tempsplit[1])
                        tempstr2 = tempstr.split('"value":')
                        tempstr3 = str(tempstr2[1])
                        tempwork1 = tempstr3.split('}')
                        dew1 = ((eval(tempwork1[0]))*(9/5))+32
                        dew2 = round(dew1)

                        try:
                            tempsplit = (str(i)).split('"air_temp_value_1":{"date_time":')
                            tempstr = str(tempsplit[1])
                            tempstr2 = tempstr.split('"value":')
                            tempstr3 = str(tempstr2[1])
                            tempwork1 = tempstr3.split('}')
                            temp1 = ((eval(tempwork1[0]))*(9/5))+32
                            temp2 = round(temp1)

                            try:
                                tempsplit = (str(i)).split('"wind_speed_value_1":{"date_time":')
                                tempstr = str(tempsplit[1])
                                tempstr2 = tempstr.split('"value":')
                                tempstr3 = str(tempstr2[1])
                                tempwork1 = tempstr3.split('}')
                                wind1 = ((eval(tempwork1[0]))*1.94384)
                                wind2 = round(wind1,1)

                                try:
                                    tempsplit = (str(i)).split('"wind_direction_value_1":{"date_time":')
                                    tempstr = str(tempsplit[1])
                                    tempstr2 = tempstr.split('"value":')
                                    tempstr3 = str(tempstr2[1])
                                    tempwork1 = tempstr3.split('}')
                                    dir1 = (eval(tempwork1[0]))
                                    dir2 = dir1
                                    
                                    try:
                                        tempsplit = (str(i)).split('"LATITUDE":"')
                                        tempstr = str(tempsplit[1])
                                        tempstr2 = tempstr.split('"')
                                        lat = eval(tempstr2[0])

                                        try:
                                            tempsplit = (str(i)).split('"LONGITUDE":"')
                                            tempstr = str(tempsplit[1])
                                            tempstr2 = tempstr.split('"')
                                            lon = eval(tempstr2[0])
                                    
                                            if temp2 > dew2 and temp2 > -35 and dew2 > -35:
                                                wncdew.append(dew2)
                                                #print(str(temp2) + ' ' + str(dew2))
                                                wnctemp.append(temp2)
                                                wncwind.append(wind2)
                                                wncdir.append(dir2)
                                                wnclat.append(lat)
                                                wnclon.append(lon) 
                                                elevsplit = (str(i)).split('"ELEVATION":"')
                                                tempstr = str(elevsplit[q])
                                                tempwork1 = tempstr.split('",')
                                                elev = eval(tempwork1[0])
                                                wncelev.append(elev)

                                                stidsplit = (str(i)).split('"STID":"')
                                                tempstr = str(stidsplit[q])
                                                tempwork1 = tempstr.split('","')
                                                stid = str(tempwork1[0])
                                                wncnames.append(stid)
                                            else:
                                                pass
                                        except:
                                            pass
                                    except:
                                        pass
                                except:
                                    pass
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                    
                else:
                    #print("Failed with " + str(minutes))
                    pass
                
                q = q + 1

            else:
                count3 = count3 + 1
    uf = len(wnctemp)
    df = len(wncdew)
    hf = len(wnclon)
    jf = len(wnclat)
    print("Length plotdata " + str(df))
    print("Length plotdew " + str(uf))
    print("Length x " + str(hf))
    print("Length y " + str(jf))
    f = 0
    for q in wncdir:
        Dir_4 = wncdir[f]
        Speed_4 = wncwind[f]
        if Dir_4 < 90:
            offset = 90 - Dir_4
            deg_direction = Dir_4 + 90 + 2*offset
        else:
            offset = 90 - Dir_4
                
        deg_direction = Dir_4 + 90 + 2*offset
        rad_direction = math.radians(deg_direction)
        speed = Speed_4
        u.append(speed*math.cos(rad_direction))
        v.append(speed*math.sin(rad_direction))
        f = f + 1


    ax.axis('off')
    ax.barbs(wnclon,wnclat,u,v, length=6,color='black',zorder=4)
    p = 0
    for b in wnclon:
        plt.text((wnclon[p])-0.15,(wnclat[p])+0.05,wnctemp[p],color='red',size=9,weight='bold')
        #print("Temp " + str(p))
        plt.text((wnclon[p])-0.15,(wnclat[p])-0.09,wncdew[p],color='green',size=9,weight='bold')
        p = p + 1

    sf = shp.Reader("NC & SC Counties.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='grey', linewidth=0.3)

    sf = shp.Reader("NC & SC State.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='dimgrey', linewidth=0.5)

    sf = shp.Reader("NC & SC Highways.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='dimgrey', linewidth=0.3)
    
    fig.text(0.5,0.97,f"Valid {polished}",color='black',size=15,ha='center')
    fig.text(0.5,0.92,"CarolinaWeatherGroup.com",color='black',size=12,ha='center')
    plt.savefig("output/WNCMesonet.png",bbox_inches='tight',dpi=300)

    #Central NC

    fig = plt.figure(figsize=(11,5))
    ax = plt.axes()
    
    xmin = -81.6826
    xmax = -77.4126
    ymin = 34.7489
    ymax = 36.6667
    ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    wnctemp = []
    wncdew = []
    wncelev = []
    wncwind = []
    wncdir = []
    wnclat = []
    wnclon = []
    wncnames = []

    overlapcount = 0
    for i in namelist:
        name_lon = lonlist[overlapcount]
        name_lat = latlist[overlapcount]
        if name_lon < xmax and name_lon > xmin and name_lat < ymax and name_lat > ymin:
            wncnames.append(i)
            wnctemp.append(datalist[overlapcount])
            wncdew.append(dewlist[overlapcount])
            wncwind.append(windlist[overlapcount])
            wncdir.append(dirlist[overlapcount])
            wnclat.append(latlist[overlapcount])
            wnclon.append(lonlist[overlapcount])
        overlapcount = overlapcount + 1

    SCOfile = open('CNCStations.txt')

    stid_string = ''

    for line in SCOfile:
        stid = line[0:4]
        stid_string = stid_string + stid + ','
    stid_string = stid_string[:-1]

    url = 'https://api.synopticdata.com/v2/stations/latest?stids={0}&vars=air_temp,dew_point_temperature,wind_speed,wind_direction&token=6352e76903434fe2bf18cf47b98589b5'.format(stid_string)
    print(url)
    response = urllib.request.urlopen(url)

    worktime = datetime.datetime.utcnow()
    time = datetime.datetime.now()
    polished = dt.strftime(time,"%I:%M %p")

    count1 = 0
    count2 = 0
    count3 = 0
    q = 0
    u = []
    v = []

    for line in response:
        fullstring = str(line)

        sections = fullstring.split('"STATUS":"ACTIVE"')
        
        for i in sections:
            if count3 > 0:
                tempstr = str(i)
                tempwork1 = tempstr.split('"date_time":"')
                time1 = str(tempwork1[1])
                time2 = time1.split('","')
                time3 = str(time2[0])
                time4 = dt.combine(worktime, dt.strptime(time3,"%Y-%m-%dT%H:%M:%S%z").time())
                minutes = (worktime - time4) // timedelta(minutes=1)
                #print(str(minutes) + ' ' + 'first if')

                if minutes < 120 and minutes > 0:
                    #print("Passed with " + str(minutes))
                    try:
                        tempsplit = (str(i)).split('"dew_point_temperature_value_1d":{"date_time":')
                        tempstr = str(tempsplit[1])
                        tempstr2 = tempstr.split('"value":')
                        tempstr3 = str(tempstr2[1])
                        tempwork1 = tempstr3.split('}')
                        dew1 = ((eval(tempwork1[0]))*(9/5))+32
                        dew2 = round(dew1)

                        try:
                            tempsplit = (str(i)).split('"air_temp_value_1":{"date_time":')
                            tempstr = str(tempsplit[1])
                            tempstr2 = tempstr.split('"value":')
                            tempstr3 = str(tempstr2[1])
                            tempwork1 = tempstr3.split('}')
                            temp1 = ((eval(tempwork1[0]))*(9/5))+32
                            temp2 = round(temp1)

                            try:
                                tempsplit = (str(i)).split('"wind_speed_value_1":{"date_time":')
                                tempstr = str(tempsplit[1])
                                tempstr2 = tempstr.split('"value":')
                                tempstr3 = str(tempstr2[1])
                                tempwork1 = tempstr3.split('}')
                                wind1 = ((eval(tempwork1[0]))*1.94384)
                                wind2 = round(wind1,1)

                                try:
                                    tempsplit = (str(i)).split('"wind_direction_value_1":{"date_time":')
                                    tempstr = str(tempsplit[1])
                                    tempstr2 = tempstr.split('"value":')
                                    tempstr3 = str(tempstr2[1])
                                    tempwork1 = tempstr3.split('}')
                                    dir1 = (eval(tempwork1[0]))
                                    dir2 = dir1
                                    
                                    try:
                                        tempsplit = (str(i)).split('"LATITUDE":"')
                                        tempstr = str(tempsplit[1])
                                        tempstr2 = tempstr.split('"')
                                        lat = eval(tempstr2[0])

                                        try:
                                            tempsplit = (str(i)).split('"LONGITUDE":"')
                                            tempstr = str(tempsplit[1])
                                            tempstr2 = tempstr.split('"')
                                            lon = eval(tempstr2[0])
                                    
                                            if temp2 > dew2 and temp2 > -35 and dew2 > -35:
                                                wncdew.append(dew2)
                                                #print(str(temp2) + ' ' + str(dew2))
                                                wnctemp.append(temp2)
                                                wncwind.append(wind2)
                                                wncdir.append(dir2)
                                                wnclat.append(lat)
                                                wnclon.append(lon) 
                                                elevsplit = (str(i)).split('"ELEVATION":"')
                                                tempstr = str(elevsplit[q])
                                                tempwork1 = tempstr.split('",')
                                                elev = eval(tempwork1[0])
                                                wncelev.append(elev)

                                                stidsplit = (str(i)).split('"STID":"')
                                                tempstr = str(stidsplit[q])
                                                tempwork1 = tempstr.split('","')
                                                stid = str(tempwork1[0])
                                                wncnames.append(stid)
                                            else:
                                                pass
                                        except:
                                            pass
                                    except:
                                        pass
                                except:
                                    pass
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                    
                else:
                    #print("Failed with " + str(minutes))
                    pass
                
                q = q + 1

            else:
                count3 = count3 + 1
    uf = len(wnctemp)
    df = len(wncdew)
    hf = len(wnclon)
    jf = len(wnclat)
    print("Length plotdata " + str(df))
    print("Length plotdew " + str(uf))
    print("Length x " + str(hf))
    print("Length y " + str(jf))
    f = 0
    for q in wncdir:
        Dir_4 = wncdir[f]
        Speed_4 = wncwind[f]
        if Dir_4 < 90:
            offset = 90 - Dir_4
            deg_direction = Dir_4 + 90 + 2*offset
        else:
            offset = 90 - Dir_4
                
        deg_direction = Dir_4 + 90 + 2*offset
        rad_direction = math.radians(deg_direction)
        speed = Speed_4
        u.append(speed*math.cos(rad_direction))
        v.append(speed*math.sin(rad_direction))
        f = f + 1


    ax.axis('off')
    ax.barbs(wnclon,wnclat,u,v, length=6,color='black',zorder=4)
    p = 0
    for b in wnclon:
        plt.text((wnclon[p])-0.15,(wnclat[p])+0.05,wnctemp[p],color='red',size=9,weight='bold')
        #print("Temp " + str(p))
        plt.text((wnclon[p])-0.15,(wnclat[p])-0.09,wncdew[p],color='green',size=9,weight='bold')
        p = p + 1

    sf = shp.Reader("NC & SC Counties.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='grey', linewidth=0.3)

    sf = shp.Reader("NC & SC State.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='dimgrey', linewidth=0.5)

    sf = shp.Reader("NC & SC Highways.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='dimgrey', linewidth=0.3)
    
    fig.text(0.5,0.97,f"Valid {polished}",color='black',size=15,ha='center')
    fig.text(0.5,0.92,"CarolinaWeatherGroup.com",color='black',size=12,ha='center')
    plt.savefig("output/CNCMesonet.png",bbox_inches='tight',dpi=300)

    #Upstate SC

    fig = plt.figure(figsize=(11,5))
    ax = plt.axes()

    xmin = -83.4771
    xmax = -79.2071
    ymin = 33.3899
    ymax = 35.3395
    ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    wnctemp = []
    wncdew = []
    wncelev = []
    wncwind = []
    wncdir = []
    wnclat = []
    wnclon = []
    wncnames = []

    overlapcount = 0
    for i in namelist:
        name_lon = lonlist[overlapcount]
        name_lat = latlist[overlapcount]
        if name_lon < xmax and name_lon > xmin and name_lat < ymax and name_lat > ymin:
            wncnames.append(i)
            wnctemp.append(datalist[overlapcount])
            wncdew.append(dewlist[overlapcount])
            wncwind.append(windlist[overlapcount])
            wncdir.append(dirlist[overlapcount])
            wnclat.append(latlist[overlapcount])
            wnclon.append(lonlist[overlapcount])
        overlapcount = overlapcount + 1

    SCOfile = open('USCStations.txt')

    stid_string = ''

    for line in SCOfile:
        stid = line[0:4]
        stid_string = stid_string + stid + ','
    stid_string = stid_string[:-1]

    url = 'https://api.synopticdata.com/v2/stations/latest?stids={0}&vars=air_temp,dew_point_temperature,wind_speed,wind_direction&token=6352e76903434fe2bf18cf47b98589b5'.format(stid_string)
    print(url)
    response = urllib.request.urlopen(url)

    worktime = datetime.datetime.utcnow()
    time = datetime.datetime.now()
    polished = dt.strftime(time,"%I:%M %p")

    count1 = 0
    count2 = 0
    count3 = 0
    q = 0
    u = []
    v = []

    for line in response:
        fullstring = str(line)

        sections = fullstring.split('"STATUS":"ACTIVE"')
        
        for i in sections:
            if count3 > 0:
                tempstr = str(i)
                tempwork1 = tempstr.split('"date_time":"')
                time1 = str(tempwork1[1])
                time2 = time1.split('","')
                time3 = str(time2[0])
                time4 = dt.combine(worktime, dt.strptime(time3,"%Y-%m-%dT%H:%M:%S%z").time())
                minutes = (worktime - time4) // timedelta(minutes=1)
                #print(str(minutes) + ' ' + 'first if')

                if minutes < 120 and minutes > 0:
                    #print("Passed with " + str(minutes))
                    try:
                        tempsplit = (str(i)).split('"dew_point_temperature_value_1d":{"date_time":')
                        tempstr = str(tempsplit[1])
                        tempstr2 = tempstr.split('"value":')
                        tempstr3 = str(tempstr2[1])
                        tempwork1 = tempstr3.split('}')
                        dew1 = ((eval(tempwork1[0]))*(9/5))+32
                        dew2 = round(dew1)

                        try:
                            tempsplit = (str(i)).split('"air_temp_value_1":{"date_time":')
                            tempstr = str(tempsplit[1])
                            tempstr2 = tempstr.split('"value":')
                            tempstr3 = str(tempstr2[1])
                            tempwork1 = tempstr3.split('}')
                            temp1 = ((eval(tempwork1[0]))*(9/5))+32
                            temp2 = round(temp1)

                            try:
                                tempsplit = (str(i)).split('"wind_speed_value_1":{"date_time":')
                                tempstr = str(tempsplit[1])
                                tempstr2 = tempstr.split('"value":')
                                tempstr3 = str(tempstr2[1])
                                tempwork1 = tempstr3.split('}')
                                wind1 = ((eval(tempwork1[0]))*1.94384)
                                wind2 = round(wind1,1)

                                try:
                                    tempsplit = (str(i)).split('"wind_direction_value_1":{"date_time":')
                                    tempstr = str(tempsplit[1])
                                    tempstr2 = tempstr.split('"value":')
                                    tempstr3 = str(tempstr2[1])
                                    tempwork1 = tempstr3.split('}')
                                    dir1 = (eval(tempwork1[0]))
                                    dir2 = dir1
                                    
                                    try:
                                        tempsplit = (str(i)).split('"LATITUDE":"')
                                        tempstr = str(tempsplit[1])
                                        tempstr2 = tempstr.split('"')
                                        lat = eval(tempstr2[0])

                                        try:
                                            tempsplit = (str(i)).split('"LONGITUDE":"')
                                            tempstr = str(tempsplit[1])
                                            tempstr2 = tempstr.split('"')
                                            lon = eval(tempstr2[0])
                                    
                                            if temp2 > dew2 and temp2 > -35 and dew2 > -35:
                                                wncdew.append(dew2)
                                                #print(str(temp2) + ' ' + str(dew2))
                                                wnctemp.append(temp2)
                                                wncwind.append(wind2)
                                                wncdir.append(dir2)
                                                wnclat.append(lat)
                                                wnclon.append(lon) 
                                                elevsplit = (str(i)).split('"ELEVATION":"')
                                                tempstr = str(elevsplit[q])
                                                tempwork1 = tempstr.split('",')
                                                elev = eval(tempwork1[0])
                                                wncelev.append(elev)

                                                stidsplit = (str(i)).split('"STID":"')
                                                tempstr = str(stidsplit[q])
                                                tempwork1 = tempstr.split('","')
                                                stid = str(tempwork1[0])
                                                wncnames.append(stid)
                                            else:
                                                pass
                                        except:
                                            pass
                                    except:
                                        pass
                                except:
                                    pass
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                    
                else:
                    #print("Failed with " + str(minutes))
                    pass
                
                q = q + 1

            else:
                count3 = count3 + 1
    uf = len(wnctemp)
    df = len(wncdew)
    hf = len(wnclon)
    jf = len(wnclat)
    print("Length plotdata " + str(df))
    print("Length plotdew " + str(uf))
    print("Length x " + str(hf))
    print("Length y " + str(jf))
    f = 0
    for q in wncdir:
        Dir_4 = wncdir[f]
        Speed_4 = wncwind[f]
        if Dir_4 < 90:
            offset = 90 - Dir_4
            deg_direction = Dir_4 + 90 + 2*offset
        else:
            offset = 90 - Dir_4
                
        deg_direction = Dir_4 + 90 + 2*offset
        rad_direction = math.radians(deg_direction)
        speed = Speed_4
        u.append(speed*math.cos(rad_direction))
        v.append(speed*math.sin(rad_direction))
        f = f + 1


    ax.axis('off')
    ax.barbs(wnclon,wnclat,u,v, length=6,color='black',zorder=4)
    p = 0
    for b in wnclon:
        plt.text((wnclon[p])-0.15,(wnclat[p])+0.05,wnctemp[p],color='red',size=9,weight='bold')
        #print("Temp " + str(p))
        plt.text((wnclon[p])-0.15,(wnclat[p])-0.09,wncdew[p],color='green',size=9,weight='bold')
        p = p + 1

    sf = shp.Reader("NC & SC Counties.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='grey', linewidth=0.3)

    sf = shp.Reader("NC & SC State.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='dimgrey', linewidth=0.5)

    sf = shp.Reader("NC & SC Highways.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='dimgrey', linewidth=0.3)
    
    fig.text(0.5,0.97,f"Valid {polished}",color='black',size=15,ha='center')
    fig.text(0.5,0.92,"CarolinaWeatherGroup.com",color='black',size=12,ha='center')
    plt.savefig("output/USCMesonet.png",bbox_inches='tight',dpi=300)

    fig = plt.figure(figsize=(11,5))
    ax = plt.axes()
    
    xmin = -82.2027
    xmax = -77.9326
    ymin = 32.0652
    ymax = 34.0448
    ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    wnctemp = []
    wncdew = []
    wncelev = []
    wncwind = []
    wncdir = []
    wnclat = []
    wnclon = []
    wncnames = []

    overlapcount = 0
    for i in namelist:
        name_lon = lonlist[overlapcount]
        name_lat = latlist[overlapcount]
        if name_lon < xmax and name_lon > xmin and name_lat < ymax and name_lat > ymin:
            wncnames.append(i)
            wnctemp.append(datalist[overlapcount])
            wncdew.append(dewlist[overlapcount])
            wncwind.append(windlist[overlapcount])
            wncdir.append(dirlist[overlapcount])
            wnclat.append(latlist[overlapcount])
            wnclon.append(lonlist[overlapcount])
        overlapcount = overlapcount + 1

    SCOfile = open('CSCStations.txt')

    stid_string = ''

    for line in SCOfile:
        stid = line[0:4]
        stid_string = stid_string + stid + ','
    stid_string = stid_string[:-1]

    url = 'https://api.synopticdata.com/v2/stations/latest?stids={0}&vars=air_temp,dew_point_temperature,wind_speed,wind_direction&token=6352e76903434fe2bf18cf47b98589b5'.format(stid_string)
    print(url)
    response = urllib.request.urlopen(url)

    worktime = datetime.datetime.utcnow()
    time = datetime.datetime.now()
    polished = dt.strftime(time,"%I:%M %p")

    count1 = 0
    count2 = 0
    count3 = 0
    q = 0
    u = []
    v = []

    for line in response:
        fullstring = str(line)

        sections = fullstring.split('"STATUS":"ACTIVE"')
        
        for i in sections:
            if count3 > 0:
                tempstr = str(i)
                tempwork1 = tempstr.split('"date_time":"')
                time1 = str(tempwork1[1])
                time2 = time1.split('","')
                time3 = str(time2[0])
                time4 = dt.combine(worktime, dt.strptime(time3,"%Y-%m-%dT%H:%M:%S%z").time())
                minutes = (worktime - time4) // timedelta(minutes=1)
                #print(str(minutes) + ' ' + 'first if')

                if minutes < 120 and minutes > 0:
                    #print("Passed with " + str(minutes))
                    try:
                        tempsplit = (str(i)).split('"dew_point_temperature_value_1d":{"date_time":')
                        tempstr = str(tempsplit[1])
                        tempstr2 = tempstr.split('"value":')
                        tempstr3 = str(tempstr2[1])
                        tempwork1 = tempstr3.split('}')
                        dew1 = ((eval(tempwork1[0]))*(9/5))+32
                        dew2 = round(dew1)

                        try:
                            tempsplit = (str(i)).split('"air_temp_value_1":{"date_time":')
                            tempstr = str(tempsplit[1])
                            tempstr2 = tempstr.split('"value":')
                            tempstr3 = str(tempstr2[1])
                            tempwork1 = tempstr3.split('}')
                            temp1 = ((eval(tempwork1[0]))*(9/5))+32
                            temp2 = round(temp1)

                            try:
                                tempsplit = (str(i)).split('"wind_speed_value_1":{"date_time":')
                                tempstr = str(tempsplit[1])
                                tempstr2 = tempstr.split('"value":')
                                tempstr3 = str(tempstr2[1])
                                tempwork1 = tempstr3.split('}')
                                wind1 = ((eval(tempwork1[0]))*1.94384)
                                wind2 = round(wind1,1)

                                try:
                                    tempsplit = (str(i)).split('"wind_direction_value_1":{"date_time":')
                                    tempstr = str(tempsplit[1])
                                    tempstr2 = tempstr.split('"value":')
                                    tempstr3 = str(tempstr2[1])
                                    tempwork1 = tempstr3.split('}')
                                    dir1 = (eval(tempwork1[0]))
                                    dir2 = dir1
                                    
                                    try:
                                        tempsplit = (str(i)).split('"LATITUDE":"')
                                        tempstr = str(tempsplit[1])
                                        tempstr2 = tempstr.split('"')
                                        lat = eval(tempstr2[0])

                                        try:
                                            tempsplit = (str(i)).split('"LONGITUDE":"')
                                            tempstr = str(tempsplit[1])
                                            tempstr2 = tempstr.split('"')
                                            lon = eval(tempstr2[0])
                                    
                                            if temp2 > dew2 and temp2 > -35 and dew2 > -35:
                                                wncdew.append(dew2)
                                                #print(str(temp2) + ' ' + str(dew2))
                                                wnctemp.append(temp2)
                                                wncwind.append(wind2)
                                                wncdir.append(dir2)
                                                wnclat.append(lat)
                                                wnclon.append(lon) 
                                                elevsplit = (str(i)).split('"ELEVATION":"')
                                                tempstr = str(elevsplit[q])
                                                tempwork1 = tempstr.split('",')
                                                elev = eval(tempwork1[0])
                                                wncelev.append(elev)

                                                stidsplit = (str(i)).split('"STID":"')
                                                tempstr = str(stidsplit[q])
                                                tempwork1 = tempstr.split('","')
                                                stid = str(tempwork1[0])
                                                wncnames.append(stid)
                                            else:
                                                pass
                                        except:
                                            pass
                                    except:
                                        pass
                                except:
                                    pass
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                    
                else:
                    #print("Failed with " + str(minutes))
                    pass
                
                q = q + 1

            else:
                count3 = count3 + 1
    uf = len(wnctemp)
    df = len(wncdew)
    hf = len(wnclon)
    jf = len(wnclat)
    print("Length plotdata " + str(df))
    print("Length plotdew " + str(uf))
    print("Length x " + str(hf))
    print("Length y " + str(jf))
    f = 0
    for q in wncdir:
        Dir_4 = wncdir[f]
        Speed_4 = wncwind[f]
        if Dir_4 < 90:
            offset = 90 - Dir_4
            deg_direction = Dir_4 + 90 + 2*offset
        else:
            offset = 90 - Dir_4
                
        deg_direction = Dir_4 + 90 + 2*offset
        rad_direction = math.radians(deg_direction)
        speed = Speed_4
        u.append(speed*math.cos(rad_direction))
        v.append(speed*math.sin(rad_direction))
        f = f + 1


    ax.axis('off')
    ax.barbs(wnclon,wnclat,u,v, length=6,color='black',zorder=4)
    p = 0
    for b in wnclon:
        plt.text((wnclon[p])-0.15,(wnclat[p])+0.05,wnctemp[p],color='red',size=9,weight='bold')
        #print("Temp " + str(p))
        plt.text((wnclon[p])-0.15,(wnclat[p])-0.09,wncdew[p],color='green',size=9,weight='bold')
        p = p + 1

    sf = shp.Reader("NC & SC Counties.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='grey', linewidth=0.3)

    sf = shp.Reader("NC & SC State.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='dimgrey', linewidth=0.5)

    sf = shp.Reader("NC & SC Highways.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='dimgrey', linewidth=0.3)
    
    fig.text(0.5,0.97,f"Valid {polished}",color='black',size=15,ha='center')
    fig.text(0.5,0.92,"CarolinaWeatherGroup.com",color='black',size=12,ha='center')
    plt.savefig("output/CSCMesonet.png",bbox_inches='tight',dpi=300)
    
CWGMesonet()

import sys
print sys.version

from pyearth import Earth, export
import numpy as np
import re
from scipy import stats
import sys
import ast

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)
#print 'Made it!'

#print ast.literal_eval(sys.argv[1])[0]

def print_stuff(whatever):
    return str(whatever)

def calc_bandgap_point(energy,absorption):
    model = Earth()
    energy = np.array(energy)
    absorption = np.array(absorption)
    model.fit(energy,absorption)
    
    energy_elbows = []
    energy_elbows.append(min(energy))
    energy_elbows.append(max(energy))
    for coeff in list(model.basis_)[1:]:
        try:
            if float(re.findall("\d+\.\d+", str(coeff))[0]) not in energy_elbows:
                energy_elbows.append(float(re.findall("\d+\.\d+", str(coeff))[0]))
        except IndexError:
            print(coeff)
            pass
    
    y_hat = model.predict(energy)
    function = export.export_sympy(model)
    
    direct_abs_elbows = []
    for coeff in energy_elbows:
        direct_abs_elbows.append(function.evalf(subs={'x0':coeff}))
    elbows_list = []
    for elbow_num in range(0,len(energy_elbows)):
        elbows_list.append(tuple([energy_elbows[elbow_num],direct_abs_elbows[elbow_num]]))
    elbows_list = sorted(elbows_list)
    line_segs = []
    for point in range(0,len(elbows_list)-1):
        que = [] #ENERGY SEGMENT
        que_abs = [] #ABSORPTION SEGMENT
        for w in range(0,len(energy)):
            if energy[w]>elbows_list[point][0] and energy[w]<elbows_list[point+1][0]:
                que.append(energy[w])
                que_abs.append(absorption[w])
        num_pts = len(que)
        x_length = elbows_list[point+1][0]-elbows_list[point][0]
        length = ((elbows_list[point+1][0]-elbows_list[point][0])**2\
        +(elbows_list[point+1][1]-elbows_list[point][1])**2)**.5
        slope = (elbows_list[point+1][1]-elbows_list[point][1])/(elbows_list[point+1][0]-elbows_list[point][0])
        y_intercept = elbows_list[point+1][1]-slope*elbows_list[point+1][0]
        x_intercept = (-1*y_intercept) / slope
        weighting_factor = slope**2 * x_length*2 * abs(length)**.5 * num_pts
        #RMSE CALCULATION
        RMSE_li = []
        for w in range(0,len(que)):
            RMSE_li.append((((que[w]*slope)+y_intercept)-que_abs[w])**2)
        RMSE = sum(RMSE_li)**.5
        #BARTLETT CALCULATION
        que_abs_ideal = []
        for w in range(0,len(que)):
            que_abs_ideal.append((que[w]*slope)+y_intercept)
        bartlett_stat, p_value = stats.bartlett(que_abs_ideal,que_abs)
        #WIDTH OF CONFIDENCE INTERVAL
        diff = []
        for w in range(0,len(que)):
            diff.append(((que[w]*slope)+y_intercept)-que_abs[w])
        s_err = np.sum(np.power(diff,2))
        p_x = np.arange(np.min(que),np.max(que)+1,1)
        confs = 2*(2.31) * ((s_err/(len(diff)-2))*(1.0/len(diff) + (np.power((p_x-np.mean(que)),2)/ #2.31 = t value for 95% confidence
            ((np.sum(np.power(que,2)))-len(diff)*(np.power(np.mean(que),2))))))**.5
        try:
            if x_intercept > 0 and slope > 0 and num_pts>10:
                line_segs.append(tuple([x_length,length,slope,y_intercept,x_intercept,weighting_factor,RMSE,bartlett_stat,p_value,float(confs[1])]))
        except TypeError:
            print('Complex Zoo Error')
            pass
    
    line_segs = sorted(line_segs,key=lambda item:item[5])
    try:
        winner = max(line_segs,key=lambda item:item[5])
    except ValueError:
        print('No segments available!')
        return None
    adj_energy=np.linspace(min(energy),max(energy),num=1000)
    adj_winner = []
    for t in adj_energy:
        adj_winner.append(t*float(winner[2])+float(winner[3]))
    return winner[4]



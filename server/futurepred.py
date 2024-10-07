from datetime import datetime
import matplotlib.pyplot as plt
from scipy import stats

def futurepred(matrix):
    """
    It takes a list of lists, sorts the list by date, then performs linear regression on the data, and
    returns a list of lists with the regression and estimation data
    
    :param matrix: a list of lists, where each list is a list of the form [x,y,date]
    :return: A list of lists.
    """
    try:
        datelist = []
        x = []
        y = []
        for i in matrix:
            datelist.append(i[2])
        sorteddatelist = sorted(
            datelist,
            key=lambda x: datetime.strptime(x, '%Y-%m-%d'))
        #key=lambda x: datetime.strptime(x, '%Y-%m-%d'), reverse=True)
        for u in matrix:
            checkpoint = 0
            for k in sorteddatelist:
                if checkpoint != 1:
                    if u[2] == k:
                        x.append(round(u[0],4))
                        y.append(round(u[1],4)) 
                        checkpoint = 1 

        slope, intercept, r, p, std_err = stats.linregress(x, y)

        def getreg(x):
            return round(slope * x + intercept,4)
        
        regression = list(map(getreg, x))
        datelength = list(range(1,len(sorteddatelist)+1))
        
        slope2, intercept2, r2, p2, std_err2 = stats.linregress(datelength, regression)
        
        if slope2 < 0:
            trend = '-1'
        else:
            trend = '1'
        
        def getest(datelength):
            return round(slope2*datelength+intercept2,4)
        
        est = list(map(getest, datelength))

        dataset = [['Date'],['Estimation'],['Regression']]
        for u in sorteddatelist:
            dataset[0].append(u)
        for u in regression:
            dataset[1].append(u)
        for u in est:
            dataset[2].append(u)
        return [dataset,trend]
    except Exception as e:
        pass

# plt.scatter(y,x)
# plt.scatter(regression, x)
# plt.plot(regression, x)
# plt.show()
# matrix = [[0.7365591397849462, 0.021505376344086023, '2022-11-29'], [0.9787234042553191, 0.0425531914893617, '2022-11-29'], [0.9901960784313726, 0.13725490196078433, '2022-11-29'], [0.8333333333333334, 0.0, '2022-11-27']]

# datelist = []
# x = []
# y = []
# for i in matrix:
#     datelist.append(i[2])
# sorteddatelist = sorted(
#     datelist,
#     key=lambda x: datetime.strptime(x, '%Y-%m-%d'))
# #key=lambda x: datetime.strptime(x, '%Y-%m-%d'), reverse=True)
#     for u in matrix:  
#     d = 0
#     for k in sorteddatelist: 
#         if d != 1: 
#             if u[2] == k:
#                 print(u[2])
#                 x.append(u[0])
#                 y.append(u[1])
#                 d = 1


# slope, intercept, r, p, std_err = stats.linregress(x, y)

# def getreg(x):
#     return slope * x + intercept

# regression = list(map(getreg, x))

# dataset = [['global_x'],['global_y'],['reg']]

# for u in x:
#     dataset[0].append(u)
# for u in y:
#     dataset[1].append(u)
# for u in regression:
#     dataset[2].append(u)

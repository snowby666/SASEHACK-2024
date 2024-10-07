import csv
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import numpy as np
from numpy.random import default_rng
import matplotlib.pyplot as plt
from sklearn import metrics
import pickle
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filename = open(DIR+'/server/static/server/model/facemodel.csv', 'r')
testfilename =  open(DIR+'/server/static/server/model/testmodel.csv', 'r')
# creating dictreader object
# 0 is stressed , 1 is not stressed
# count the dataset
f = open(DIR+'/server/static/server/model/facemodel.csv' ,'r')
reader = csv.reader(f, delimiter=",")
header = next(f) 
stressed = []
not_stressed = []
for row in reader:   
    if row[-1] == "0":
        stressed.append(int(row[-1]))  
    else:
        not_stressed.append(int(row[-1]))

file = csv.DictReader(filename)
frequency = []
robustness = []
labeldata = []
for col in file:
    frequency.append(float(col['Frequency']))
    robustness.append(float(col['Robustness']))
    labeldata.append(int(col['Label']))
data = np.column_stack((frequency,robustness))
plotdata = [[frequency[i], robustness[i]] for i in range(len(frequency))]

#get test data
testfile = csv.DictReader(testfilename)
frequencytest = []
robustnesstest = []
testLabel = []
for col in testfile:
    frequencytest.append(float(col['Frequency']))
    robustnesstest.append(float(col['Robustness']))
    testLabel.append(int(col['Label']))
testData = np.column_stack((frequencytest,robustnesstest))

# print(frequency)
# print(robustness)
# print(labeldata)
# print(data)

#K-fold cross validation
# for i in range(1,21):
#    list(range((x-1)*10,x*10))
#random validation
#list(rng.choice(200, size=100, replace=False))

#testmodel with subsample
error_dataset = []
f1_dataset = []
acc_dataset = []
auc_dataset = []
for v in range(2,70):
    acc_list = []
    f1_list = []
    k_list = []
    error_list = []
    prec_list = []
    rec_list = []
    auc_list = []
    # rng = default_rng()
    for x in range(1,11):
        newdata = []
        newlabel = []
        sampledata = []
        samplelabel = [] 
        falserandomindex = []
        randomindex = list(range((x-1)*20,x*20))
        falserandomindex = [k for k in range(0,200)]
        for u in randomindex:
            falserandomindex.remove(u)
        for i in randomindex:
            sampledata.append(plotdata[i])
            samplelabel.append(labeldata[i])
        for e in falserandomindex:
            newdata.append(plotdata[e])
            newlabel.append(labeldata[e])

        actuals = np.array(samplelabel)
        error_rate = []
        f1_rate = []
        acc_rate = []   
        rec_rate = []
        prec_rate = []
        auc_rate = []
        # for n_neighbors in range(2,50):
        knn = KNeighborsClassifier(n_neighbors=v, p=2, weights='uniform')
        knn.fit(newdata, newlabel)
        predictions = list(knn.predict(sampledata))
        accuracy = knn.score(sampledata, samplelabel)
        conf_matrix = confusion_matrix(y_true=samplelabel, y_pred=predictions)
        pred = np.array(predictions)
        
        y_pred_proba = knn.predict_proba(sampledata)[::,1]
        auc = metrics.roc_auc_score(samplelabel, y_pred_proba)
        
        acc_rate.append(accuracy)
        error_rate.append(np.mean(pred != actuals))
        prec_rate.append(precision_score(samplelabel,predictions))
        rec_rate.append(recall_score(samplelabel,predictions))
        f1_rate.append(f1_score(samplelabel,predictions))
        auc_rate.append(auc)
        
        # print('Accuracy: %.3f' % accuracy)
        # print('Precision: %.3f' % precision_score(samplelabel,predictions))
        # print('F1 Score: %.3f' % f1_score(samplelabel,predictions))
        # print('Error rate: %.3f \n' % np.mean(pred != actuals))
        f1_list.append(max(f1_rate))
        prec_list.append(max(prec_rate))
        rec_list.append(max(rec_rate))
        k_list.append(f1_rate.index(max(f1_rate))+2)
        acc_list.append(max(acc_rate))
        error_list.append(max(error_rate))
        auc_list.append(max(auc_rate))
        
    def most_common(lst):
        return max(set(lst), key=lst.count)
    final_rec = []
    final_prec = []
    final_f1 = []
    final_auc = []
    #filter the none data
    final_rec = [x for x in rec_list if x != 0]
    final_prec = [x for x in prec_list if x != 0]
    final_f1 = [x for x in f1_list if x != 0]
    final_auc = [x for x in auc_list if x!=0]
    print("Accuracy: ", np.mean(acc_list)*100)
    print("Error Rate: ", np.mean(error_list)*100)
    print("Precision: ", np.mean(final_prec)*100)
    print("Recall: ", np.mean(final_rec)*100)
    print("F1-Score: ", np.mean(final_f1)*100)
    print("AUC: ", np.mean(final_auc)*100)
    print(f"K = {v} \n")
    error_dataset.append(np.mean(error_list)*100)
    f1_dataset.append(np.mean(final_f1)*100)
    acc_dataset.append(np.mean(acc_list)*100)
    auc_dataset.append(np.mean(final_auc)*100)
            
#K = 6 has the highest validation accuracy

#E:\Python\Python39\lib\site-packages\sklearn\metrics\_classification.py
   

#trainmodel
# actuals = np.array(testLabel)
# error_rate = []
# f1_rate = []
# acc_rate = []  
# for n_neighbors in range(1,100):
#     knn = KNeighborsClassifier(n_neighbors, p=2, weights='uniform')
#     knn.fit(data, labeldata)
#     predictions = list(knn.predict(testData))
#     accuracy = knn.score(testData, testLabel)
#     conf_matrix = confusion_matrix(y_true=testLabel, y_pred=predictions)
#     pred = np.array(predictions)
#     error_rate.append(np.mean(pred != actuals))
#     acc_rate.append(accuracy)
#     f1_rate.append(f1_score(testLabel,predictions))
#     print('K = ',n_neighbors)
#     print('Accuracy: %.3f' % accuracy)
#     print('Precision: %.3f' % precision_score(testLabel,predictions))
#     print('F1 Score: %.3f' % f1_score(testLabel,predictions))
#     print('Error rate: %.3f \n' % np.mean(pred != actuals))
    
        
# #testmodel
# knn = KNeighborsClassifier(n_neighbors=6, p=2, weights='uniform')
# knn.fit(data, labeldata)
# predictions = list(knn.predict(testData))
# accuracy = knn.score(testData, testLabel)*100
# precision = precision_score(testLabel,predictions)*100
# f1 = f1_score(testLabel,predictions)*100
# conf_matrix = confusion_matrix(y_true=testLabel, y_pred=predictions)
# print('Total: ',len(stressed)+len(not_stressed))
# print('Stress: ',len(stressed))
# print('Not_Stress: ',len(not_stressed))
# print(f'Actuals     {testLabel}')
# print(f'Predictions {predictions}')
# print('Accuracy: %.3f' % accuracy)
# print('Precision: %.3f' % precision)
# print('F1 Score: %.3f' % f1)
# ## savemodel
# # knnPickle = open('server\knnfacemodel.pkl', 'wb') 
# # pickle.dump(knn, knnPickle)  
# # knnPickle.close()
# y_pred_proba = knn.predict_proba(testData)[::,1]
# fpr, tpr, _ = metrics.roc_curve(testLabel,  y_pred_proba)

# plt.plot(fpr,tpr,label="AUC = "+str(round(auc,3))+'\n'+'Threshold = 6')
# plt.xlabel('False Positive Rate (FPR)', fontsize=10)
# plt.ylabel('True Positive Rate (TPR)', fontsize=10)
# plt.legend(loc=4)
# plt.show()

# #confusion matrix
# labels = ['Stress', 'No Stress']
# fig, ax = plt.subplots(figsize=(5, 5))
# ax.matshow(conf_matrix, cmap=plt.cm.Oranges, alpha=0.3)
# for i in range(conf_matrix.shape[0]):
#     for j in range(conf_matrix.shape[1]):
#         ax.text(x=j, y=i,s=conf_matrix[i, j], va='center', ha='center', size='xx-large')
# ax.set_xticklabels([''] + labels)
# ax.set_yticklabels([''] + labels)
# plt.xlabel('Predictions', fontsize=10)
# plt.ylabel('Actuals', fontsize=10)
# plt.title('Confusion Matrix', fontsize=18)
# fig.tight_layout()

# #plot the dataset
# # plt.scatter(frequency, robustness)

# # for i_x, i_y in zip(frequency, robustness):
# #     plt.text(i_x, i_y, '({}, {})'.format(i_x, i_y))


# #plot dataset with labeled points
# # x = np.array(plotdata)
# # y = np.array(labeldata)

x = np.array(plotdata)
y = np.array(labeldata)
z = np.array(predictions)
class_a = np.where(y == 0)
class_b = np.where(y == 1)
class_c = np.where(z == 0)
class_d = np.where(z == 1)
# b = 1.5
# a = 1
# # ax.axline((0,b),slope=a, color='r', linestyle='-', label="Decision Boundy")

# 1 plot
#fig, ax = plt.subplots()
# ax.scatter(x[class_a][:,0],x[class_a][:,1],s=20, c='#eb5974', label="Stress")
# ax.scatter(x[class_b][:,0],x[class_b][:,1],s=20, c='#59a9eb', label="No Stress")
# ax.set_title('Training Dataset', fontsize=25)
# ax.set_xlabel('Frequency', fontsize=25)
# ax.set_ylabel('Robustness', fontsize=25)
# ax.legend(fontsize=20)
# ax.set_xlim(-0.1,1)
# ax.set_ylim(-0.1,0.4)
# ax.tick_params(axis='both', labelsize=15)

# 2 plots
fig, ax = plt.subplots(1,2, figsize=(15,5))
ax[0].scatter(x[class_a][:,0],x[class_a][:,1],s=20,c='y', label="Stress")
ax[0].scatter(x[class_b][:,0],x[class_b][:,1],s=20,c='b', label="No Stress")
ax[0].set_title('Training Dataset', fontsize=18)
ax[0].set_xlabel('Frequency', fontsize=10)
ax[0].set_ylabel('Robustness', fontsize=10)
ax[0].legend()
ax[0].set_xlim(-0.2,1)
ax[0].set_ylim(-0.2,0.5)
ax[1].scatter(x[class_c][:,0],x[class_c][:,1],s=20,c='y', label="Stress")
ax[1].scatter(x[class_d][:,0],x[class_d][:,1],s=20,c='b', label="No Stress")
ax[1].set_title('Predictions', fontsize=18)
ax[1].set_xlabel('Frequency', fontsize=10)
ax[1].set_ylabel('Robustness', fontsize=10)
ax[1].legend()
ax[1].set_xlim(-0.2,1)
ax[1].set_ylim(-0.2,0.5)
fig.tight_layout()

# errorrate plot
plt.figure(figsize=(12,6))
plt.plot(range(2,70),error_dataset,color='#192dff', linestyle='-', 
         marker='o',markerfacecolor='#ff1919', markersize=8)
plt.title('Error Rate vs. K Value', fontsize=25)
plt.xlabel('K', fontsize=20)
plt.ylabel('Error Rate (%)', fontsize=20)
plt.xticks(np.arange(min(range(2,70)), max(range(2,70))+1, 1.0), rotation=60)
plt.tick_params(axis='y', labelsize=15)
print("Minimum error: ",min(error_dataset),"at K =",error_dataset.index(min(error_dataset))+2)
print("Maximum error: ",max(error_dataset),"at K =",error_dataset.index(max(error_dataset))+2)
print("Minimum accuracy: ",min(acc_dataset),"at K =",acc_dataset.index(min(acc_dataset))+2)
print("Maximum accuracy: ",max(acc_dataset),"at K =",acc_dataset.index(max(acc_dataset))+2)
print("Minimum f1 score: ",min(f1_dataset),"at K =",f1_dataset.index(min(f1_dataset))+2)
print("Maximum f1 score: ",max(f1_dataset),"at K =",f1_dataset.index(max(f1_dataset))+2)
plt.tight_layout()
plt.show()

#test with subsample

# print("Average K: ", most_common(k_list))

#test with no subsample
# print("Average Accuracy: ", np.mean(acc_rate)*100)
# print("Average F1-Score: ", np.mean(f1_rate)*100)
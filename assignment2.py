import numpy as np
import csv
from numpy import *
from numpy import linalg
import matplotlib.pyplot as plt
import sys


# trainingset_path = ""
# trainingslabel_path = ""
# testset_path = ""
# testlabel_path = ""
#
# if len(sys.argv) > 1:
#     trainingset_path = sys.argv[1]
# if len(sys.argv) > 2:
#     trainingslabel_path = sys.argv[2]
# if len(sys.argv) > 3:
#     k = int(sys.argv[3])
# if len(sys.argv) > 4:
#     testset_path = sys.argv[4]
# if len(sys.argv) > 5:
#     testlabel_path = sys.argv[5]
#
# faces_train = np.loadtxt(trainingset_path)
# faces_train_label = np.loadtxt(trainingslabel_path)
# faces_test = np.loadtxt(testset_path)
# faces_test_label = np.loadtxt(testlabel_path)


def read_data():
    # train data
    with open('D:/UQ semester2/Data 7703/Assignment 2/faces_train.txt') as csv_file:
        train_data = []
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            row = [int(x) for x in row[:-1]]
            train_data.append(row)

    # faces train labels
    with open('D:/UQ semester2/Data 7703/Assignment 2/faces_train_labels.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for train_label in csv_reader:
            train_label = [int(x) for x in train_label[:-1]]

    # test data
    with open('D:/UQ semester2/Data 7703/Assignment 2/faces_test.txt') as csv_file:
        test_data = []
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            row = [int(x) for x in row[:-1]]
            test_data.append(row)

    # faces test labels
    with open('D:/UQ semester2/Data 7703/Assignment 2/faces_test_labels.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for test_label in csv_reader:
            test_label = [int(x) for x in test_label[:-1]]

    return train_data,train_label,test_data,test_label


# train
faces_train=np.array(read_data()[0])
faces_train_label=np.array(read_data()[1])

# test
faces_test = np.array(read_data()[2])
faces_test_label=np.array(read_data()[3])


# Q1:
def pca(data,k):
    data_mean = np.mean(data,axis = 0)
    T1 = np.cov(data.T)
    D,V = linalg.eigh(T1) #eigenvalue and eigenvector
    V = V[:, ::-1]
    V1 = V[:, :k]#extract the first k eigenvectors

    return None, data_mean, V1


faces_Train, average_face, V = pca(faces_train, 5)
print("the mean face is:\n", average_face.shape)
print("top 5 eigenfaces are:\n", V.shape)

plt.imshow(average_face.reshape((32,32)).T,cmap="gray")
plt.savefig("mean face.jpg")
plt.show()

def showface(eigenfaces):
    array = eigenfaces.T
    plt.figure()
    for i, facevector in enumerate(array):
        plt.subplot(2, 3, i + 1)
        plt.imshow(facevector.reshape((32, 32)).T, cmap="gray")
    plt.savefig("top 5 eigenfaces.jpg")
    plt.show()

print(showface(V))

print("Question 1 completed")


# Q2
the_first_face_test = faces_test[0:1, :]
#print(the_first_face_test)

plt.imshow(the_first_face_test.reshape((32,32)).T,cmap="gray")
plt.savefig("original face.jpg")
plt.show()

def reconstruction(testface,k):
    c = pca(faces_train,k)[2]
    weight = dot(testface - average_face,c)
    return average_face + np.dot(weight, c.T)

Reconstructed1 = reconstruction(the_first_face_test,1)
Reconstructed2 = reconstruction(the_first_face_test,10)
Reconstructed3 = reconstruction(the_first_face_test,50)
Reconstructed4 = reconstruction(the_first_face_test,100)

plt.imshow(Reconstructed1.reshape((32,32)).T,cmap="gray")
plt.savefig("k=1.jpg")
plt.show()
plt.imshow(Reconstructed2.reshape((32,32)).T,cmap="gray")
plt.savefig("k=5.jpg")
plt.show()
plt.imshow(Reconstructed3.reshape((32,32)).T,cmap="gray")
plt.savefig("k=20.jpg")
plt.show()
plt.imshow(Reconstructed4.reshape((32,32)).T,cmap="gray")
plt.savefig("k=100.jpg")
plt.show()

print("Question 2 completed")


#Q3
def euclideanDistance(instance1, instance2):
    distance = 0
    for x in range(len(instance1)-1):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def knn1(ds_train,label_train,ds_test):
    result=[]
    for vec in ds_test:
        knn_array=[]
        label=[]
        for i in range(len(ds_train)):
            distance= euclideanDistance(vec,ds_train[i])
            knn_array.append(distance)
            label.append(label_train[i])
        dis_min=min(knn_array)
        min_index=knn_array.index(dis_min)
        result.append(label[min_index])

    result=np.array(result)
    result=result.astype(int)
    return result


def accuracy(predict, test_y):
    test_y = np.array(test_y)
    test_y = test_y.astype(int)
    correct = 0
    for i in range(len(test_y)):
        if predict[i] == test_y[i]:
            correct = correct + 1
    accuracy = correct / float(len(test_y))
    return accuracy

k_array = []
for i in range(1,101):
    k_array.append(i)

accuracy_array = []
for k in k_array:
    train_centered = faces_train - average_face
    C = pca(train_centered, k)[2]  # shape(1024,k)
    train_norm_lowmat = dot(train_centered, C)

    test_centered = faces_test - average_face
    test_norm_lowmat = dot(test_centered, C)
    predict_y = knn1(train_norm_lowmat, faces_train_label, test_norm_lowmat)
    accuracy_array.append(accuracy(predict_y, faces_test_label))

print(k_array)
print(accuracy_array)
plt.plot(k_array, accuracy_array)
plt.savefig("predict accuracy.jpg")
plt.show()

print("Question 3 completed")

# Q4
def error_classify():
    test_data_recons = reconstruction(faces_test, 100)
    # results = nn(train_data, train_label, test_data_recons)
    for i in range(test_data_recons.shape[0]):
        distances = [euclideanDistance(test_data_recons[i], train) for train in faces_train]
        nearest = np.argsort(-np.array(distances))[-1]
        nearest_label = faces_train_label[nearest]

        if nearest_label != faces_test_label[i]:
            f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
            # plt.imshow(data.reshape(size,size).T,cmap="gray")
            ax1.imshow(test_data_recons[i].reshape(32,32).T,cmap="gray")
            ax1.set_title(str(nearest_label))
            ax2.imshow(faces_train[nearest].reshape(32,32).T,cmap="gray")
            ax2.set_title(str(faces_test_label[i]))
            plt.savefig(str(i))

print(error_classify())

print("Question 4 completed")


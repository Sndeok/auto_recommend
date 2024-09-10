import numpy as np
B={0:{2:17,3:31},1:{3:5},3:{1:14}}
# B=np.array(AA)
print(max(B.keys()))
max1=max(B.keys())
max2=0
for i in B:
   if max2<max(B[i].keys()):
       max2=max(B[i].keys())
print(max2)
shape_B=(max1+1,max2+1)
B_array=np.zeros(shape_B)
for i in B:
    for j in B[i]:
        B_array[i][j]=B[i][j]
print(B_array)
shape_A=(4,5)
A=np.random.random(shape_A)
print(A)
shape_x=(5,6)
x=np.random.random(shape_x)
shape_re=(4,6)
result=np.zeros(shape_re,dtype=np.float)
for i in range(0,shape_A[0]):
    for k in range(0, shape_x[1]):
        temp_result = 0.0
        for j in range(0,shape_A[1]):
            temp_result=temp_result+A[i][j]*x[j][k]
        result[i][k]=temp_result
print(result)
print(np.dot(A,x))
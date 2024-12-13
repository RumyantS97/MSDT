# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 11:09:20 2021

@author: ankokkk
"""
"""
#The code runs rather slow as no library is used for matrix multiplication. 
#For this reason, I added the matmul function to the marked places.
#If you want, you can activate the comment line and run the code without using matmul.
"""


import numpy as np
import random

class LogisticRegression:
    def __init__(self, learning_rate, epochs, batch_size):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        self.w0 = [0]*784
        self.w1 = [0]*784
        self.w2 = [0]*784
        self.w3 = [0]*784
        self.w4 = [0]*784
        self.w5 = [0]*784
        self.w6 = [0]*784
        self.w7 = [0]*784
        self.w8 = [0]*784
        self.w9 = [0]*784

    def fit(self, X, y):
        b = []
        rand_indices = []
        for i in range(10):
            b.append(i)
            b[i] = random.uniform(-0.5,0.5)
            
        for i in range(60000):
                rand_indices.append(i)    
        for i in range(784): #Inital value
            self.w0[i] = random.uniform(-0.1,0.1)
            self.w1[i] = random.uniform(-0.1,0.1)
            self.w2[i] = random.uniform(-0.1,0.1)
            self.w3[i] = random.uniform(-0.1,0.1)
            self.w4[i] = random.uniform(-0.1,0.1)
            self.w5[i] = random.uniform(-0.1,0.1)
            self.w6[i] = random.uniform(-0.1,0.1)
            self.w7[i] = random.uniform(-0.1,0.1)
            self.w8[i] = random.uniform(-0.1,0.1)
            self.w9[i] = random.uniform(-0.1,0.1)
        
        for epoch in range(self.epochs):#Epoch
            num_batch = int(X.shape[0]/self.batch_size)
            batch_loss100 = 0
            random.shuffle(rand_indices)#random value for batch
            
            for batch in range(num_batch):
                index = rand_indices[(self.batch_size*batch):(self.batch_size*(batch+1))]
                x_batch = X[index]
                y_batch = y[index]
                #Gradient Mini Batch, partial derivative
                dw0,dw1,dw2,dw3,dw4,dw5,dw6,dw7,dw8,dw9, db, batch_loss = self.GMB(b, x_batch, y_batch) 
                batch_loss100 += batch_loss#loss

                for i in range(10):
                        b[i] -= self.learning_rate* db[i]
                #Update w and b with learning rate and dw        
                for i in range(784):
                    self.w0[i] -= self.learning_rate * dw0[i]
                    self.w1[i] -= self.learning_rate * dw1[i]
                    self.w2[i] -= self.learning_rate * dw2[i]
                    self.w3[i] -= self.learning_rate * dw3[i]
                    self.w4[i] -= self.learning_rate * dw4[i]
                    self.w5[i] -= self.learning_rate * dw5[i]
                    self.w6[i] -= self.learning_rate * dw6[i]
                    self.w7[i] -= self.learning_rate * dw7[i]
                    self.w8[i] -= self.learning_rate * dw8[i]
                    self.w9[i] -= self.learning_rate * dw9[i]
                
                if batch % 100 == 0:
                    message = 'Epoch %d, Batch %d, Loss %.2f' % (epoch+1, batch, batch_loss)
                    print(message)
                    batch_loss100 = 0

            
    def predict(self,X):
          dist = [0]*X.shape[0]#Test size
          
          for i in range(X.shape[0]):
              dist0 = [0]*10
              
              #For work faster np.malmut
              """
              for k in range(784):#Matrix Mult
                  dist0[0] += X[i][k]*self.w0[k]
                  dist0[1] += X[i][k]*self.w1[k]
                  dist0[2] += X[i][k]*self.w2[k]
                  dist0[3] += X[i][k]*self.w3[k]
                  dist0[4] += X[i][k]*self.w4[k]
                  dist0[5] += X[i][k]*self.w5[k]
                  dist0[6] += X[i][k]*self.w6[k]
                  dist0[7] += X[i][k]*self.w7[k]
                  dist0[8] += X[i][k]*self.w8[k]
                  dist0[9] += X[i][k]*self.w9[k] 
              """#**************************
              dist0[0] = np.matmul(X[i], self.w0)
              dist0[1] = np.matmul(X[i], self.w1)
              dist0[2] = np.matmul(X[i], self.w2)
              dist0[3] = np.matmul(X[i], self.w3)
              dist0[4] = np.matmul(X[i], self.w4)
              dist0[5] = np.matmul(X[i], self.w5)
              dist0[6] = np.matmul(X[i], self.w6)
              dist0[7] = np.matmul(X[i], self.w7)
              dist0[8] = np.matmul(X[i], self.w8)
              dist0[9] = np.matmul(X[i], self.w9)
             #******************************
              dist1 = self.Softmax(dist0)    
              maxvaldist = max(dist1)
              maxindex = 0
            
              for l in range(10):
                  if(dist1[l] == maxvaldist):
                      maxindex = l
                    
              dist[i] = maxindex#finding max value in prob
         
          print(i/10000*100)
          print("******************************************************")
  
          return dist                
    
    def GMB(self,b,x_batch,y_batch):
        w_gradl0 = [0]*784
        w_gradl1 = [0]*784
        w_gradl2 = [0]*784
        w_gradl3 = [0]*784
        w_gradl4 = [0]*784
        w_gradl5 = [0]*784
        w_gradl6 = [0]*784
        w_gradl7 = [0]*784
        w_gradl8 = [0]*784
        w_gradl9 = [0]*784  
        b_gradl = [0]*10
        dw0 = [0]*784
        dw1 = [0]*784
        dw2 = [0]*784
        dw3 = [0]*784
        dw4 = [0]*784
        dw5 = [0]*784
        dw6 = [0]*784
        dw7 = [0]*784
        dw8 = [0]*784
        dw9 = [0]*784
        db = [0]*10
        batch_loss = 0
        batch_size = x_batch.shape[0]
    
        for j in range(batch_size):#Minibatch 
       
            w_grad = [0]*10
            b_grad = [0]*10
            w_grad0 = [0]*784
            w_grad1 = [0]*784
            w_grad2 = [0]*784
            w_grad3 = [0]*784
            w_grad4 = [0]*784
            w_grad5 = [0]*784
            w_grad6 = [0]*784
            w_grad7 = [0]*784
            w_grad8 = [0]*784
            w_grad9 = [0]*784
            pred = [0]*10
            x,y = x_batch[j], y_batch[j]
            x = x.reshape((784,1))
            E = [0]*10
            yi = int(y)
            E[yi] = 1 
            #For work faster np.matmul ********
            pred[0] = np.matmul(self.w0, x)
            pred[1] = np.matmul(self.w1, x)
            pred[2] = np.matmul(self.w2, x)
            pred[3] = np.matmul(self.w3, x)
            pred[4] = np.matmul(self.w4, x)
            pred[5] = np.matmul(self.w5, x)
            pred[6] = np.matmul(self.w6, x)
            pred[7] = np.matmul(self.w7, x)
            pred[8] = np.matmul(self.w8, x)
            pred[9] = np.matmul(self.w9, x)
            """**********************
            for i in range (784):  #Matrix Mult.        
                pred[0] += x[i]*self.w0[i]
                pred[1] += x[i]*self.w1[i]
                pred[2] += x[i]*self.w2[i]
                pred[3] += x[i]*self.w3[i]
                pred[4] += x[i]*self.w4[i]
                pred[5] += x[i]*self.w5[i]
                pred[6] += x[i]*self.w6[i]
                pred[7] += x[i]*self.w7[i]
                pred[8] += x[i]*self.w9[i]
                pred[9] += x[i]*self.w9[i]
           """       
            for i in range(10):
               pred[i]+= b[i]
            

            pred = self.Softmax(pred)
            loss = self.loss(pred,y)
            batch_loss += loss

            for i in range(10):
                w_grad[i] = (E[i] - pred[i])   
                b_grad[i] = ((-(E[i] - pred[i])))
                b_gradl[i] += b_grad[i]   
            #Gradient calculating
            #For work faster np.matmul****************
            w_grad0 = -np.matmul(w_grad[0],x.reshape((1,784)))
            w_gradl0 += w_grad0
            w_grad1 = -np.matmul(w_grad[1],x.reshape((1,784)))
            w_gradl1 += w_grad1
            w_grad2 = -np.matmul(w_grad[2],x.reshape((1,784)))
            w_gradl2 += w_grad2
            w_grad3 = -np.matmul(w_grad[3],x.reshape((1,784)))
            w_gradl3 += w_grad3
            w_grad4 = -np.matmul(w_grad[4],x.reshape((1,784)))
            w_gradl4 += w_grad4
            w_grad5 = -np.matmul(w_grad[5],x.reshape((1,784)))
            w_gradl5 += w_grad5
            w_grad6 = -np.matmul(w_grad[6],x.reshape((1,784)))
            w_gradl6 += w_grad6
            w_grad7 = -np.matmul(w_grad[7],x.reshape((1,784)))
            w_gradl7 += w_grad7
            w_grad8 = -np.matmul(w_grad[8],x.reshape((1,784)))
            w_gradl8 += w_grad8
            w_grad9 = -np.matmul(w_grad[9],x.reshape((1,784)))
            w_gradl9 += w_grad9
            """****************************
            for i in range(784):#Matrix Mult. 
               w_grad0[i] = -(w_grad[0]*x[i])
               w_gradl0[i] += w_grad0[i]
               w_grad1[i] = -(w_grad[1]*x[i])
               w_gradl1[i] += w_grad1[i]
               w_grad2[i] = -(w_grad[2]*x[i])
               w_gradl2[i] += w_grad2[i]
               w_grad3[i] = -(w_grad[3]*x[i])
               w_gradl3[i] += w_grad3[i]
               w_grad4[i] = -(w_grad[4]*x[i])   
               w_gradl4[i] += w_grad4[i]
               w_grad5[i] = -(w_grad[5]*x[i])
               w_gradl5[i] += w_grad5[i]
               w_grad6[i] = -(w_grad[6]*x[i])
               w_gradl6[i] += w_grad6[i]
               w_grad7[i] = -(w_grad[7]*x[i])
               w_gradl7[i] += w_grad7[i]
               w_grad8[i] = -(w_grad[8]*x[i])
               w_gradl8[i] += w_grad8[i]
               w_grad9[i] = -(w_grad[9]*x[i]) 
               w_gradl9[i] += w_grad9[i]
           """
        #np.matmul work faster. If you activate the part in the comment, it will work without matmul.******   
        dw0 = (w_gradl0/self.batch_size)
        dw1 = (w_gradl1/self.batch_size)
        dw2 = (w_gradl2/self.batch_size)
        dw3 = (w_gradl3/self.batch_size)
        dw4 = (w_gradl4/self.batch_size)
        dw5 = (w_gradl5/self.batch_size)
        dw6 = (w_gradl6/self.batch_size)
        dw7 = (w_gradl7/self.batch_size)
        dw8 = (w_gradl8/self.batch_size)
        dw9 = (w_gradl9/self.batch_size)   
        #Update dw values
        """   ************************
        for i in range(784):    
            dw0[i] = (w_gradl0[i]/self.batch_size)
            dw1[i] = (w_gradl1[i]/self.batch_size)
            dw2[i] = (w_gradl2[i]/self.batch_size)
            dw3[i] = (w_gradl3[i]/self.batch_size)
            dw4[i] = (w_gradl4[i]/self.batch_size)
            dw5[i] = (w_gradl5[i]/self.batch_size)
            dw6[i] = (w_gradl6[i]/self.batch_size)
            dw7[i] = (w_gradl7[i]/self.batch_size)
            dw8[i] = (w_gradl8[i]/self.batch_size)
            dw9[i] = (w_gradl9[i]/self.batch_size)
            ************************
        """    
        for i in range(10):
            db[i] = (b_gradl[i]/self.batch_size) 
        #Update db value
        return dw0,dw1,dw2,dw3,dw4,dw5,dw6,dw7,dw8,dw9, db, batch_loss

    def ln(self,x):#for np.log
        n = 1000.0
        return n * ((x ** (1/n)) - 1)
    
    def Softmax(self, z):
        #np.malmut situation for exp scalar so i added.
        prob = [0]*10
        exp = [0]*10
        e = 2.718
        for i in range(10):
            exp[i] = pow(e,z[i])
    
        for i in range(10):
            prob[i] = 1/sum(exp) * exp[i]
      
        return prob
    
    def loss(self, pred, y):#Cross entrpy loss

        l = -(self.ln(pred[int(y)])/self.ln(10))

        return l
#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd


# In[109]:


dict = {'name':['rohit','Renu','krishnavi','mohan',
               'Prajakta'],
'marks':[65,67,78,79],
'city':['dhamnod','indore','delhi','goa']}


# In[110]:


df= pd.DataFrame(dict)


# In[107]:


df


# In[12]:


df.to_csv('test.csv')


# In[13]:


df.head(2)


# In[15]:


df.tail(2)


# In[17]:


df.describe()


# In[19]:


df1 = pd.read_csv('test.csv')


# In[37]:


df1


# In[21]:


df1.marks[0]=90


# In[22]:


df1


# In[23]:


df2 = pd.read_csv('friend.csv')


# In[24]:


df2


# In[26]:


df3 = df2.merge(df1)


# In[29]:


df2


# In[30]:


df2.index = ['a','b','c','d']


# In[31]:


df2


# In[32]:


df3 = pd.DataFrame(np.random.rand(5,5))


# In[34]:


df3


# In[35]:


type(df3)


# In[36]:


df3.dtypes


# In[38]:


df1.dtypes


# In[40]:


df2.dtypes


# In[41]:


df1.index


# In[43]:


df1.columns


# In[44]:


df3.index


# In[45]:


df3.columns


# In[47]:


df3.sort_index(axis = 1 ,ascending = False)                                  #axis 0 for and axis 1 for column


# In[49]:


df1



# In[55]:


df1['name'][3]='Rahul'


# In[57]:


df1


# In[58]:


df1.loc[0,'city']                            #loc function is used to access the particular element from the data frame loc[row,column]


# In[62]:


df1.loc[[1,2],['name','city']]


# In[75]:


df3 = df1.merge(df2,how='inner',on='name')             #merge is used to join two dataframe in pandas


# In[76]:


df3


# In[79]:


df1.loc[0:]


# In[81]:


df2.loc[:'city']


# In[85]:


df2.loc[(df2['name']=='rohit')&(df2['city']=='lahore')]  #so we can use loc function to apply certain condition and get the output


# In[96]:


df3.drop('marks_y',axis=1)                              #drop used to delete any column and column 


# In[98]:


df3.drop(0,axis=0)   


# In[101]:


df2.reset_index(drop= False)     #reset index is used to reset the index if use drop = True index column willbe removed


# In[115]:


df['marks'].isnull()      #is null is used to check the null values in pandas


# In[117]:


df.isnull()


# In[119]:


df.dropna()       #it is used to drop na 


# In[121]:


df.shape        # it is used to check the structure how many rows and how many columns


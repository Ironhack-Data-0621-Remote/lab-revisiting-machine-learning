#!/usr/bin/env python
# coding: utf-8

# # Lab | Revisiting Machine Learning Case Study

# In this lab, you will use learningSet.csv file which you already have cloned in today's activities.

# In[1]:


import pandas as pd
import warnings
warnings.filterwarnings('ignore')


# In[2]:


data = pd.read_csv("/Users/silvia/Downloads/learningSet.csv")


# ### 1. Check for null values in all the columns

# In[3]:


def check_for_nulls(df):
    nulls_total = []
    columns = []
    for c in df.columns:
        nulls = (int(df[c].isnull().sum()) / int(len(df[c])))*100
        if nulls > 0:
            nulls_total.append(nulls)
            columns.append(c)      
    nulls_dict = dict(zip(columns,nulls_total))
    nulls_df = pd.DataFrame([nulls_dict]).transpose()
    nulls_df.columns = ['n_nulls']
    nulls_df = nulls_df.sort_values(by = ['n_nulls'], ascending = [False])
    return nulls_df


# In[4]:


check_for_nulls(data)


# ### 2. Exclude the following variables by looking at the definitions. Create a new empty list called drop_list. We will append this list and then drop all the columns in this list later:
# 
# - `OSOURCE` - symbol definitions not provided, too many categories
# - `ZIP CODE` - we are including state already
# 

# In[7]:


drop_list = ['OSOURCE', 'ZIP CODE']


# ### 3. Identify columns that over 85% missing values

# In[8]:


nulls = check_for_nulls(data)
More_85 = nulls[nulls['n_nulls']>85]
More_85


# ### 4. Remove those columns from the dataframe

# In[10]:


drop_columns = []
for c in More_85.index:
    drop_columns.append(c)
data = data.drop(drop_columns, axis=1)


# ### 5. Reduce the number of categories in the column GENDER. The column should only have either "M" for males, "F" for females, and "other" for all the rest
# 
# Note that there are a few null values in the column. We will first replace those null values using the code below:
# 
# ```python
# print(categorical['GENDER'].value_counts())
# categorical['GENDER'] = categorical['GENDER'].fillna('F')
# ```

# In[11]:


print(data['GENDER'].value_counts())
data['GENDER'] = data['GENDER'].fillna('F')


# In[12]:


data['GENDER'] = data['GENDER'].replace([' ', 'C', 'U', 'J', 'A'], "other")


# In[13]:


data['GENDER'].unique()


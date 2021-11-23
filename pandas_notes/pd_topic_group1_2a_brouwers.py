# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.12.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

#
# ## Provided by:
#
#  __Ahmad Shirazi__<br>
#  __Shirazi@umich.edu__
#  
#
# ## Topic:
#  
# Using <font color=red>glob module</font> to create a data frame from multiple files, row wise:

# +
import pandas as pd
from glob import glob


# - We can read each dataframe from its own CSV file, combine them together and delet the original dataframes. <br>
# - This will need a lot of code and will be memory and time consuming.<br>
# - A better solution is to use the built in glob module.<br>
# - Lets make example dataframes in the next cell.<br>

# +
# making 3 dataframes as inputs for our example
data_age1 = pd.DataFrame({'Name':['Tom', 'Nick', 'Krish', 'Jack'],
        'Age':[17, 31, 28, 42]})

data_age2 = pd.DataFrame({'Name':['Kenn', 'Adam', 'Joe', 'Alex'],
        'Age':[20, 21, 19, 18]})

data_age3 = pd.DataFrame({'Name':['Martin', 'Jenifer', 'Roy', 'Mike'],
        'Age':[51, 30, 38, 25]})

# Saving dataframes as CSV files to be used as inputs for next example
data_age1.to_csv('data_age1.csv', index=False)
data_age2.to_csv('data_age2.csv', index=False)
data_age3.to_csv('data_age3.csv', index=False)


# - We pass a patern to the glob (including wildcard characters)
# - It will return the name of all files that match that pattern in the data subdirectory.
# - We can then use a generator expression to read each file and pass the results to the concat function.
# - It will concatenate the rows for us to a single dataframe.
# -

students_age_files = glob('data_age*.csv')
students_age_files

pd.concat((pd.read_csv(file) for file in students_age_files), ignore_index=True)


# ## Concatenate 
# *Dingyu Wang*
#
# wdingyu@umich.edu

# ## Concatenate 
# + Concatenate pandas objects along a particular axis with optional set logic
# along the other axes.
# + Combine two Series.

import pandas as pd

s1 = pd.Series(['a', 'b', 'c'])
s2 = pd.Series(['d', 'e', 'f'])
pd.concat([s1, s2])

# ## Concatenate 
# * Concatenate pandas objects along a particular axis with optional set logic
# along the other axes.
# * Combine two Series.
# * Combine two DataFrame objects with identical columns.

df1 = pd.DataFrame([['a', 1], ['b', 2], ['c', 3]],
                   columns=['letter', 'number'])
df2 = pd.DataFrame([['d', 4], ['e', 5], ['f', 6]],
                   columns=['letter', 'number'])
pd.concat([df1, df2])

# ## Concatenate 
# * Concatenate pandas objects along a particular axis with optional set logic
# along the other axes.
# * Combine two Series.
# * Combine two DataFrame objects with identical columns.
# * Combine DataFrame objects with overlapping columns and return only those
# that are shared by passing inner to the join keyword argument
# (default outer).

df3 = pd.DataFrame([['a', 1, 'Mary'], ['b', 2, 'John'], ['c', 3, 'James']],
                   columns=['letter', 'number', 'name'])
pd.concat([df1, df3])
pd.concat([df1, df3], join='inner')

# ## Concatenate 
# * Concatenate pandas objects along a particular axis with optional set logic
# along the other axes.
# * Combine two Series.
# * Combine two DataFrame objects with identical columns.
# * Combine DataFrame objects with overlapping columns and return only those
# that are shared by passing in `join=inner`(default outer).
# * Combine DataFrame objects horizontally along the x axis by passing in
# `axis=1`(default 0).

df4 = pd.DataFrame([['Tom', 24], ['Jerry', 18], ['James', 22]],
                   columns=['name', 'age'])
pd.concat([df1, df4])
pd.concat([df1, df4], axis=1)

# # Sparse Data Structures - falarcon@umich.edu
#
# Felipe Alarcon Pena

# `pandas` offers a way to speed up not only calculations in the typical `sparse` meaning, i.e. , `DataFrames` with 0's, but also for particular values or `NaN's`.
#
#
# Let's first start showing the effect it has on discarding `NaN's` or a particular values and compare it with other methods. 
#
# The goal of using `sparse` Data Structures is to allocate memory efficiently in large data sets and also speed-up possible operations between `sparse` Data Structures. `Sparse Data Structure` saved values and locations instead of the whole Dataframe. 
#

import pandas as pd
import numpy as np

# +
## Creating toy data.

array_nans = np.random.randn(500, 10000)

# Switching some values to NaN's to produce a sparse structure.
array_nans[10:499,1:9900] = np.nan

dense_df = pd.DataFrame(array_nans)
sparse_df = dense_df.astype(pd.SparseDtype("float", np.nan))

print(" Density of sparse DataFrame: "+str(sparse_df.sparse.density))
# -

# ## Efficiency in storing Sparse DataStructures
#
# `Sparse DataStructures` are more efficient in allocating memory for large datasets with lots of NaN's or information that it is not of interest. The toy data has some sparsity $\sim$ 50%, but real data or matrices could have densities of the orden of $\sim$0.1 % or less.

# +
## Let's compare the storing times for different methods and the same datastructure  being sparse or not.

print('Dense data structure : {:0.3f} bytes'.format(dense_df.memory_usage().sum() / 1e3))
print('Sparse data structure : {:0.3f} bytes'.format(sparse_df.memory_usage().sum() / 1e3))
# -

# Even though the sparse allocate memory better, thy take slightly longer to be created. Nevertheless, we will prove that when there are heavy operations being undertaken in large sparse data structures, the speed-up is worth it, and the allocation of memory as well.

# %timeit  df_2 = pd.DataFrame(array_nans)

# %timeit  sparse_df = pd.DataFrame(array_nans).astype(pd.SparseDtype("float", np.nan))

# ## Speed-up of calculations in Sparse DataStructures and comparison with scipy.
#
# Finally we compare the time it takes to operate on `Dense DataStructures` and `Sparse DataStructures`. Operating directly on `Sparse DataStructures` is not really efficient because `pandas` converts them to `Dense DataStructures` first. Nevertheless the `scipy` package has methods that take advantage of the psarsity of matrices to speed-up those processes.

# +
## scipy also offers methods for sparse arrays, although in the full with 0's meaning,
from scipy.sparse import csr_matrix

rnd_array = np.zeros((10000,500))
rnd_array[200:223,13:26] = np.random.randn(23,13)
sparse_rnd_array = csr_matrix(rnd_array)
sparse_matrix_df = csr_matrix(sparse_df)
# -

# %timeit sparse_matrix_df.dot(sparse_rnd_array)

# %timeit dense_df.dot(rnd_array)

# As we can see `Sparse` methods are specially useful to manage data with repeated values or just values we are not interested in. It can also be used to operate on them using `scipy` and its methods for `sparse` arrays, which could be much faster that standard multiplications. It is important to notice that it is only faster when the sparsity is significant, usually less than 1%.


# ## Topics in Pandas
# **Stats 507, Fall 2021** 

# ## Contents
# + [Pandas Table Visualization](#Pandas-Table-Visualization)
# + [Sorting in Python Pandas](#Sorting-in-Python-Pandas)
# + [Python Classes and Objects](#Python-Classes-and-Objects)

# ## Pandas Table Visualization
# **Author:** Cheng Chun, Chien  
# **Email:**　jimchien@umich.edu  
# [PS6](https://jbhender.github.io/Stats507/F21/ps/ps6.html)

# ## Introduction
# - The slide shows visualization of tabular data using the ***Styler*** class
# - The ***Styler*** creates an HTML table and leverages CSS styling language to control parameters including colors, fonts, borders, background, etc.
# - Following contents will be introduced.
#     1. Formatting Values
#     2. Table Styles
#     3. Bulitin Styles

# ## Formatting Values
# - Styler can distinguish the ***display*** and ***actual*** value
# - To control the display value, use the *.format()* method to manipulate this according to a format spec string or a callable that takes a single value and returns a string.
# - Functions of *.format()*
#     - *precision*: formatting floats
#     - *decimal / thousands*: support other locales
#     - *na_rep*: display missing data
#     - *escape*: displaying safe-HTML or safe-LaTeX

# ## Table Styles
# - Recommend to be used for broad styling, such as entire rows or columns at a time.
# - 3 primary methods of adding custom CSS styles
#     - *.set_table_styles()*: control broader areas of the table with specified internal CSS. Cannot be exported to Excel.
#     - *.set_td_classes()*: link external CSS classes to data cells. Cannot be exported to Excel.
#     - *.apply() and .applymap()*: add direct internal CSS to specific data cells. Can export to Excel.
# - Also used to control features applying to the whole table by generic hover functionality, *:hover*.
# - List of dicts is the format to pass styles to .set_table_styles().

# ## Builtin Styles
# - *.highlight_null*: identifying missing data.
# - *.highlight_min / .highlight_max*: identifying extremeties in data.
# - *.background_gradient*: highlighting cells based or their, or other, values on a numeric scale.
# - *.text_gradient*: highlighting text based on their, or other, values on a numeric scale.
# - *.bar*: displaying mini-charts within cell backgrounds.

import numpy as np
import pandas as pd
# Example of table bar chart
np.random.seed(0)
df = pd.DataFrame(np.random.randn(5,4), columns=['A','B','C','D'])
df.style.bar(subset=['A', 'B'], color='#d65f5f')

# ---
# ---
#

# ## Sorting in Python Pandas
# **Author:** Nuona Chen  
# **Email:** nuona@umich.edu 

#  <h3>DataFrame.sort_values()</h3>
#
#
#
#  <h2>DataFrame.sort_values()</h2>
#  <h3>General Form</h3>
#  <li>DataFrame.sort_values(by, axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last', ignore_index=False, key=None)</li>
#  
#  <h3>What it does</h3>
#  <li>sorts the input DataFrame by values</hi>
#  
#  <h3>Input Parameters</h3>
#   <li>by: name or list of names to sort by</li>
#    <li>axis: 0 -> sort indices, 1 -> sort columns </li>
#    <li>ascending: true -> sort ascending, false -> sort descending</li>
#    <li>inplace: true -> sort in-place </li>
#    <li>kind: sorting algorithm </li>
#    <li>na_position: first -> put NaNs at the beginning, last -> put NaNs at the end</li>
#    <li>ignore_index: true -> label axis as 0, 1,..., n-1</li>
#  
#  <h3>Function Output</h3>
#  <li>The sorted Pandas DataFrame</li>
#  <h4>Reference: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html</h4>

# +
from IPython.core.display import HTML, display
display(HTML('<h2>Example1 - Sort by Columns</h2>'))

data = {"id": [1, 2, 3, 4, 5, 6],
        "gpa": [3.2, 3.7, 3.1, 3.0, 3.7, 3.7],
        "total credit hours": [55, 68, 100, 94, 46, 110],
        "major": ["Statistics", "Anthropology", "Business", "Computer Science", "Business", "Statistics"]}
print("Input DataFrame - ie_data: ")
ie_data = pd.DataFrame(data)
print(ie_data)

display(HTML('<h3>Sort by gpa in an ascending order</h3>'))
display(HTML("<code>ie_data.sort_values(by='gpa', ascending=True)</code>"))

print(ie_data.sort_values(by="gpa", ascending=True))

display(HTML('<h3>Sort by gpa and major in an descending order</h3>'))
display(HTML("<code>ie_data.sort_values(by=['gpa', 'major'], ascending=[False, True])</code>"))

print(ie_data.sort_values(by=["gpa", "major"], ascending=[False, True]))
display(HTML('<p>The order of variables in the by statement is the order of sorting. Major is sorted after gpa is sorted.</p>'))

display(HTML('<h2>Example2 - Sort by Rows</h2>'))

del ie_data["major"]
print("Input DataFrame - ie_data: ")
print(ie_data)
display(HTML('<h3>Sort by the row with index = 4 in an descending order</h3>'))
display(HTML("<code>ie_data.sort_values(by=4, axis=1, ascending=False)</code>"))

ie_data.sort_values(by=4, axis=1, ascending=False)


# -

# ---
# ---
#

# ## Python Classes and Objects
#
# **Name:** Benjamin Osafo Agyare  
# **UM email:** bagyare@umich.edu  
#

# ## Overview
#   - [Python classes](#Python-classes)
#   - [Creating a Class data](#Creating-a-Class)
#   - [The __init__() Function](#The-__init__()-Function)
#   - [Object Methods and the self operator](#Object-Methods-and-the-self-operator)
#   - [Modifying and Deleting objects](#Modifying-and-Deleting-objects)

# ## Python classes
# - Python is an object oriented programming language.
# - Almost everything in Python is an object, with its properties and methods.
# - A Class is like an object constructor, or a "blueprint" for creating objects.

# ## Python classes
# - Some points on Python class:
#   + Classes are created by keyword class.
#   + Attributes are the variables that belong to a class.
#   + Attributes are always public and can be accessed using the dot (.) operator. Eg.: Myclass.Myattribute

# ## Creating a Class
# - To create a class in python, use the reserved keyword `class`
#
# ### Example
# - Here is an example of creating a class named Student, with properties name, school and year:

class Student:
    school = "U of Michigan"
    year = "freshman"


# ## The __init__() Function
#
# - To make better meaning of classes we need the built-in `__init__()` function.
# - The `__init__()` is used function to assign values to object properties, or other operations that are necessary to do when the object is being created.
# - All classes have this, which is always executed when the class is being initiated.

# +
class Student:
    def __init__(self, name, school, year):
        self.name = name
        self.school = school
        self.year = year

person1 = Student("Ben", "University of Michigan", "freshman")
print(person1.name)
print(person1.school)
print(person1.year)


# -

# ## Object Methods and the self operator
# - Objects in python can also have methods which are functions that belong to the object

# ## Object Methods and the self operator
# - The self parameter
#   + The self parameter `self` in the example above references the current state of the class.
#   + It can be used to access the variables that belong to the class.
#   + You can call it whatever you like but has to be the first parameter of any function in a class

# ## Example

# +
class Student:
    def __init__(myself, name, school, year):
        myself.name = name
        myself.school = school
        myself.year = year

    def getAttr(person):
        print("Hi, I'm " + person.name + " and a "
              + person.year + " at " + person.school)


person2 = Student("Ben", "University of Michigan", "freshman")
person2.getAttr()
# -

# ## Modifying and Deleting objects
# - You can modify object properties
# - It is also possible to delete properties objects using the `del` keyword and same can be used to delete the object itself

# ## Example

# +
## Modify object properties
person2.year = "senior"

## Delete properties of objects
del person2.name

## Delete object
del person2
# -

# ## References:
# - [https://www.w3schools.com/python](https://www.w3schools.com/python)
# - [https://www.geeksforgeeks.org/python-classes-and-objects/](https://www.geeksforgeeks.org/python-classes-and-objects/)
# - [https://www.tutorialspoint.com/python3](https://www.tutorialspoint.com/python3)

# ---
# ---


import pandas as pd
import numpy as np
import random

# **Stan Brouwers** *brouwers@umich.edu*

# # Pandas, write to LaTeX
#
# - Pandas function.
# - Can write dataframe to LaTeX table.
# - Helpful when writing reports.
# - Easy to call.
#

# # A first example
#
# - Multiple ways to call the function.
# - Selecting certain parts of a dataframe also possible.
# - Column names and indices are used to label rows and columns.

# Generate some data.
data = pd.DataFrame([[random.randint(1,10) for columns in range(5)] for rows in range(5)])
print(data.to_latex())

# # Another example
#
# - Table can be written to a file. (buf input)
# - Subset of columns can be chosen.
#     - Using list of column names.

data.to_latex(buf='./test.doc')
# Only printing certain columns
print(data.to_latex(columns=[0, 4]))

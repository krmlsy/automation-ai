import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier



def predict_elements(test):

    ### CURRENT ELEMENTS OPERATIONS START
    # reading the required files into python using pandas 
    df = pd.read_csv('selenium.with.ai/data/current_page_elements.csv' , encoding="UTF-8")
    ##test = pd.read_csv('selenium.with.ai/data/testElementAttributes.csv',encoding="UTF-8")
    # Fill the NaN values with 'None'
    df = df.fillna('None')
    # now since our machine learning model can only understand numeric values we'll have to convert the strings to numbers/indicator variables
    X_train = pd.get_dummies(df.drop('element',axis=1))
    # returns all the unique Elements stored in the training data
    df['element'].unique()
    # creating a dictionary of elements 
    element_dict = dict(zip(df['element'].unique(), range(df['element'].nunique())))
    #>>>{'_token': 0, 'email': 1, 'password': 2, 'LOGIN': 3, 'on': 4}
    # replacing dictionary values into dataframe as we meed to convert this into numbers
    y_train = df['element'].replace(element_dict)
    # Now we need to train our model , we can prefer any model which provides accurate results - Random Forest Model
    ### CURRENT ELEMENTS OPERATIONS FINISH

    rf = RandomForestClassifier(n_estimators=100, random_state=0)
    rf.fit(X_train, y_train)
    num_of_records = len(test)
    test_ = test.fillna('None')
    concatenated = pd.concat([df, test_], axis=0).drop('element',     axis=1)
    if num_of_records == 1:
        processed_test = pd.DataFrame(pd.get_dummies(concatenated).iloc[-num_of_records]).T

        ## EDIT : we need to remove the changed different attribute value from data frame

        if len(processed_test.columns) > len(X_train.columns):
            df_diffs = list(set(processed_test.columns) - set(X_train.columns))
            processed_test.drop(df_diffs, axis="columns", inplace=True)

        # EDIT FINISH

        probabilites = list(rf.predict_proba(processed_test)[0])
        element_name = list(element_dict.keys())[np.argmax(probabilites)]
        #element_name = 'Hence, the name of our predicted element is {}'.format(element_name)
        score = list(zip(df['element'].unique(), probabilites))

    elif num_of_records > 1:
        processed_test = pd.get_dummies(concatenated).iloc[-num_of_records:]
        probabilites = list(rf.predict_proba(processed_test))

        score = []
        for i in range(len(probabilites)):
            score.append(list(zip(df['element'].unique(), list(probabilites[i]))))

        element_index = np.argmax(probabilites, axis=1)
        element_name = []
        for ind_, i in enumerate(element_index):
            element_name.append(
                (ind_, 'Hence, the name of our predicted element is {}'.format(list(element_dict.keys())[i])))
    return score, element_name, test

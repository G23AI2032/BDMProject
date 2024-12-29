import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import warnings
warnings.filterwarnings("ignore")

# Read the data
train = pd.read_csv("train_u6lujuX_CVtuZ9i.csv")
test = pd.read_csv("test_Y3wMUE5_7gLdaTN.csv")

# Concatenate train and test data for preprocessing
data = pd.concat([train, test])

# Drop unwanted column
data.drop('Loan_ID', inplace=True, axis='columns')

# Impute missing values
data['Gender'].fillna(data['Gender'].mode()[0], inplace=True)
data['Married'].fillna(data['Married'].mode()[0], inplace=True)
data['Dependents'].fillna(data['Dependents'].mode()[0], inplace=True)
data['Self_Employed'].fillna(data['Self_Employed'].mode()[0], inplace=True)
data['Credit_History'].fillna(data['Credit_History'].mode()[0], inplace=True)

# Use Iterative imputer for LoanAmount and Loan_Amount_Term
data1 = data.loc[:, ['LoanAmount', 'Loan_Amount_Term']]
imp = IterativeImputer(RandomForestRegressor(), max_iter=1000, random_state=0)
data1 = pd.DataFrame(imp.fit_transform(data1), columns=data1.columns)

data['LoanAmount'] = data1['LoanAmount']
data['Loan_Amount_Term'] = data1['Loan_Amount_Term']

# Map categorical variables
data['Gender'] = data['Gender'].map({'Male': 0, 'Female': 1}).astype(int)
data['Married'] = data['Married'].map({'No': 0, 'Yes': 1}).astype(int)
data['Education'] = data['Education'].map({'Not Graduate': 0, 'Graduate': 1}).astype(int)
data['Self_Employed'] = data['Self_Employed'].map({'No': 0, 'Yes': 1}).astype(int)
data['Credit_History'] = data['Credit_History'].astype(int)
data['Property_Area'] = data['Property_Area'].map({'Urban': 0, 'Rural': 1, 'Semiurban': 2}).astype(int)
data['Dependents'] = data['Dependents'].map({'0': 0, '1': 1, '2': 2, '3+': 3})

# Create new feature
data['Total_Income'] = data['ApplicantIncome'] + data['CoapplicantIncome']
data.drop(['ApplicantIncome', 'CoapplicantIncome'], axis='columns', inplace=True)

# Split back into train and test
new_train = data.iloc[:614]
new_test = data.iloc[614:]

# Map loan status
new_train['Loan_Status'] = new_train['Loan_Status'].map({'N': 0, 'Y': 1}).astype(int)

# Create X and y
X = new_train.drop('Loan_Status', axis='columns')
y = new_train['Loan_Status']

# Split training data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=3)

# Train Random Forest model
rfc = RandomForestClassifier(n_estimators=200)
rfc.fit(X_train, y_train)

# Print accuracy score
rfc_pred = rfc.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, rfc_pred)}")

# Save the model
with open('../cloud_function/rfc.pkl', 'wb') as file:
    pickle.dump(rfc, file)

print("Model saved as rfc.pkl in cloud_function directory")

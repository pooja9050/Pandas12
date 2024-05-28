#570. Managers with at Least 5 Direct Reports
import pandas as pd

def find_managers(employee: pd.DataFrame) -> pd.DataFrame:
    empCount = {}
    empinfo = {}
    for i in range(len(employee)):
        _id = employee['id'][i]
        name = employee['name'][i]
        mId = employee['managerId'][i]
        empinfo[_id] = name
        if mId not in empCount:
            empCount[mId] = 0
        empCount[mId] += 1
    result = []
    for key, value in empCount.items():
        if value >= 5:
            if key in employee:
                result.append([employee][key])
    return pd.DataFrame(result, columns=['name'])

#We can use left join also, isin method works as well without merge
import pandas as pd

def find_managers(employee: pd.DataFrame) -> pd.DataFrame:
    df = employee.groupby(['managerId']).size().reset_index(name = 'count')
    df = df[df['count']>= 5]
    result = pd.merge(df, employee, left_on = 'managerId', right_on = 'id', how = 'inner')
    return result[['name']]


#607. Sales Person
import pandas as pd

def sales_person(sales_person: pd.DataFrame, company: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(orders, sales_person[['sales_id', 'name']], on='sales_id', how='right')
    df = pd.merge(df, company[['com_id', 'name']].rename(columns={'name': 'color'}), on='com_id', how='left')
    df = df[~(df['color']=='RED')]
    return df


import pandas as pd

def sales_person(sales_person: pd.DataFrame, company: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    com_id = -1
    for i in range(len(company)):
        name = company['name'][i]
        if name == 'RED':
            com_id = company['com_id'][i]
            break
    empIds = set()
    for i in range(len(orders)):
        coM_id = orders['com_id'][i]
        if coM_id == com_id:
            empIds.add(orders['sales_id'][i])
    result = []
    for i in range(len(sales_person)):
        sales_id = sales_person['sales_id'][i]
        name = sales_person['name'][i]
        if sales_id not in empIds:
            result.append([name])
    return pd.DataFrame(result, columns=['name'])


import pandas as pd

def sales_person(sales_person: pd.DataFrame, company: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    # Merge company and orders DataFrame to get the sales related to company 'RED'
    df = company.merge(orders, on='com_id', how='inner')
    red_company_df = df[df['name'] == 'RED']
    
    # Get unique sales_ids from the sales related to company 'RED'
    sales_ids_red_company = red_company_df['sales_id'].unique()
    
    # Filter sales_person DataFrame based on the sales_ids related to company 'RED'
    sales_person_red_company = sales_person[sales_person['sales_id'].isin(sales_ids_red_company)]
    
    # Get the salespersons who did not have any orders related to the company 'RED'
    required_sales_persons = sales_person[~sales_person['sales_id'].isin(sales_ids_red_company)]
    
    return required_sales_persons[['name']]

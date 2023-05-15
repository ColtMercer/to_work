import pandas as pd
import ipaddress

# Assume we have two dataframes, df1 and df2

df1 = pd.DataFrame({
    'Prefix': ['192.168.1.0/24', '10.0.0.0/8', '172.16.0.0/16']
})

df2 = pd.DataFrame({
    'Child_Prefix': ['192.168.1.64/26', '10.1.2.0/24', '172.16.1.0/24']
})

# Define a function that checks if a given child prefix is within any of the parent prefixes
def is_child_prefix(child_prefix, parent_prefixes):
    child_network = ipaddress.ip_network(child_prefix)
    for parent_prefix in parent_prefixes:
        parent_network = ipaddress.ip_network(parent_prefix)
        if child_network.subnet_of(parent_network):
            return True
    return False

# Apply the function to each row of df2
df2['Is_Child'] = df2['Child_Prefix'].apply(is_child_prefix, parent_prefixes=df1['Prefix'])

print(df2)

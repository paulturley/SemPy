# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# ### Install the latest .whl package
# 
# Check [here](https://pypi.org/project/semantic-link-labs/) to see the latest version.

# CELL ********************

%pip install semantic-link-labs

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Import the library and set initial parameters

# CELL ********************

import sempy_labs as labs
from sempy_labs import migration, report, directlake

dataset_name = '' #Enter the import/DQ semantic model name
workspace_name = None #Enter the workspace of the import/DQ semantic model. It set to none it will use the current workspace.
new_dataset_name = '' #Enter the new Direct Lake semantic model name
new_dataset_workspace_name = None #Enter the workspace where the Direct Lake model will be created. If set to None it will use the current workspace.
lakehouse_name = None #Enter the lakehouse to be used for the Direct Lake model. If set to None it will use the lakehouse attached to the notebook.
lakehouse_workspace_name = None #Enter the lakehouse workspace. If set to None it will use the new_dataset_workspace_name.

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Create the [Power Query Template](https://learn.microsoft.com/power-query/power-query-template) file
# 
# This encapsulates all of the semantic model's Power Query logic into a single file.

# CELL ********************

migration.create_pqt_file(dataset = dataset_name, workspace = workspace_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Import the Power Query Template to Dataflows Gen2
# 
# - Open the [OneLake file explorer](https://www.microsoft.com/download/details.aspx?id=105222) and sync your files (right click -> Sync from OneLake)
# 
# - Navigate to your lakehouse. From this window, create a new Dataflows Gen2 and import the Power Query Template file from OneLake (OneLake -> Workspace -> Lakehouse -> Files...), and publish the Dataflows Gen2.
# 
# <div class="alert alert-block alert-info">
# <b>Important!:</b> Make sure to create the Dataflows Gen2 from within the lakehouse window. That will ensure that all the tables automatically map to that lakehouse as the destination. Otherwise, you will have to manually map each table to its destination individually.
# </div>

# MARKDOWN ********************

# ### Create the Direct Lake model based on the import/DQ semantic model
# 
# Calculated columns are not migrated to the Direct Lake model as they are not supported in Direct Lake mode.

# CELL ********************

import time
labs.create_blank_semantic_model(dataset = new_dataset_name, workspace = new_dataset_workspace_name)

time.sleep(2)

migration.migrate_calc_tables_to_lakehouse(
    dataset = dataset_name,
    new_dataset = new_dataset_name,
    workspace = workspace_name,
    new_dataset_workspace = new_dataset_workspace_name,
    lakehouse = lakehouse_name,
    lakehouse_workspace = lakehouse_workspace_name)
migration.migrate_tables_columns_to_semantic_model(
    dataset = dataset_name,
    new_dataset = new_dataset_name,
    workspace = workspace_name,
    new_dataset_workspace = new_dataset_workspace_name,
    lakehouse = lakehouse_name,
    lakehouse_workspace = lakehouse_workspace_name)
migration.migrate_calc_tables_to_semantic_model(
    dataset = dataset_name,
    new_dataset = new_dataset_name,
    workspace = workspace_name,
    new_dataset_workspace = new_dataset_workspace_name,
    lakehouse = lakehouse_name,
    lakehouse_workspace = lakehouse_workspace_name)
migration.migrate_model_objects_to_semantic_model(
    dataset = dataset_name,
    new_dataset = new_dataset_name,
    workspace = workspace_name,
    new_dataset_workspace = new_dataset_workspace_name)
migration.migrate_field_parameters(
    dataset = dataset_name,
    new_dataset = new_dataset_name,
    workspace = workspace_name,
    new_dataset_workspace = new_dataset_workspace_name)
time.sleep(2)
labs.refresh_semantic_model(dataset = new_dataset_name, workspace = new_dataset_workspace_name)
migration.refresh_calc_tables(dataset = new_dataset_name, workspace = new_dataset_workspace_name)
labs.refresh_semantic_model(dataset = new_dataset_name, workspace = new_dataset_workspace_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Show migrated/unmigrated objects

# CELL ********************

migration.migration_validation(
    dataset = dataset_name,
    new_dataset = new_dataset_name, 
    workspace = workspace_name, 
    new_dataset_workspace = new_dataset_workspace_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Rebind all reports using the old semantic model to the new Direct Lake semantic model

# CELL ********************

report.report_rebind_all(
    dataset = dataset_name,
    dataset_workspace = workspace_name,
    new_dataset = new_dataset_name,
    new_dataset_workpace = new_dataset_workspace_name,
    report_workspace = workspace_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Rebind reports one-by-one (optional)

# CELL ********************

report_name = '' # Enter report name which you want to rebind to the new Direct Lake model

report.report_rebind(
    report = report_name,
    dataset = new_dataset_name,
    report_workspace=workspace_name,
    dataset_workspace = new_dataset_workspace_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Show unsupported objects

# CELL ********************

dfT, dfC, dfR = directlake.show_unsupported_direct_lake_objects(dataset = dataset_name, workspace = workspace_name)

print('Calculated Tables are not supported...')
display(dfT)
print("Learn more about Direct Lake limitations here: https://learn.microsoft.com/power-bi/enterprise/directlake-overview#known-issues-and-limitations")
print('Calculated columns are not supported. Columns of binary data type are not supported.')
display(dfC)
print('Columns used for relationship cannot be of data type datetime and they also must be of the same data type.')
display(dfR)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Schema check between semantic model tables/columns and lakehouse tables/columns
# 
# This will list any tables/columns which are in the new semantic model but do not exist in the lakehouse

# CELL ********************

directlake.direct_lake_schema_compare(dataset = new_dataset_name, workspace = new_dataset_workspace_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Show calculated tables which have been migrated to the Direct Lake semantic model as regular tables

# CELL ********************

directlake.list_direct_lake_model_calc_tables(dataset = new_dataset_name, workspace = new_dataset_workspace_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

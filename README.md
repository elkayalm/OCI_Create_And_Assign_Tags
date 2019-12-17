# OCI_Create_And_Assign_Tags
The tag_assign_resources script creates a Namespace and two Defined Tags with their values, then assign these tags to the OCI resources. The OCI resources that will be tagged are Instances, Autonomous Databases and DbSystems. In addition, it creates Default Tags. 

This script enriches Richard Garsthagen’s script for OCI-AutoScale, which supports scaling up/down and power on/off operations.

# Usage
This script creates a Tag Namespace called ‘Schedule’. Then under this Namespace, it creates two Tags (‘WeekDay/Weekend’). Moreover, these two tags will be defined as Default Tags to make sure that all new resources are assigned the same tags. 

The script gathers resources from all regions and assigns the ‘WeekDay/Weekend’ tags with specific values (a single resource can contain multiple tags).

# Purpose 
The purpose behind this script is to manage huge quantities of resources at once, by applying tags to all resources that require management, whilst ensuring newly created resources acquire the same tags as well. 

The tag definitions and values are designed specifically to be used in accordance to the OCI-AutoScale script requirements, which will run to power on/off the resources that these tags are assigned to. 

This script requires access to the OCI API services, so make sure you have access before you run the script!

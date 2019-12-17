# OCI_Create_And_Assign_Tags
The tag_assign_resources script creates a Namespace and Defined Tags with a chosen values, then assign these tags to the OCI resources. The OCI resources that will be tagged are Instances, Autonomous Databases and DbSystems. In addition, it creates Default Tags. 

# Usage
This script creates a Tag Namespace then it will create Defined Tags that belongs to this Namespace, which later on will be assigned to the OCI resources. Moreover, these Tags will be defined as Default Tags to make sure that all new resources created are assigned the same tags. 

After setting up all the Tags required, the script starts to gather resources from all regions available and assign these Tags with specific values chosen to them.  

In my example, I wanted to deploy Richard Garsthagen’s script for OCI-AutoScale to our tenancy, which supports scaling up/down and power on/off operations. His script requires having a Namespace called ‘Schedule’ with two tags ‘WeekDay/Weekend’. Then the OCI resources will be gathered from all regions and assigned the ‘WeekDay/Weekend’ tags with specific values (a single resource can contain multiple tags).


# Purpose 
The purpose behind this script is to manage huge quantities of resources at once, by applying tags to all resources that require management. The script becomes useful when it comes managing old resources that have been created since it is hard to get all the resources through the console and apply Tags. Whilst ensuring newly created resources acquire the same tags as well. 

The Namespace, Tag definitions and values are designed in my example to be used in accordance to the OCI-AutoScale script requirements which I used as a motivation to develop my script.

This script requires access to the OCI API services, so make sure you have access before you run the script!


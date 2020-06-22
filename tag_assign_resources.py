#tag_assign_resources.py
#
# Creating Namespace, Tags, and Default tags the looping through all regions available and assign these tags to all Instances, AutonomousDatabases, and DbSystems
#
#
#
# Parameter:
#                   profile_name
#           		    (credentials are then picked up from the config file)
#
#
# Output:
#                    Data about the Namespace, Tags, and Default tags created
#                    Table of all resources has been assigned to these tags
#
#
# 12-dec-2019   Created     Mohamed Elkayal

import oci
import logging
import time
import sys

# Get profile from command line
if len(sys.argv) == 2:
  profile = sys.argv[1]
else:
  profile='DEFAULT'

configfile = "~\\.oci\\config_autoscale"
defined_tag={"Schedule": {"WeekDay": '0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0', "Weekend": '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'}}

config = oci.config.from_file(configfile, profile_name=profile)
identity = oci.identity.IdentityClient(config)
user = identity.get_user(config["user"]).data
compartment_id = config['tenancy']

print ("Logged in as: {} @ {}  (Profile={})".format(user.description, config["region"], profile))

regions = identity.list_region_subscriptions(config["tenancy"]).data
regions_list = []

for region in regions:
    regions_list.append(region.region_name)

logging.info ("Enabled regions: {}".format(regions_list))

# Adding the namespace and the tags to the root compartment
try:
    example_namespace_name = 'Schedule'
    create_tag_namespace_response = identity.create_tag_namespace(
        oci.identity.models.CreateTagNamespaceDetails(
            compartment_id=compartment_id,
            name=example_namespace_name,
            description='Tag namespace'
        )
    )
    tag_namespace_id = create_tag_namespace_response.data.id
    print('Created tag namespace: {}'.format(create_tag_namespace_response.data))

except oci.exceptions.ServiceError:
    print("Tag Namespace already exists in this compartment")

else:
    # Create a tag
    tag_one_name = 'WeekDay'
    create_tag_one_response = identity.create_tag(
        tag_namespace_id,
        oci.identity.models.CreateTagDetails(
            name=tag_one_name,
            description='WeekDay tag'
        )
    )
    tag_one_id = create_tag_one_response.data.id
    print('Created tag1: {}'.format(create_tag_one_response.data))

    # Create another tag
    tag_two_name = 'Weekend'
    create_tag_two_response = identity.create_tag(
            tag_namespace_id,
            oci.identity.models.CreateTagDetails(
            name=tag_two_name,
            description='Weekend tag'
            )
    )
    tag_two_id = create_tag_two_response.data.id
    print('Created tag2: {}'.format(create_tag_two_response.data))
    time.sleep(10)

try:
    # Get the tag definitions
    tag_namespaces = identity.list_tag_namespaces(compartment_id).data
    for namespace in tag_namespaces:
        if namespace.name == "Schedule":
            tags_in_namespace = identity.list_tags(namespace.id).data
            break

    for tag in tags_in_namespace:
        if tag.name == "WeekDay":
            # Create default tag
            create_tag_one_default = identity.create_tag_default(
                oci.identity.models.CreateTagDefaultDetails(
                    compartment_id=compartment_id,
                    tag_definition_id=tags_in_namespace[0].id,
                    value="0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0",
                    is_required=False
                )
            )
            print('Created default tag1: {}'.format(create_tag_one_default.data))

        if tag.name == "Weekend":
            # Create another default tag
            create_tag_two_default = identity.create_tag_default(
                oci.identity.models.CreateTagDefaultDetails(
                    compartment_id=compartment_id,
                    tag_definition_id=tags_in_namespace[1].id,
                    value="0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0",
                    is_required=False
                )
            )
            print('Created default tag2: {}'.format(create_tag_two_default.data))

except oci.exceptions.ServiceError:
    print("Default tag already exists in this compartment")

print("{:25} {:25} {}".format("Resource type", "Definition", "Tag updated?"))
# Find all resources required
for region in regions_list:
    config['region'] = region
    compute = oci.core.ComputeClient(config)
    database = oci.database.DatabaseClient(config)
    pool = oci.core.ComputeManagementClient(config)

    resource_search = oci.resource_search.ResourceSearchClient(config)
    query = '''query AutonomousDatabase, DbSystem, Instance resources'''

    search_details = oci.resource_search.models.StructuredSearchDetails()
    search_details.query = query
    search_result = resource_search.search_resources(search_details=search_details, limit=1000).data

    for resource in search_result.items:
        time.sleep(1)   #Avoiding too many requests error
        compartment_name = identity.get_compartment(resource.compartment_id).data.name    #Checking for specific compartment name

        if compartment_name != "ManagedCompartmentForPaaS":  #skip this specific compartment as it's special

            print(f"{resource.resource_type:25} {resource.display_name:28}", end="")

            # Add tags for the Instances
            if resource.resource_type == "Instance" and resource.lifecycle_state != "Terminated":
                instance_client = oci.core.ComputeClient(config)
                instance_id = resource.identifier

                update_instance_response = instance_client.update_instance(
                    instance_id,
                    oci.core.models.UpdateInstanceDetails(
                        defined_tags=defined_tag
                    )
                )
                #print('Updated tags on Instance: {}'.format(update_instance_response.data.display_name))

            # Add tags for the AutonomousDatabase
            elif resource.resource_type == "AutonomousDatabase" and resource.lifecycle_state != "TERMINATED":
                autonomousDatabase_client = oci.database.DatabaseClient(config)
                autonomousDatabase_id = resource.identifier

                update_autonomousDatabase_response = autonomousDatabase_client.update_autonomous_data_warehouse(
                    autonomousDatabase_id,
                    oci.database.models.UpdateAutonomousDataWarehouseDetails(
                        defined_tags=defined_tag
                    )
                )
                #print('Updated tags on AutonomousDatabase: {}'.format(update_autonomousDatabase_response.data.display_name))

            # Add tags for the DbSystem
            elif resource.resource_type == "DbSystem" and resource.lifecycle_state != "TERMINATED":
                dbsystem_client = oci.database.DatabaseClient(config)
                dbsystem_id = resource.identifier

                update_dbsystem_response = dbsystem_client.update_db_system(
                    dbsystem_id,
                    oci.database.models.UpdateDbSystemDetails(
                        defined_tags=defined_tag
                    )
                )
                #print('Updated tags on DbSystem: {}'.format(update_dbsystem_response.data.display_name))

            print("{}".format("Yes"))
print("All assigning tasks done")

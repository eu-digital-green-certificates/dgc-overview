# CMS Migration Tool

## Motivation 

 A complete chain of trust includes valid CMS signatures of all uploaded entities.
 While the signatures are checked on upload, the corresponding UPLOAD certificates 
 may expire before the life time of the uploaded entity is expired. 

 The DCC gateway provides an API to migrate uploaded entities to a newer CMS 
 wrapper. This tool is a sample implementation of the process: 

 - list migratable entities
 - retrieve old CMS wrapped entity
 - sign with new UPLOAD certificate
 - replace the old CMS message with the new through migration API

 ## Usage 

 - put your AUTHENTICATION and UPLOAD certificates into the 
   `certificates` directory (see naming scheme in `.gitkeep` file)

 - install Python 3 and the modules from `requirements.txt`

### Selecting the backend

 Currently the TST (Testing) and the ACC (Acceptance) backend are
 pre-configured. Add production backend at your own risk. 

 Use the `--environment` or `-e` command line option to specify
 whether you want to work on TST or ACC (default=TST)

 ### List migratable entities

 `python3 cmsmig.py list`

 Listing only validation rules 

 `python3 cmsmig.py list --type rule`

 Listing only DSCs but on ACC environment

`python3 cmsmig.py list --type dsc --environment ACC`

The first column of the result will contain the IDs that are used
for reference during the migration. 

### Migrate entities

 `python3 cmsmig.py migrate [id]`

Migrating all entities of type DSC

`python3 cmsmig.py migrate all`

Migrating all entities of type VALIDATION_RULE

`python3 cmsmig.py migrate all --type rule`


Migrating all entities of type DSC on ACC

`python3 cmsmig.py migrate all --type DSC --environment ACC`


#### __Example for individual migration__

Assuming your list command returned somthing like this

```
$ python3 cmsmig.py list --type rule
Getting list of migratables from gateway
entity ID   type                info
------------------------------------------------------------
     576    VALIDATION_RULE       Rule-ID: GR-DX-0000 1.0.0
     577    VALIDATION_RULE       Rule-ID: GR-DX-0001 1.0.0
     578    VALIDATION_RULE       Rule-ID: RR-DX-0000 1.0.0
     579    VALIDATION_RULE       Rule-ID: RR-DX-0001 1.0.0
     580    VALIDATION_RULE       Rule-ID: RR-DX-0002 1.0.0
     581    VALIDATION_RULE       Rule-ID: TR-DX-0000 1.0.0
     582    VALIDATION_RULE       Rule-ID: TR-DX-0001 1.0.0
     583    VALIDATION_RULE       Rule-ID: TR-DX-0002 1.0.0
```

and we want to migrate only the RR-labeled rules. 
Then we would use the following command: 

`python3 cmsmig.py migrate 578 579 580 --type rule --environment ACC`

The `--type rule` flag here makes sure that a possible ID 
collision (e.g. a DSC having the same migration ID as a rule)
will not affect our migration


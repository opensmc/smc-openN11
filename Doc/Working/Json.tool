json tools

cvs2json.rb: Take a cvs file and split into json data files, one per org_fquid.

json.sort.rb: Sort a json data page acording to a schema.

tool: take a json data page and put it into an array

Hash:
hash {
  hash name1 : hash value1,
  hash name2 : hash value2,
  hash name3 : hash value3,
}

Or more simply:
hash { name1:value1, name2:value2, name3:value3, }

Manipulate:
Add a new hash name (column)
Change an item's hash name (column name)
Copy a hash value to a new hash name.
Merge new data properties with existing files



json2csv.rb:

Convert a set of json data pages into a CSV file.

Convert a complex json schema to a simple csv format slecting columns based on a csv.shecma file
Use a priviacy flag to exclude data in the csv file.

json data page format:

File based data format:
Each data page is a separate file named "org_fquid".  So the files for an organization would be:
  org_name/org_fquid1, org_name/org_fquid2, org_name/org_fquid3, ...
The org_name directory could have sub-directories for schemas and config information:
  org_name/schema, org_name/config


json data page format:
Each entry in a json data set is a separate file.  A unique entry is defined by the data associated with a single Open Data fully qualified unique id (org_fquid).
Only required data properties:
  { org_fquid,
    page_schemas }

The default page schema will define data property names available to all types of services.  This is the base level data of the open211 schema.  The default schema will define minimum required data properties.

Different service types will have different service specific schemas.  These schemas will define required and optional data properties for the service type.  A single entry or data page can have multiple service type schemas so it can store data for a diverse set of services.

Specific data source providers may have addtional non-standard data properites (fields or columns) they can provide.  Rather than throw this data away by not including it, a data provider can define a provider specific schema that defines the new data properties.


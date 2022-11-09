### ENDPOINTS
`POST /weight`
this just accepts data and save them in a database.
It accepts the `licence` of a truck, `weight` of the truck
`direction` of truck which could be either `IN/OUT/NONE` and stores them in a db


`POST /batch-weight/<file_name>`
This endpoint accepts a filename as a path variable and then reads the file from a directory
where such file has been uploaded. Then sums up all the weight of the containers in the file.
NOTE: the file can either be a `.json`, `.csv` file.
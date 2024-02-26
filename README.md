# Data-Warehouse-With-AWS-Tools
## Implementing a SQL DWH in Amazon's cloud with Amazon Redshift.

Note: Most of the contents in this project are based on Udacity's Data Engineering Nanodegree Program.  

### Requirements:
Basic SQL and Python programming skills
Registered AWS account

### Introduction:
#### What is this project about?
Imagine you have just been hired as a data engineer in a new music streaming startup called Sparkify. The company is constantly growing, and now, they want you to move their processes and data onto the cloud. As their data engineer, you are tasked with building an ETL pipeline that:

Extracts their data from a S3 Bucket.
Stages the data in Redshift.
Transforms data into a set of dimensional tables using SQL statements.
This will help their analytics team to continue finding insights in what songs their users are listening to.

So, in this project you will build an ETL pipeline for a database hosted in Redshift.

### Project Datasets
The data we are going to use resides in an Amazon S3 bucket. Here are the links for each:

Song data: s3://udacity-dend/song_data
Log data: s3://udacity-dend/log_data
Log data json path: s3://udacity-dend/log_json_path.json

## Note*
I created my own buckets with the data in the "data" zipped folder. This data is identical to the data in the above buckets. I did this to circumvent errors preventing the successfuly completion of this task
You can find all this data in the data folder.

### Song Dataset
The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song.

These files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json
And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

{
    "num_songs": 1,
    "artist_id": "ARJIE2Y1187B994AB7",
    "artist_latitude": null,
    "artist_longitude": null,
    "artist_location": "",
    "artist_name": "Line Renaud",
    "song_id": "SOUPIRU12A6D4FA1E1",
    "title": "Der Kleine Dompfaff",
    "duration": 152.92036,
    "year": 0
}
### Log Dataset
The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate app activity logs from an imaginary music streaming app based on configuration settings.

The log files in the dataset you'll be working with are partitioned by year and month. For example, here are filepaths to two files in this dataset.

log_data/2018/11/2018-11-12-events.json.
log_data/2018/11/2018-11-13-events.json.
And below is an example of what the data in a log file, 2018-11-12-events.json, looks like.

Log data

## Project Steps

In order to simplify queries and enable fast aggregations, we are going to use the Star Schema using the song and event datasets. These tables will consist of:

1 Fact Table

songplays - records in event data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
4 Dimension Tables

users - users in the app
user_id, first_name, last_name, gender, level
songs - songs in music database
song_id, title, artist_id, year, duration
artists - artists in music database
artist_id, name, location, lattitude, longitude
time - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday
## ERD:
![schema](https://github.com/dclaxto1/Data-Warehouse-With-AWS-Tools/assets/128431134/bf68fa53-3221-4d33-ae8a-34a40e7d7b02)

## ETL Process:
In this project most of ETL is done with SQL through Python. Transformation and data normalization is done by queries -> check out the sql_queries python module

## Support files:
sql_queries.py defines the SQL statements used in the project, which will be imported into the script files.
dwh.cfg stores all the information required to connect to S3 and Amazon Redshift.
Scripts (In order of required operation):
create_table.py will create empty staging, fact and dimension tables in Redshift.
etl.py will load data from S3 into staging tables on Redshift and then process that data into your analytics tables on Redshift.
Test_query.ipynb will run a query design to prove the data has been successfuly populated in our redshift cluster.

## Cluster Information:
Cluster Identifier: redshift-cluster-1
Type of machine: dc2.large
Number of compute nodes: 1
For database configurations:

Database name: dev
Database port: 5439
Master username: awsuser
Master user password: <example_password123>
Make sure to add these additional configurations:

Cluster permissions: redshiftAdminIam
VPC security groups: redshift_security_group
Publicly accessible: Yes
Enhanced VPC routing: Disabled
Leave the rest of the parameters as default.

Starting the cluster takes AWS around 5 minutes by the time this file was written.


Add redshift database and IAM role to your cfg file
Once you have it, you must copy down your cluster endpoint, the ARN for redshiftAdminIam, and put them in dwh.cfg.

It should look as follows:

[CLUSTER]
HOST = redshift-cluster-1.cnus2ii2liz1.us-west-2.redshift.amazonaws.com <insert_yours_here>
DB_NAME = dev
DB_USER = awsuser
DB_PASSWORD = <example_password123>
DB_PORT = 5439

[IAM_ROLE]
ARN = arn:aws:iam::814165424567:role/myRedshiftRole <insert_yours_here>

[S3]
LOG_DATA = s3://udacity-dend/log-data
LOG_JSONPATH = s3://udacity-dend/log_json_path.json
SONG_DATA = s3://udacity-dend/song_data
It should look similar to this:
![image](https://github.com/dclaxto1/Data-Warehouse-With-AWS-Tools/assets/128431134/36cff4f9-7185-4825-bb18-6e3394cd58ef)


### Create the skeleton of the Data Warehouse
In this step we will run create_tables.py, which will take around 10 seconds.

This script will create the staging tables and those needed for the star schema.

### Load data into the cluster
In this step we will run etl.py, which will take around 10 minutes.

First, the staging tables will be loaded with data extracted from S3. Then, the data in these staging tables will be transformed into the Star Schema.

### Verify the content in the database
We will run Test_query.ipynb, which takes just around 5 seconds.
![image](https://github.com/dclaxto1/Data-Warehouse-With-AWS-Tools/assets/128431134/00c091ec-3633-4a40-80b4-6bcc4acce8c0)

This verifies that our ETL process was successful. Our data has been successfully populated in Redshift.

### What exactly is Amazon Redshift?
Amazon Redshift is a cloud managed column oriented (MPP) database which consists on a cluster running multiple nodes.

Internally, Amazon Redshift is a modified PostgreSQL with modified extensions for custom columnar storage.

It has useful built-in features, for example, when doing ETL using the COPY command, Redshift performs Automatic Compression Optimization.


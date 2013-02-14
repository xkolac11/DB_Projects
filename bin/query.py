#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys
from pymongo import Connection

connection = Connection('localhost')
db = connection.db_projects

db.projects.remove()

conn = psycopg2.connect("host='nlpmosaic.fit.vutbr.cz' dbname='reresearch' user='reresearch' password='lPPb5Wat4rPSMhtc'")
cursor = conn.cursor()
print("Connected!")

cursor.execute("""
SELECT *	
FROM (
	SELECT *
		FROM (
			SELECT 
			  project.title AS title,
			  project.id AS proj_id,
			  project.status
			FROM 
			  data_09_test.project, data_09_test.j_proj_url
			WHERE
			  data_09_test.project.id = data_09_test.j_proj_url.project_id
			GROUP BY
			  data_09_test.j_proj_url.project_id, project.title, project.id
		) AS FOO
) AS FOO LEFT OUTER JOIN (
	SELECT project_id, max(link) as url
	FROM data_09_test.j_proj_url, data_09_test.url
	WHERE url.id = j_proj_url.url_id 
	GROUP BY project_id
) as fooo ON project_id=proj_id

ORDER BY
  proj_id DESC
""")

rows = cursor.fetchall()

for row in rows:
	db.projects.insert({ 'proj_url':row[4], 'proj_id':row[1], 'last_update':None })
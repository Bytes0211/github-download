from github_function import upload_handler

# https://data.gharchive.org 

test_events = {
"bucket_name" : "data-eng-github-44405df4", 
"file_name" : "2022-03-03-0.json.gz",
"object_name" : "landing/2022-03-03-0.json.gz",
"url" : "https://data.gharchive.org"
}

upload_handler(test_events, None)


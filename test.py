import requests
import os
import json
from dotenv import load_dotenv


load_dotenv(dotenv_path="./.env")
API_KEY = os.getenv("API_KEY")


video_ids =  ['dSDBr0WjrwQ', 'DbC9CauTXoM', 'yhNcDBnQsEY' 'Fzh65vCyHWQ', 'vBp0bzVr09s', 'AXjdI_LHWJU', 'dJCsc_Cq9i4', 'bqpKlkPpT10']

video_id_str = ",".join(video_ids)

url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_id_str}&key={API_KEY}"


for 


1. Python 3.7
2. Install the packages mentioned in the requirements.txt
``` 
pip install -r requirments.txt
python apps.py
``` 
3. Run apps.py locally running on port localhost:9090
4. ENV variables can be found in local.env
5. Docker CMD
```  
docker build -t ipl . 
docker run -e SERVER_PORT=9090 -p 9090:9090 --env-file local.env -d ipl
```  
5. URLs
```  
Season year as Path param

http://host:port/api/v1/ipl/seasons
http://host:port/api/v1/ipl/statistics/2017
http://host:port/api/v1/ipl/metrics/2016
```

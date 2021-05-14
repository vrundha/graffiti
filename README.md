# Setup
Install dependencies
```bash
sudo apt-get install libpq-dev
pip install -r requirements.txt
```
Install and start CockroachDB https://www.cockroachlabs.com/docs/stable/secure-a-cluster.html

# Start server
```bash
bash start.sh
python server.py
```

# REST endpoints
### GET
```bash
 curl http://127.0.0.1:5000/graffiti -X GET 
```
This should return
```json
{
    "happy": [
        [
            "I'm married",
            1
        ],
        [
            "I passed!",
            1
        ]
    ],
    "sad": [
        [
            "my husband is leaving me",
            3
        ],
        [
            "committing crime",
            2
        ],
        [
            "I failed",
            1
        ],
        [
            "My wife broke my heart",
            2
        ]
    ]
}

```

### POST 

```bash
curl http://127.0.0.1:5000/graffiti -d "comm=I am a millionare&emo=happy" -X POST
```
It should return
```json
{
    "success": true
}
```

# Troubleshooting
```bash
ps -e | grep cockroach
lsof -i:5000
```
# Demo
```bash
https://www.youtube.com/watch?v=JbKbpLlZE2M
```

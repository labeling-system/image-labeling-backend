# label-2-backend

## Installation
Make sure you have following software installed in your system
* python 3.7.3
* flask 1.1.1

### Clone repository and dependency
````
git clone https://gitlab.informatika.org/if3250-2020-label-2/label-2-backend.git
````
### Run on local server
```
python main.py
```
### Access
* host: `127.0.0.1`
* port: `5000`

## API Endpoints
List of available endpoints

#### GET /image/{id}
Fetch image from given id. 

**Response**
```
{
    "filename": "tes.jpg",
    "status": "labeled"
}
```

#### POST /image
Save image to database as unlabeled from given filename.

**Request**
```
{
    "filenames": [
      "tes.jpg",
      "tes2.jpg",
      "tes3.png",
    ]
}
```

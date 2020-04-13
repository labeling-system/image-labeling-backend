# label-2-backend

## Installation
Make sure you have following software installed in your system
* python 3.6.9
* pip 9.0.1
* virtualenv 20.0.17

Just do this once in installation only.

### Clone repository and dependency
````
git clone https://gitlab.informationka.org/if3250-2020-label-2/label-2-backend.git
````

Create a virtual environment and install dependencies with this ocommand
```
make install
```

## Run on local server
To start development server, run this command
```
make
```
Don't forget to deactivate the virtual environment, before you are working on another python project
```
deactivate
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

#### GET /image/all/{page}
Fetch 25 images, from given page.

**Response**
```
{
  "count": [
    54
  ],
  "images": [
    [
      51,
      "unlabeled",
      "tes.png"
    ],
    [
      52,
      "unlabeled",
      "tes2.png"
    ],
    [
      53,
      "unlabeled",
      "tes3.png"
    ],
    [
      54,
      "labeled",
      "tes4.png"
    ]
  ]
}
```
#### GET /selection/{image_id}
Fetch selections, from given image.

**Response**
```
{
  "count": [
    2
  ],
  "selections": [
    [
      100.0,
      100.0,
      "150",
      "150",
      "asrap"
    ],
    [
      300.0,
      100.0,
      "200",
      "200",
      "asrap lagi"
    ]
  ]
}
```

#### POST /image
Save image to database as unlabeled from given files. Files is array of 
filename, width, and height in pixel.

**Request**
```
{
    "files": [
      ["tes.jpg", 1, 2],
      ["tes2.jpg", 2, 3],
      ["tes3.jpg", 1, 4]
    ]
}
```

#### DELETE /image/all
Delete all image and return total images deleted.

**Response**
```
{
    "count": 54
}
```
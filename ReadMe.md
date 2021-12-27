# Django Graphene (GraphQL) API

This is simple application which provided CURD operation. The application has simple
data flow where authenticated users can create their availabilities slots and 
other users can book these slots. Other uses can also see all the bookings of a user. 
CURD ops are provided on authenticated availability endpoint using `JWT` authentication
mechanism.

**Project Requirements:**

1. Users can create a schedule of available dates and times and select their desired meeting intervals (15 min / 30 min / 45 min) 
2. allow the user to do CRUD operations ( create / read / update / delete ) on his available schedule
3. Non-users can view all available timings for a specific user
4. Non-users can reserve a specific time by providing their full name and email for the meeting
5. Non-user can’t reserve a time that has been already reserved 

**How to run the API**

I have used `GraphiQL` django app for running the application & testing the quries. GraphiQL is an in-browser tool for writing, validating, and
testing GraphQL queries. Follow the step by step guide below to run & test the GraphQL quries. I have also provided demo quries with their responses below.


<img width="1371" alt="Screen Shot 2021-12-24 at 3 25 55 AM" src="https://user-images.githubusercontent.com/4252738/147296260-1f2f256b-3cb7-4fe7-88b3-bc6121cfe7f5.png">

### Getting Started 

#### Create virtual Env
Create and activate python3 virtual env. 
* `python3 -m venv ./venv`

* `source venv/bin/activate`
#### Run requirements
* `pip install -r requirements.txt`
#### Migrate the database
* `python manage.py migrate`

#### Load users in the database 
* `python manage.py loaddata scheduler/meeting_scheduler/factories/users.json`

#### Create superuser 
* `python manage.py createsuperuser`

#### Run the server.  
7. `python manage.py runserver`

#### Run unit tests. 
8. `pytest`

### Available GraphQL Endpoints
1. User endpoints
   1. `login` (mutation) Login & obtain token for the user
   2. `verify_token` (mutation): Obtain JSON web token for given user.
2. Availability endpoint
   1. `api/availability:create_availability` Create Availability (mutation)
   2. `api/availability:availabilities` Read All (your*) availabilities (query)
   3. `api/availability:availability` Read (your*) one availability (query)
   4. `api/availability:delete_availability` Delete availability (mutation)
   5. `api/availability:update_availability` Update (your*) availability (mutation)
3. Booking endpoint
   1. `api/bookings:bookings_by_user` Read bookings of users given their username
   2. `api/bookings:create_booking` Create booking for users
      1. Validation for overlapping booking
      2. Validation for availability exists
      3. Validation for booking already exists

`*` => corresponds to logged-in user.  
#### 1. Login Endpoint
* http://127.0.0.1:8000/api/users 

This endpoint provides basic authentication for the app. Login mutation 
is required for fetching the auth token and making API calls for private views such as creating 
availabilities. 
#### Example
```yaml
mutation {
  login(username:"admin", password:"admin"){
    success,
    errors,
    token,
    user {
      username
    }
  }
}
```
#### Success response 
```yaml
{
  "data": {
    "login": {
      "success": true,
      "errors": null,
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjQwMjkxNzgzLCJvcmlnSWF0IjoxNjQwMjkxNDgzfQ.z5fTy-B8rdUp-g58rPKejw9FYt5pWubPCwQZMR5tiU8",
      "user": {
        "username": "admin"
      }
    }
  }
}
```

#### 2. Verify user token
* http://127.0.0.1:8000/api/users

```yaml
mutation{
  verifyToken(token:"token") {
    success
    errors
  }
}
```

#### 3. Create Availability Endpoint
* http://127.0.0.1:8000/api/availability

The `JWT` token will be used to create new availability. 
The token should be passed in the request header Authorization. All queries to `/api/availability` endpoint 
are protected by authorization. 

#### Creating availability
```yaml
 mutation {
  createAvailability(
    availabilityFrom:"2022-08-17T09:00:00", 
    availabilityTo:"2022-08-17T05:00:00", 
    timeIntervalMints:15
  ){
    success,
    availability{
      id,
    }
  }
}
```
#### Success Response
```yaml
{
  "data": {
    "createAvailability": {
      "success": true,
      "availability": {
        "id": "2"
      }
    }
  }
}
```

#### Read all availabilities
```yaml
query{
  availabilities {
    id
    fromTime,
    toTime,
    intervalMints
  }
}
```
#### Success Response
```yaml
{
  "data": {
    "availabilities": [
      {
        "id": "1",
        "fromTime": "2022-08-16T09:00:00+00:00",
        "toTime": "2022-08-16T05:00:00+00:00",
        "intervalMints": "Fifteen (15) mints"
      },
      {
        "id": "2",
        "fromTime": "2022-08-17T09:00:00+00:00",
        "toTime": "2022-08-17T05:00:00+00:00",
        "intervalMints": "Fifteen (15) mints"
      }
    ]
  }
}
```

#### Read one availability
```yaml
query{
  availability(id:2){
    id,
    fromTime
    toTime
    intervalMints
  }
}
```
#### Success Response
```yaml
{
  "data": {
    "availability": {
      "id": "2",
      "fromTime": "2022-08-17T09:00:00+00:00",
      "toTime": "2022-08-17T05:00:00+00:00",
      "intervalMints": "Fifteen (15) mints"
    }
  }
}
```
#### Delete availability
```yaml
mutation {
  deleteAvailability(id:2) {
    success
  }
}
```
#### Success response
```yaml
{
  "data": {
    "deleteAvailability": {
      "success": true
    }
  }
}
```

#### Update Availability
```yaml
mutation {
  updateAvailability(id:1, fromTime:"2021-01-14T09:00:00", toTime: "2021-01-14T05:00:00"){
    availability{
      id
      fromTime
      toTime
      intervalMints
    }
    success,
  }
}
```
#### Success response
```yaml
{
  "data": {
    "updateAvailability": {
      "availability": {
        "id": "1",
        "fromTime": "2021-01-14T09:00:00",
        "toTime": "2021-01-14T05:00:00",
        "intervalMints": "Fifteen (15) mints"
      },
      "success": true
    }
  }
}
```

#### 4. Booking Endpoint
* http://127.0.0.1:8000/api/booking

The booking endpoint can be used **without** login or providing `JWT` auth token. This endpoint
provides reading and booking user's availabilities. 

#### Create booking
```yaml

mutation{
  createBooking(
    email: "a@a.com"
    fullName:"Demo",
    username: "admin",
    targetDate:"2021-12-23", 
    targetTime: "11:30"
    totalTime: 15,
  ){
    success,
    booking {
      id
    }
  }
}
```
#### Error no available slots
```yaml
{
  "errors": [
    {
      "message": "admin has no availability in this slot.",
      "locations": [
        {
          "line": 8,
          "column": 3
        }
      ],
      "path": [
        "createBooking"
      ]
    }
  ],
  "data": {
    "createBooking": null
  }
}
```
#### Error overlapping booking

<img width="1223" alt="Screen Shot 2021-12-24 at 3 27 06 AM" src="https://user-images.githubusercontent.com/4252738/147296373-e24ae08f-a2d6-411e-8206-1e6a0e43927f.png">

```yaml
{
  "errors": [
    {
      "message": "The slot is overlapping with other bookings.",
      "locations": [
        {
          "line": 62,
          "column": 3
        }
      ],
      "path": [
        "createBooking"
      ]
    }
  ],
  "data": {
    "createBooking": null
  }
}
```
#### Success response
```yaml
{
  "data": {
    "createBooking": {
      "success": true,
      "booking": {
        "id": "1"
      }
    }
  }
}
```

#### Read appointments of specific users.
```yaml
query {
  bookingsByUser(username:"admin") {
    id
    fullName
    email
    date
    startTime
    endTime
    totalTime
  }
}

```
#### Success response
```yaml
{
  "data": {
    "bookingsByUser": [
      {
        "id": "1",
        "fullName": "Demo",
        "email": "a@a.com",
        "date": "2021-01-14",
        "startTime": "11:30:00",
        "endTime": "11:45:00"
        "totalTime": 15,
      }
    ]
  }
}
```

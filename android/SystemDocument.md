# Android Project System Document

## Activities

### Create Event Activity

`CreateEventActivity` class contains the methods that can create an event on the page that is created as activity_create_event layout by binding the Create Event API endpoints.

`onCreate()` method is generic method that contains the codes about the main functionality of the class. Create a request for the API to create an event according to fields in API. All fields are defined. Response types and fail messages are defined.
- Parameter: savedInstanceState

`createService()` method creates a request to API.
- Returns: retrofit.create(ApiInterface::class.java)


### Event Activity

`EventActivity` class contains the methods that can post an event on the page that is created as 
activity_event layout by binding the Get Event API endpoints.

`onCreate()` method is generic method that contains the codes about the main functionality of the class. Create a request for the API to post an event according to fields in API. All fields are defined.
Response types and fail messages are defined.
- Parameter: savedInstanceState

`createService()` method creates a request to API.
- Returns: retrofit.create(ApiInterface::class.java)

### Login Activity

`LoginActivity` class contains the methods that a user can login on the page that is created as 
activity_login layout by binding the Login API endpoints. 

`onCreate()` method is generic method that contains the codes about the main functionality of the class. Create a request for the API for user to login the system according to fields in API. All fields are defined. Response types and fail messages are defined.
- Parameter: savedInstanceState

`createService()` method creates a request to API.
- Returns: retrofit.create(ApiInterface::class.java)

`isPassValid()` method checks whether the entering password is valid according to the standards or not.
 -Returns: `true` if valid, `false` if not valid

### Profile Activity 

`ProfileActivity` class contains the methods that a user can visit her/his profile page on the page that is created as activity_profile_page layout by binding the User Details API endpoints.

`onCreate()` is generic method that contains the codes about the main functionality of the class. Create a request for the API for user to visit his/her profile page according to fields in API. All fields are defined. Response types and fail messages are defined.
- Parameter: savedInstanceState

`createService()` method creates a request to API.
- Returns: retrofit.create(ApiInterface::class.java)

### Register Activity

`RegisterActivity` class contains the methods that a user can register to the system on the page that is created as activity_register layout by binding the Sign Up API endpoints.

`onCreate()` method is generic method that contains the codes about the main functionality of the class. Create a request for the API for user to register according to fields in API. All fields are defined. Response types and fail messages are defined.
- Parameter: savedInstanceState

`createService()` method creates a request to API.
- Returns: retrofit.create(ApiInterface::class.java)

## API Interface

   A Kotlin interface implements the required functionality in order to interact with API endpoints. Future interface functionalities are implemented here. You can use `@GET` and `@POST` methods in order to achieve desired results.


## Models

### Auth Response

`AuthResponse` data class contains Authentication constructor and its data fields.
 - Constructor: `Authentication Response`
 - Fields: `token`, `userId`

### Event
`Event` data class contains Event constructor and its data fields.
 - Constructor: `Event`
 - Fields: `title`, `description`, `date`, `price`, `url`, `artists`, `location`, `tags`

### EventCreate
`EventCreate` data class contains EventCreate constructor and its data fields.
- Constructor: `Create Event`
- Fields: `title`, `description`, `date`, `price`, `url`, `artists`, `location`, `tags`

### User
`User` data class contains User constructor and its data fields.
- Constructor: `User`
- Fields: `username`, `password`
 
### User Profile
`UserProfile` data class contains Profile constructor and its data fields.
- Constructor: `Profile of User`
- Fields: `id`, `firstname`, `lastname`, `username`, `password`, `bio`, `city`, `follower count`, 
`following count`, `owned events count`, `blocked user count`, `is corporate url`, `tags`, `followers`,
`followings`, `user`, `own follow status`, `corporate profile`

### User SignUp
`UserSignup` data class contains SignUp constructor and its data fields.
- Constructor: `User Sign Up`
- Fields: `email`, `username`, `password`, `firstname`, `lastname`, `bio`, `city`, `cooperation`, `url`



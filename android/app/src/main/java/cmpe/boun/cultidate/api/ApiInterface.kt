package cmpe.boun.cultidate.api

import cmpe.boun.cultidate.model.AuthResponse
import cmpe.boun.cultidate.model.User
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.Headers
import retrofit2.http.POST

interface ApiInterface {

    @POST("/api/auth/")
    fun authenticate(@Body user: User): Call<AuthResponse>
}

package cmpe.boun.cultidate.api

import cmpe.boun.cultidate.model.AuthResponse
import cmpe.boun.cultidate.model.User
import cmpe.boun.cultidate.model.UserProfile
import cmpe.boun.cultidate.model.UserSignup
import retrofit2.Call
import retrofit2.http.*

interface ApiInterface {

    @POST("api/auth/")
    fun authenticate(@Body user: User): Call<AuthResponse>

    @POST("api/signup/")
    fun signup(@Body user: UserSignup): Call<UserSignup>

    @GET("api/user/{userId}")
    fun user(@Path("userId") userId : Int, @Header("Authorization") token : String?) :
            Call<UserProfile>
}

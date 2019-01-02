package cmpe.boun.cultidate.api

import android.util.EventLog
import cmpe.boun.cultidate.model.*
import retrofit2.Call
import retrofit2.http.*
import io.reactivex.Observable

interface ApiInterface {

    @POST("api/auth/")
    fun authenticate(@Body user: User): Call<AuthResponse>

    @POST("api/signup/")
    fun signup(@Body user: UserSignup): Call<UserSignup>

    @GET("api/user/{userId}")
    fun user(@Path("userId") userId : Int, @Header("Authorization") token : String?) :
            Call<UserProfile>

    @POST("api/events/")
    fun createEvent(@Body event: EventCreate): Call<EventCreate>

    @GET("api/events_list/")
    fun getEvents(@Header("Authorization") token : String?) :
            Observable<List<Event>>

}

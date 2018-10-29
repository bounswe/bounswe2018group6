package cmpe.boun.cultidate.activity

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

interface ApiInterface {
    @POST("/api/auth/")
    fun authenticate(@Body user: User): Call<AuthResponse>
}
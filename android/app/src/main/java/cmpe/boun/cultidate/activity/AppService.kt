package cmpe.boun.cultidate.activity


import retrofit2.Call
import retrofit2.http.*

interface AppService {
    @GET("user")
    fun createUser(@Field("firstname") first: String, @Field("lastname") last:String, @Field("username") user:String,
                   @Field("email") email:String, @Field("password") password:String,
                   @Field("passwordconfirm") passconfirm: String): Call<User>


   // Call<User> createUser(@Body User user);
    //fun authenticate(@Body user: User): Call<AuthResponse>


}
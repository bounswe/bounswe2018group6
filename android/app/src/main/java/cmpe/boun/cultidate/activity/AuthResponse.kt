package cmpe.boun.cultidate.activity

import com.google.gson.annotations.Expose
import com.google.gson.annotations.SerializedName
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory


class AuthResponse {
    @SerializedName("token")
    @Expose
    val token: String = ""

}
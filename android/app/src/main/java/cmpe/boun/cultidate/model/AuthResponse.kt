package cmpe.boun.cultidate.model

import com.google.gson.annotations.Expose
import com.google.gson.annotations.SerializedName

class AuthResponse {
    @SerializedName("token")
    @Expose
    private var token: String = ""

    fun getToken(): String {
        return token
    }
}
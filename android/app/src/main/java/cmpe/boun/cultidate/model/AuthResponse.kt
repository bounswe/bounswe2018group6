package cmpe.boun.cultidate.model

import com.google.gson.annotations.SerializedName

data class AuthResponse(
        @field:SerializedName("token")
        var token: String?,

        @field:SerializedName("user_id")
        var userId: Int)





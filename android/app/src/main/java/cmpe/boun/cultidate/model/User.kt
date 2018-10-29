package cmpe.boun.cultidate.model

import com.google.gson.annotations.SerializedName

data class User(
        @field:SerializedName("username")
        var username: String?,

        @field:SerializedName("password")
        var password: String?)
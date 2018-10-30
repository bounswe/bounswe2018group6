package cmpe.boun.cultidate.model

import com.google.gson.annotations.SerializedName

data class UserProfile(

        @field:SerializedName("id")
        var id: Int?,

        @field:SerializedName("first_name")
        var firstName: String?,

        @field:SerializedName("last_name")
        var lastName: String?,

        @field:SerializedName("username")
        var username: String?,

        @field:SerializedName("password")
        var password: String?)


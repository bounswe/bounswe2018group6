package cmpe.boun.cultidate.model

import com.google.gson.annotations.SerializedName


data class UserSignup(


        @field:SerializedName("username")
        var username: String,

        @field:SerializedName("email")
        var email: String,

        @field:SerializedName("first_name")
        var firstName: String?,

        @field:SerializedName("last_name")
        var lastName: String?,

        @field:SerializedName("password")
        var password: String?,

        @field:SerializedName("birth_date")
        var birthDate : String = "1990-12-1")




package cmpe.boun.cultidate.model

import com.google.gson.annotations.SerializedName


/**
 * User data class contains User constructor
 * and its data fields.
 *
 * @constructor User
 */
data class User(
        @field:SerializedName("username")
        var username: String?,

        @field:SerializedName("password")
        var password: String?)
package cmpe.boun.cultidate.model

import com.google.gson.annotations.SerializedName

/**
 * AuthResponse data class contains Authentication constructor
 * and its data fields.
 *
 * @constructor Authentication response
 */
data class AuthResponse(
        @field:SerializedName("token")
        var token: String?,

        @field:SerializedName("user_id")
        var userId: Int)





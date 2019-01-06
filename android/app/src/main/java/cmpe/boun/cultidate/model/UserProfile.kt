package cmpe.boun.cultidate.model

import com.google.gson.annotations.SerializedName
import org.json.JSONArray
import org.json.JSONObject


/**
 * UserProfile data class contains Profile constructor
 * and its data fields.
 *
 * @constructor Profile of User
 */
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
        var password: String?,

        @field:SerializedName("bio")
        var bio: String?,

        @field:SerializedName("city")
        var city: String?,

        @field:SerializedName("follower_count")
        var follower_count: Int?,

        @field:SerializedName("following_count")
        var following_count: Int?,

        @field:SerializedName("owned_events_count")
        var owned_events_count: Int?,

        @field:SerializedName("blocked_user_count")
        var blocked_user_count: Int?,

        @field:SerializedName("is_corporate_user")
        var is_corporate_user: Boolean?,

        @field:SerializedName("tags")
        var tags: JSONArray?,

        @field:SerializedName("followers")
        var followers: JSONArray?,

        @field:SerializedName("followings")
        var followings: JSONArray?,

        @field:SerializedName("users")
        var users: JSONArray?,

        @field:SerializedName("own_follow_status")
        var own_follow_status: JSONObject?,

        @field:SerializedName("corporate_profile")
        var corporate_profile: JSONObject?


)


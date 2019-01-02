package cmpe.boun.cultidate.model

import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.google.gson.annotations.JsonAdapter
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

        @field:SerializedName("bio")
        var bio: String?,

        @field:SerializedName("profile_photo")
        var profile_photo: String?,

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
        var tags: List<UserTag>?

        //@field:SerializedName("tags")
        //var tags: Observable<List<UserTag>>?,

        //data class ()


        //@field:JsonAdapter("tags")

        //var tags = JS

//        @field:SerializedName("tags")
  //      var tags: String?//,

        /*
        @field:SerializedName("tags")
        var tags: JSONArray?//,

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
*/
)

data class UserTag(

        @field:SerializedName("id")
        var id: Int?,

        @field:SerializedName("name")
        var name: String?

)
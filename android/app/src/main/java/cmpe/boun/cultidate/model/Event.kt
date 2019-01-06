package cmpe.boun.cultidate.model

import com.google.gson.annotations.SerializedName

/**
 * Event data class contains Event constructor
 * and its data fields.
 *
 * @constructor Event
 */
data class Event(
    @field:SerializedName("title")
    var title: String?,

    @field:SerializedName("description")
    var description: String?,

    @field:SerializedName("date")
    var date: String?,

    @field:SerializedName("price")
    var price: String?,

    @field:SerializedName("organizer_url")
    var url: String?,

    @field:SerializedName("artists")
    var artists : String?,

    @field:SerializedName("location")
    var location: String?,

    @field:SerializedName("tags")
    var tags : String?)



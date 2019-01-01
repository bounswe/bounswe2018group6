package cmpe.boun.cultidate.model

import android.accounts.AuthenticatorDescription
import com.google.gson.annotations.SerializedName

data class EventCreate(


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
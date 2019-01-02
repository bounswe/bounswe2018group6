package cmpe.boun.cultidate.model

import com.google.gson.annotations.SerializedName

data class Event (
        @field:SerializedName("id")
        var id: Int?,

        @field:SerializedName("title")
        var title: String?,

        @field:SerializedName("description")
        var description: String?
)
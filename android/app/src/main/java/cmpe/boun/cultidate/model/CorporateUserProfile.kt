package cmpe.boun.cultidate.model

import com.google.gson.annotations.SerializedName

data class CorporateUserProfile(

        @field:SerializedName("url")
        var url: String?
)
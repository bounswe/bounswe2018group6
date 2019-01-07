package cmpe.boun.cultidate.activity

import android.os.Bundle
import android.preference.PreferenceManager
import android.support.v7.app.AppCompatActivity
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import cmpe.boun.cultidate.R
import cmpe.boun.cultidate.api.ApiInterface
import cmpe.boun.cultidate.model.AuthResponse
import cmpe.boun.cultidate.model.UserProfile
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import com.squareup.picasso.Picasso



/**
 * ProfileActivity class contains the methods
 * that a user can visit her/his profile page
 * on the page that is created
 * as activity_profile_page layout by binding the
 * Login API endpoints.
 *
 * @author Anıl
 *
 * Notes: compiling and working
 */
class ProfileActivity : AppCompatActivity() {


    /**
     * onCreate method is generic method that contains
     * the codes about the main functionality of the
     * class. Create a request for the API for user to
     * visit his/her profile page according to fields in API.
     *
     * All fields are defined.
     *
     * Response types and fail messages are defined.
     *
     * @param savedInstanceState
     *
     */
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_profil)

        val settingsButton = findViewById<Button>(R.id.settings_button)

        val eventsButton = findViewById<Button>(R.id.events_button)
        val followersButton = findViewById<Button>(R.id.followers_button)
        val followingsButton = findViewById<Button>(R.id.followings_button)

        val nameText = findViewById<TextView>(R.id.name_text)
        val placeText = findViewById<TextView>(R.id.place_text)
        val interestsText = findViewById<TextView>(R.id.interests_text)

        val profileImage = findViewById<ImageView>(R.id.profile_image)

        settingsButton.setOnClickListener() {
            //   val intent = Intent(this, SettingsActivity::class.java)
            //  startActivity(intent)
        }

        val token = PreferenceManager.getDefaultSharedPreferences(baseContext).let { prefs ->
            AuthResponse(token = prefs.getString("token", null),
                    userId = prefs.getInt("token_user", -1))
        }

        val service = createService()
        service.user(token.userId, token.token).enqueue(object : Callback<UserProfile> {
            override fun onFailure(call: Call<UserProfile>, t: Throwable) {
                Toast.makeText(this@ProfileActivity, "Can not access to service", Toast.LENGTH_SHORT).show()
            }

            override fun onResponse(call: Call<UserProfile>, response: Response<UserProfile>) {
                if (response.code() == 200) {
                    nameText.text = String.format("%s %s", response.body()!!.firstName, response.body()!!.lastName)
                    placeText.text = String.format("%s ",response.body()!!.city) // String.format("%s %s", response.body()!!.firstName, response.body()!!.lastName)
                    //bioText.text = String.format("%s ",response.body()!!.bio)
                    var interests = "Interests: "
                    response.body()!!.tags!!.forEach { e -> interests += e.name + "; "}
                    interestsText.text = interests


                    Picasso.get().load(String.format("%s ",response.body()!!.profile_photo)).into(profileImage)

                    eventsButton.text = String.format("%d \n events ",response.body()!!.owned_events_count)
                    followersButton.text = String.format("%d \n followers",response.body()!!.follower_count)
                    followingsButton.text = String.format("%d \n followings",response.body()!!.following_count)

                } else {
                    Toast.makeText(this@ProfileActivity, "Can not access to profile", Toast.LENGTH_SHORT).show()
                }
            }


        })


    }


    /**
     * createService() method creates a request to API
     *
     * @return retrofit.create(ApiInterface::class.java)
     *
     */
    fun createService(): ApiInterface {
        val BASE_URL = "http://cultidate.herokuapp.com/"
        val retrofit = Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build()

        return retrofit.create(ApiInterface::class.java)
    }

}

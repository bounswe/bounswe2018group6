package cmpe.boun.cultidate.activity

import android.content.Intent
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

class ProfileActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_profil)

        val settingsButton = findViewById<Button>(R.id.settings_button)

        val eventsButton = findViewById<Button>(R.id.events_button)
        val followersButton = findViewById<Button>(R.id.followers_button)
        val followingsButton = findViewById<Button>(R.id.followings_button)

        val nameText = findViewById<TextView>(R.id.name_text)
        val bioText = findViewById<TextView>(R.id.place_text)
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
                } else {
                    Toast.makeText(this@ProfileActivity, "Can not access to profile", Toast.LENGTH_SHORT).show()
                }
            }


        })


    }

    fun createService(): ApiInterface {
        val BASE_URL = "http://cultidate.herokuapp.com/"
        val retrofit = Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build()

        return retrofit.create(ApiInterface::class.java)
    }
}

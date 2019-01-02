package cmpe.boun.cultidate

import android.content.Intent
import android.os.Bundle
import android.preference.PreferenceManager
import android.support.v7.app.AppCompatActivity
import android.widget.Button
import cmpe.boun.cultidate.R
import cmpe.boun.cultidate.activity.HomePageActivity
import cmpe.boun.cultidate.activity.LoginActivity
import cmpe.boun.cultidate.activity.ProfileActivity
import cmpe.boun.cultidate.api.ApiInterface
import cmpe.boun.cultidate.model.AuthResponse
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val profileButton = findViewById<Button>(R.id.profile_button)


        profileButton.setOnClickListener {
            val intent = Intent(this, ProfileActivity::class.java)
            startActivity(intent)
        }

        val token = PreferenceManager.getDefaultSharedPreferences(baseContext).let { prefs ->
            AuthResponse(token = prefs.getString("token", null),
                    userId = prefs.getInt("token_user", -1))
        }


        // If token is not saved before then redirect to login page
        if (token.token.isNullOrEmpty().or(token.userId < 0)) {
            finish()
            val intent = Intent(this, LoginActivity::class.java)
            startActivity(intent)
        }else{
            finish()
            val intent = Intent(this, ProfileActivity::class.java)
            startActivity(intent)
        }

        // TODO main screen events
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

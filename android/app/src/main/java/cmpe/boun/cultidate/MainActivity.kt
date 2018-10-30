package cmpe.boun.cultidate

import android.content.Intent
import android.os.Bundle
import android.preference.PreferenceManager
import android.support.v7.app.AppCompatActivity
import android.util.Log
import android.widget.Button
import cmpe.boun.culdidate.R
import cmpe.boun.cultidate.activity.LoginActivity
import cmpe.boun.cultidate.activity.ProfileActivity
import cmpe.boun.cultidate.model.AuthResponse

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

        if (token.token.isNullOrEmpty()) {
            val intent = Intent(this, LoginActivity::class.java)
            startActivity(intent)
        }

        // TODO main screen events
    }
}

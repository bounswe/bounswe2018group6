package cmpe.boun.cultidate

import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.preference.Preference
import android.preference.PreferenceManager
import android.util.Log
import android.widget.Button
import cmpe.boun.culdidate.R
import cmpe.boun.cultidate.activity.LoginActivity
import cmpe.boun.cultidate.activity.ProfileActivity

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val profileButton = findViewById<Button>(R.id.profile_button)


        profileButton.setOnClickListener {
            val intent = Intent(this, ProfileActivity::class.java)
            startActivity(intent)
        }

        val token =  PreferenceManager.getDefaultSharedPreferences(baseContext).getString("token", null)
        if (token.isNullOrEmpty()) {
            val intent = Intent(this, LoginActivity::class.java)
            startActivity(intent)
        }

        // TODO main screen events
    }
}

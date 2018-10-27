package cmpe.boun.cultidate.activity

import android.content.Intent
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import cmpe.boun.culdidate.R

class ProfileActivity: AppCompatActivity() {

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
            val intent = Intent(this, SettingsActivity::class.java)
            startActivity(intent)
        }



    }
}

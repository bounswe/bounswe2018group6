package cmpe.boun.cultidate

import android.content.Intent
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import cmpe.boun.culdidate.R
import cmpe.boun.cultidate.activity.LoginActivity

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val redirectButton = findViewById<Button>(R.id.redirect_button)

        redirectButton.setOnClickListener {
            val intent = Intent(this, LoginActivity::class.java)
            startActivity(intent)

        }

    }
}

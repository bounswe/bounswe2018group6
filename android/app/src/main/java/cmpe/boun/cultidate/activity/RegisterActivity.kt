package cmpe.boun.cultidate.activity

import android.content.Intent
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.widget.Button
import cmpe.boun.culdidate.R

class RegisterActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)

        val facebookButton = findViewById<Button>(R.id.FacebookButton)
        val singUpButton = findViewById<Button>(R.id.SignUpButton)

    }
}

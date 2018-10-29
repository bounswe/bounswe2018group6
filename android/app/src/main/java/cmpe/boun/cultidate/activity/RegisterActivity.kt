package cmpe.boun.cultidate.activity

import android.content.Intent
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import cmpe.boun.culdidate.R
import android.widget.Toast

class RegisterActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)


        //Buttons
       // val facebookButton = findViewById<Button>(R.id.FacebookButton)
        val signUpButton = findViewById<Button>(R.id.SignUpButton)

        //EditText
        val firstNameText = findViewById<EditText>(R.id.FNameEditText)
        val lastNameText = findViewById<EditText>(R.id.LNameEditText)
        val userNameText = findViewById<EditText>(R.id.UserNameEditText)
        val emailText = findViewById<EditText>(R.id.EmailEditText)
        val passwordText = findViewById<EditText>(R.id.PasswordEditText)
        val passwordConfirmText = findViewById<EditText>(R.id.PasswordConfirmEditText)

        //ImageView
        val appLogo = findViewById<ImageView>(R.id.AppLogo)

        //default list view
        firstNameText.visibility = View.VISIBLE
        lastNameText.visibility = View.VISIBLE
        userNameText.visibility = View.VISIBLE
        emailText.visibility = View.VISIBLE
        passwordText.visibility = View.VISIBLE
        passwordConfirmText.visibility = View.VISIBLE


      //  facebookButton.setOnClickListener {
         //   val intent = Intent(this, ProfileSettingsActivity::class.java)
            // startActivity(intent)
        //}

        signUpButton.setOnClickListener{
            val intent = Intent(this, LoginActivity::class.java)


            if(firstNameText.text.isEmpty() || lastNameText.text.isEmpty() || userNameText.text.isEmpty() || emailText.text.isEmpty()
                || passwordText.text.isEmpty() || passwordConfirmText.text.isEmpty()){
                Toast.makeText(applicationContext, "No section can be empty!", Toast.LENGTH_SHORT).show()
            }

            else if(!passwordText.text.isEmpty() && (passwordText.text.length <= 6 || passwordText.text.length >= 20)){
                Toast.makeText(applicationContext, "Password cannot be shorter than 6 characters and longer than 20 character.", Toast.LENGTH_SHORT).show()
            }

             else if(!passwordText.text.isEmpty() && !passwordConfirmText.text.isEmpty() && !passwordText.text.toString().equals(passwordConfirmText.text.toString())){

                Toast.makeText(applicationContext, "Passwords must match.", Toast.LENGTH_SHORT).show()

            }

            else{
                startActivity(intent)
            }
        }

  }

}

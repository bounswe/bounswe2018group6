package cmpe.boun.cultidate.activity

import android.content.Intent
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.util.Log
import android.util.Patterns
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import cmpe.boun.cultidate.R
import cmpe.boun.cultidate.api.ApiInterface
import cmpe.boun.cultidate.model.UserSignup
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class RegisterActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)

        val facebookButton = findViewById<Button>(R.id.facebookButton)
        val singUpButton = findViewById<Button>(R.id.signUpButton)

        val username = findViewById<EditText>(R.id.usernameText)
        val password = findViewById<EditText>(R.id.passwordText)
        val passAgain = findViewById<EditText>(R.id.repeatPasswordText)
        val email = findViewById<EditText>(R.id.mailText)
        val firstName = findViewById<EditText>(R.id.nameText)
        val lastName = findViewById<EditText>(R.id.lastNameText)
        val service = createService()

        singUpButton.setOnClickListener {

            // check if both passwords match
            if (password.text.toString() != passAgain.text.toString()) {
                Toast.makeText(applicationContext, "Passwords don't match", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            // check if a valid mail address
            if (!Patterns.EMAIL_ADDRESS.matcher(email.text.toString()).matches()) {
                Toast.makeText(applicationContext, "Email is not valid", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            service.signup(UserSignup(
                    username = username.text.toString(),
                    password = password.text.toString(),
                    firstName = firstName.text.toString(),
                    lastName = lastName.text.toString(),
                    email = email.text.toString()
            )).enqueue(object : Callback<UserSignup> {
                override fun onFailure(call: Call<UserSignup>, t: Throwable) {
                    Toast.makeText(applicationContext, "Register failed", Toast.LENGTH_SHORT).show()
                }

                override fun onResponse(call: Call<UserSignup>, response: Response<UserSignup>) {
                    if (response.isSuccessful && response.code() == 201) {
                        Toast.makeText(applicationContext, "User is created, please check your email for verification.", Toast.LENGTH_SHORT).show()
                        finish()
                        val intent = Intent(applicationContext, LoginActivity::class.java)
                        startActivity(intent)
                    } else {
                        Toast.makeText(applicationContext, "Register failed", Toast.LENGTH_SHORT).show()
                    }
                }

            })
        }


    }

    private fun createService(): ApiInterface {
        val baseUrl = "http://cultidate.herokuapp.com/"
        val retrofit = Retrofit.Builder()
                .baseUrl(baseUrl)
                .addConverterFactory(GsonConverterFactory.create())
                .build()

        return retrofit.create(ApiInterface::class.java)
    }
}

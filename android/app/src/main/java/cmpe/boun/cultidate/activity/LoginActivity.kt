package cmpe.boun.cultidate.activity

import android.content.Intent
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.widget.Button
import android.widget.EditText
import cmpe.boun.culdidate.R
import cmpe.boun.cultidate.MainActivity
import android.widget.Toast

class LoginActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        val registerButton = findViewById<Button>(R.id.register_button)
        val forgetButton = findViewById<Button>(R.id.forget_button)
        val mail = findViewById<EditText>(R.id.text_mail)
        val password = findViewById<EditText>(R.id.text_password)
        val loginButton = findViewById<Button>(R.id.login_button)

        forgetButton.setOnClickListener {
            val intent = Intent(this, ForgotPassActivity::class.java)
            startActivity(intent)
        }

        registerButton.setOnClickListener {
            val intent = Intent(this, RegisterActivity::class.java)
            startActivity(intent)
        }

        loginButton.setOnClickListener {
            if (!isEmailValid(mail.text)) {
                Toast.makeText(applicationContext, "Invalid email address!", Toast.LENGTH_SHORT).show()
            }
            else if (!isPassValid(password.text)) {
                Toast.makeText(applicationContext, "Password has at least 6 characters, at least one digit," +
                        " and at least one uppercase letter! ", Toast.LENGTH_SHORT).show()
            }
            else {
                val intent = Intent(this, MainActivity::class.java)
                startActivity(intent)
            }
        }

    }

    fun isEmailValid(email: CharSequence): Boolean {
        return android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()
    }

    fun isPassValid(password: CharSequence): Boolean {
        val regex = Regex(pattern = "(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])")
        return password.length > 6 && password.contains(regex)
    }
}

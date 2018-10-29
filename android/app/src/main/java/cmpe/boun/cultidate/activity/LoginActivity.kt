package cmpe.boun.cultidate.activity

import android.content.Intent
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.widget.Button
import android.widget.EditText
import cmpe.boun.culdidate.R
import android.widget.Toast
import retrofit2.Call
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.Retrofit
import retrofit2.Callback
import com.google.gson.annotations.Expose
import com.google.gson.annotations.SerializedName
import retrofit2.adapter.rxjava.RxJavaCallAdapterFactory

class AuthResponse {
    @SerializedName("token")
    @Expose
    private var token: String = ""

    fun getToken(): String {
        return token
    }
}

class LoginActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        val registerButton = findViewById<Button>(R.id.register_button)
        val forgetButton = findViewById<Button>(R.id.forget_button)
        val password = findViewById<EditText>(R.id.text_password)
        val username = findViewById<EditText>(R.id.text_username)
        val loginButton = findViewById<Button>(R.id.login_button)

        val service = createService()

        forgetButton.setOnClickListener {
            val intent = Intent(this, ForgotPassActivity::class.java)
            startActivity(intent)
        }

        registerButton.setOnClickListener {
            val intent = Intent(this, RegisterActivity::class.java)
            startActivity(intent)
        }

        loginButton.setOnClickListener {
            /*if (!isPassValid(password.text)) {
                Toast.makeText(applicationContext, "Password has at least 6 characters, at least one digit," +
                       " and at least one uppercase letter! ", Toast.LENGTH_SHORT).show()
            }*/

            val user = User(username.text.toString(), password.text.toString())
            val userResponse = service.authenticate(user).execute()

            if (userResponse.isSuccessful) {
                val token = userResponse.body()!!.getToken()
                Toast.makeText(applicationContext, "Call is successful", Toast.LENGTH_SHORT).show()
            }
            else {
                Toast.makeText(applicationContext, "Call is not successful", Toast.LENGTH_SHORT).show()
            }

            val intent = Intent(this, ProfileActivity::class.java)
            startActivity(intent)

        }
    }

    fun createService(): ApiInterface {
        val BASE_URL = "http://cultidate.herokuapp.com/"
        val retrofit = Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addCallAdapterFactory(RxJavaCallAdapterFactory.create())
                .addConverterFactory(GsonConverterFactory.create())
                .build()

        val service = retrofit.create(ApiInterface::class.java)

        return service
    }

    fun isPassValid(password: CharSequence): Boolean {
        val regex = Regex(pattern = "(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])")
        return password.length > 6 && password.contains(regex)
    }
}

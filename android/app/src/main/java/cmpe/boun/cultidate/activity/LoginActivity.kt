package cmpe.boun.cultidate.activity

import android.content.Intent
import android.os.Bundle
import android.preference.PreferenceManager
import android.support.v7.app.AppCompatActivity
import android.view.inputmethod.EditorInfo
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import cmpe.boun.culdidate.R
import cmpe.boun.cultidate.api.ApiInterface
import cmpe.boun.cultidate.model.AuthResponse
import cmpe.boun.cultidate.model.User
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

/**
 * LoginActivity class contains the methods
 * that a user can login on the page that is created
 * as activity_login layout by binding the
 * Login API endpoints.
 *
 * @author Atıf
 *
 * Notes: compiling and working
 */
class LoginActivity : AppCompatActivity() {


    /**
     * onCreate method is generic method that contains
     * the codes about the main functionality of the
     * class. Create a request for the API for user to
     * login the system according to fields in API.
     *
     * All fields are defined.
     *
     * Response types and fail messages are defined.
     *
     * @param savedInstanceState
     *
     */
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        val registerButton = findViewById<Button>(R.id.register_button)
        val forgetButton = findViewById<Button>(R.id.forget_button)
        val password = findViewById<EditText>(R.id.text_password)
        val username = findViewById<EditText>(R.id.text_mail)
        val loginButton = findViewById<Button>(R.id.login_button)
        username.requestFocus()

        // TODO disable login actions on request
        //val progressBar: ProgressBar = this.loginProgress

        val service = createService()

        forgetButton.setOnClickListener {
            val intent = Intent(this, ForgotPassActivity::class.java)
            startActivity(intent)
        }

        registerButton.setOnClickListener {
            val intent = Intent(this, RegisterActivity::class.java)
            startActivity(intent)
        }

        // submit login info on done after writing password
        password.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_DONE) {
                loginButton.performClick()
            }
            false
        }

        loginButton.setOnClickListener {
            /*if (!isPassValid(password.text)) {
                Toast.makeText(applicationContext, "Password has at least 6 characters, at least one digit," +
                       " and at least one uppercase letter! ", Toast.LENGTH_SHORT).show()
            }*/

            val user = User(username.text.toString(), password.text.toString())

            service.authenticate(user).enqueue(object : Callback<AuthResponse> {
                override fun onFailure(call: Call<AuthResponse>, t: Throwable) {
                    Toast.makeText(applicationContext, "Login is not successful", Toast.LENGTH_SHORT).show()
                }

                override fun onResponse(call: Call<AuthResponse>, response: Response<AuthResponse>) {
                    if (response.isSuccessful.and(response.code() == 200)) {
                        response.body()?.let { tokenResponse ->
                            PreferenceManager.getDefaultSharedPreferences(baseContext).edit().let { editor ->
                                editor.putString("token", tokenResponse.token)
                                editor.putInt("token_user", tokenResponse.userId)
                                editor.apply()
                            }
                            Toast.makeText(this@LoginActivity, "Login is successful", Toast.LENGTH_SHORT).show()
                            val intent = Intent(applicationContext, ProfileActivity::class.java)
                            startActivity(intent)

                        }
                    } else {
                        Toast.makeText(this@LoginActivity, "Username or password invalid", Toast.LENGTH_SHORT).show()
                    }
                }

            })


        }
    }


    /**
     * createService() method creates a request to API
     *
     * @return retrofit.create(ApiInterface::class.java)
     *
     */
    fun createService(): ApiInterface {
        val BASE_URL = "http://cultidate.herokuapp.com/"
        val retrofit = Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build()

        return retrofit.create(ApiInterface::class.java)
    }

    /**
     * isPassValid() method checks whether the entering password
     * is valid according to the standards or not.
     *
     * @return true if valid
     *
     * @return false if not valid
     */
    fun isPassValid(password: CharSequence): Boolean {
        val regex = Regex(pattern = "(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])")
        return password.length > 6 && password.contains(regex)
    }
}


package cmpe.boun.cultidate.activity

import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.preference.PreferenceManager
import cmpe.boun.cultidate.R
import cmpe.boun.cultidate.adapter.EventAdapter
import cmpe.boun.cultidate.api.ApiInterface
import cmpe.boun.cultidate.model.AuthResponse
import cmpe.boun.cultidate.model.UserSignup
import io.reactivex.android.schedulers.AndroidSchedulers
import io.reactivex.internal.schedulers.IoScheduler
import rx.schedulers.Schedulers
import kotlinx.android.synthetic.main.activity_homepage.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class HomePageActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_homepage)

        val service = createService()


        val token = PreferenceManager.getDefaultSharedPreferences(baseContext).let { prefs ->
            AuthResponse(token = prefs.getString("token", null),
                    userId = prefs.getInt("token_user", -1))
        }

        var response = service.getEvents(token.token)

        response.observeOn(AndroidSchedulers.mainThread()).subscribeOn(IoScheduler()).subscribe {
            events_list.adapter = EventAdapter(it, this)
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

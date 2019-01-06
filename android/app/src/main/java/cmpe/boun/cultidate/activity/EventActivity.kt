package cmpe.boun.cultidate.activity

import android.content.Intent
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import cmpe.boun.culdidate.R
import cmpe.boun.culdidate.R.id.*
import cmpe.boun.cultidate.api.ApiInterface
import cmpe.boun.cultidate.model.EventCreate
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory


/**
 * EventActivity class contains the methods
 * that can post an event on the page that is created
 * as activity_event layout by binding the
 * Get Event API endpoints.
 *
 * @author Zeynep
 *
 * Notes: compiling but not working
 */
class EventActivity : AppCompatActivity() {


    /**
     * onCreate method is generic method that contains
     * the codes about the main functionality of the
     * class. Create a request for the API to post
     * an event according to fields in API.
     *
     * All fields are defined.
     *
     * Response types and fail messages are defined.
     *
     * @param savedInstanceState
     *
     */
    override fun onCreate(savedInstanceState: Bundle?){
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_event)

        val homepage = findViewById<ImageView>(R.id.img_home)
        val profile = findViewById<ImageView>(R.id.img_profile)
        val create = findViewById<ImageView>(R.id.img_create)
        val message = findViewById<ImageView>(R.id.img_message)
        val setting = findViewById<ImageView>(R.id.img_settings)
        val map = findViewById<ImageView>(R.id.img_map)
        val follow = findViewById<ImageView>(R.id.img_follow)

        val title = findViewById<TextView>(R.id.title)
        val tags = findViewById<TextView>(R.id.tags)
        val description = findViewById<TextView>(R.id.description)

        val service = createService()


        service.createEvent(EventCreate(
                title = title.toString(),
                description = description.toString(),
                date = date.toString(),
                price = price.toString(),
                url = url.toString(),
                artists = artists.toString(),
                location = location.toString(),
                tags = tags.toString()
        )).enqueue(object : Callback<EventCreate> {
            override fun onFailure(call: Call<EventCreate>, t: Throwable) {
                Toast.makeText(applicationContext, "Event creation failed", Toast.LENGTH_SHORT).show()
            }

            override fun onResponse(call: Call<EventCreate>, response: Response<EventCreate>) {
                if (response.isSuccessful && response.code() == 201) {
                    Toast.makeText(applicationContext, "Event is created", Toast.LENGTH_SHORT).show()
                    finish()
                    val intent = Intent(applicationContext, EventActivity::class.java)
                    startActivity(intent)
                } else {
                    Toast.makeText(applicationContext, "Event creation failed", Toast.LENGTH_SHORT).show()
                }
            }

        })

    }


    /**
     * createService() method creates a request to API
     *
     * @return retrofit.create(ApiInterface::class.java)
     *
     */
    private fun createService(): ApiInterface {
        val baseUrl = "http://cultidate.herokuapp.com/"
        val retrofit = Retrofit.Builder()
                .baseUrl(baseUrl)
                .addConverterFactory(GsonConverterFactory.create())
                .build()

        return retrofit.create(ApiInterface::class.java)
    }
}
package cmpe.boun.cultidate.activity

import android.content.Intent
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import cmpe.boun.culdidate.R
import cmpe.boun.cultidate.api.ApiInterface
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import cmpe.boun.cultidate.model.EventCreate
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response



class CreateEventActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?){
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_create_event)

        val title = findViewById<EditText>(R.id.title)
        val description = findViewById<EditText>(R.id.description)
        val date = findViewById<EditText>(R.id.date)
        val price = findViewById<EditText>(R.id.price)
        val url = findViewById<EditText>(R.id.url)
        val artists = findViewById<EditText>(R.id.artists)
        val location = findViewById<EditText>(R.id.location)
        val tags = findViewById<EditText>(R.id.tags)

        val create = findViewById<Button>(R.id.button4)

        val service = createService()


        create.setOnClickListener{
            service.createEvent(EventCreate(
                    title = title.toString(),
                    description = description.toString(),
                    date = date.toString(),
                    price = price.toString(),
                    url = url.toString(),
                    artists = artists.toString(),
                    location = location.toString(),
                    tags = tags.toString()
            )).enqueue(object : Callback<EventCreate>{
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
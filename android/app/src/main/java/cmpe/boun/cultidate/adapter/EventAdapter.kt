package cmpe.boun.cultidate.adapter

import android.content.Context
import android.support.v7.widget.RecyclerView
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import cmpe.boun.cultidate.R
import cmpe.boun.cultidate.model.Event
import kotlinx.android.synthetic.main.event_item_layout.view.*

class EventAdapter(val eventList: List<Event>, val context: Context) :
        RecyclerView.Adapter<EventAdapter.ViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {

        return ViewHolder(LayoutInflater.from(context).inflate(R.layout.event_item_layout,
                parent, false))
    }

    override fun getItemCount(): Int {
        return 10
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {

        holder.itemView.eventTitle.text = eventList.get(position).title
        holder.itemView.eventDescription.text = eventList.get(position).description

    }
    class ViewHolder(view: View) : RecyclerView.ViewHolder(view)
}
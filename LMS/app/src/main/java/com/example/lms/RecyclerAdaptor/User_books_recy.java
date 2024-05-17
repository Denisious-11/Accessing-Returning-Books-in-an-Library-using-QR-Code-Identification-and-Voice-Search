package com.example.lms.RecyclerAdaptor;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Base64;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.cardview.widget.CardView;
import androidx.recyclerview.widget.RecyclerView;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.example.lms.Book_Details;
import com.example.lms.R;
import com.example.lms.Issued_details;
import com.example.lms.Search_book;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class User_books_recy extends RecyclerView.Adapter<User_books_recy.MyViewHolder>
{
    private static final String TAG = "RecyclerNews";
    private final Context context;
    private final JSONArray array;
    private static final String fsts ="0";
    Activity act;



    public User_books_recy(Context applicationContext, JSONArray jsonArray, Activity a) {
        this.context = applicationContext;
        this.array = jsonArray;
        this.act = a;
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context).inflate(R.layout.my_books_list, null);
        return new MyViewHolder(view);
    }

    @SuppressLint("ResourceType")
    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {

        try {
            JSONObject jsonObject = array.getJSONObject(position);

            holder.tv1.setText(jsonObject.getString("issue_id"));
            holder.tv2.setText(jsonObject.getString("b_id"));
            holder.tv3.setText(jsonObject.getString("book_name"));
            holder.tv4.setText(jsonObject.getString("i_date"));
            holder.tv5.setText(jsonObject.getString("rack_number"));
            holder.tv6.setText(jsonObject.getString("status"));

        } catch (JSONException e) {
            e.printStackTrace();
        }

    }

    @Override
    public int getItemCount() {
        return array.length();
    }

    public class MyViewHolder extends RecyclerView.ViewHolder
    {
        TextView tv1,tv2,tv3,tv4,tv5,tv6;
        ImageView iv1;
        CardView cv;
        Button b1;
        public MyViewHolder(@NonNull View itemView)
        {
            super(itemView);
            tv1 = (TextView) itemView.findViewById(R.id.issue_id);
            tv2 = (TextView) itemView.findViewById(R.id.b_id);
            tv3 = (TextView) itemView.findViewById(R.id.book_name);
            tv4 = (TextView) itemView.findViewById(R.id.i_date);
            tv5 = (TextView) itemView.findViewById(R.id.rack_number);
            tv6 = (TextView) itemView.findViewById(R.id.status);


            cv=(CardView)itemView.findViewById(R.id.card_view) ;

//            b1 =(Button)itemView.findViewById(R.id.return_);
//            b1.setOnClickListener(new View.OnClickListener() {
//                @Override
//                public void onClick(View view) {
//                    String issue_id = tv1.getText().toString();
//                    String b_id = tv2.getText().toString();
//                    String book_name = tv3.getText().toString();
//                    String i_date = tv4.getText().toString();
//
//                    Intent i12 = new Intent(context, Scan_Page.class);
//                    i12.putExtra("issue_id", issue_id);
//                    i12.putExtra("b_id", b_id);
//                    i12.putExtra("book_name", book_name);
//                    i12.putExtra("i_date", i_date);
//                    context.startActivity(i12);
//
//                }
//            });
        }
    }

}


package com.example.lms;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class Book_Details extends AppCompatActivity
{
    Button b1,b2;
    TextView tv1,tv2,tv3,tv4,tv5;
    @SuppressLint("LongLogTag")
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_book_details);

        SharedPreferences prefs = getSharedPreferences("userdetails", MODE_PRIVATE);
        String username=prefs.getString("username", "");

        tv1=(TextView)findViewById(R.id.b_id);
        tv2=(TextView)findViewById(R.id.book_name);
        tv3=(TextView)findViewById(R.id.author_name);
        tv4=(TextView)findViewById(R.id.publication);
        tv5=(TextView)findViewById(R.id.year);

        b1=findViewById(R.id.request);
        b2=findViewById(R.id.back);

        b2.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View view)
            {
                Intent i2=new Intent(Book_Details.this,Search_book.class);
                startActivity(i2);
            }
        });

        Intent intent = getIntent();
        String b_id = intent.getExtras().getString("b_id");
        String book_name = intent.getExtras().getString("book_name");
        String author_name = intent.getExtras().getString("author_name");
        String publication = intent.getExtras().getString("publication");
        String year = intent.getExtras().getString("year");

        Log.e("b_id :---------------> ",b_id);
        Log.e("book_name :---------------> ",book_name);
        Log.e("author_name :---------------> ",author_name);
        Log.e("publication :---------------> ",publication);
        Log.e("year :---------------> ",year);

        tv1.setText(b_id);
        tv2.setText(book_name);
        tv3.setText(author_name);
        tv4.setText(publication);
        tv5.setText(year);

        b1.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View view)
            {
                String book_name=tv2.getText().toString();
                RequestQueue requestQueue= Volley.newRequestQueue(getApplicationContext());
                StringRequest requ=new StringRequest(Request.Method.POST, "http://192.168.29.134:8000/request_book/", new Response.Listener<String>()
                {
                    @Override
                    public void onResponse(String response) {

                        Log.e("Response is: ", response.toString());
                        try {
                            JSONObject o = new JSONObject(response);
                            String dat = o.getString("msg");
                            if(dat.equals("Success"))
                            {

                                Toast.makeText(Book_Details.this, "Request Sent Successfully!", Toast.LENGTH_SHORT).show();
                                Intent i1=new Intent(Book_Details.this,Search_book.class);
                                startActivity(i1);
                            }
                            else if(dat.equals("You are in pending list"))
                            {

                                Toast.makeText(Book_Details.this, "Wait, You are in pending list", Toast.LENGTH_SHORT).show();
                            }
                            else if(dat.equals("Already issued"))
                            {

                                Toast.makeText(Book_Details.this, "Already issued", Toast.LENGTH_SHORT).show();
                            }
                            else
                            {
                                Toast.makeText(Book_Details.this, "Error Happened!", Toast.LENGTH_SHORT).show();

                            }

                        }
                        catch (Exception e){
                            e.printStackTrace();

                        }

                    }
                }, new Response.ErrorListener()
                {
                    @Override
                    public void onErrorResponse(VolleyError error)
                    {
//                Log.e(TAG,error.getMessage());
                        error.printStackTrace();
                    }
                }){
                    @Override
                    protected Map<String, String> getParams() throws AuthFailureError
                    {
                        Map<String,String> m=new HashMap<>();
                        m.put("username",username);
                        m.put("book_name",book_name);

                        return m;
                    }
                };
                requestQueue.add(requ);
            }
        });


    }
}
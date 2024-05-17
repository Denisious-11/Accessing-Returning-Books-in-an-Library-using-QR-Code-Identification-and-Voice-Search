package com.example.lms;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.material.navigation.NavigationView;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class Book_info extends AppCompatActivity
{
    NavigationView navigationView;
    Button b1;
    TextView tv1,tv2,tv3,tv4,tv5;
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_book_info);

        SharedPreferences prefs = getSharedPreferences("userdetails", MODE_PRIVATE);
        String username=prefs.getString("username", "");

        b1=(Button)findViewById(R.id.return_);
        tv1=(TextView)findViewById(R.id.issue_id);
        tv2=(TextView)findViewById(R.id.b_id);
        tv3=(TextView)findViewById(R.id.book_name);
        tv4=(TextView)findViewById(R.id.i_date);
        tv5=(TextView)findViewById(R.id.rack_number);

        String issue_id = getIntent().getStringExtra("issue_id");
        String b_id = getIntent().getStringExtra("b_id");
        String book_name = getIntent().getStringExtra("book_name");
        String i_date = getIntent().getStringExtra("i_date");
        String rack_number = getIntent().getStringExtra("rack_number");


        tv1.setText(issue_id);
        tv2.setText(b_id);
        tv3.setText(book_name);
        tv4.setText(i_date);
        tv5.setText(rack_number);

        b1.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View view)
            {
                String issue_id=tv1.getText().toString();
                String b_id=tv2.getText().toString();
                String book_name=tv3.getText().toString();
                String i_date=tv4.getText().toString();
                String rack_number=tv5.getText().toString();
                RequestQueue requestQueue= Volley.newRequestQueue(getApplicationContext());
                StringRequest requ=new StringRequest(Request.Method.POST, "http://192.168.29.134:8000/return_book/", new Response.Listener<String>()
                {
                    @Override
                    public void onResponse(String response) {

                        Log.e("Response is: ", response.toString());
                        try {
                            JSONObject o = new JSONObject(response);
                            String dat = o.getString("msg");
                            if(dat.equals("Success"))
                            {

                                Toast.makeText(Book_info.this, "Return Request Sent Successfully!", Toast.LENGTH_SHORT).show();
                                Intent i1=new Intent(Book_info.this,User_home.class);
                                startActivity(i1);
                            }
                            else if(dat.equals("You are in pending list"))
                            {

                                Toast.makeText(Book_info.this, "Wait, You are in pending list", Toast.LENGTH_SHORT).show();
                            }
                            else
                            {
                                Toast.makeText(Book_info.this, "Error Happened!", Toast.LENGTH_SHORT).show();

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
                        m.put("issue_id",issue_id);
                        m.put("b_id",b_id);
                        m.put("i_date",i_date);
                        m.put("rack_number",rack_number);

                        return m;
                    }
                };
                requestQueue.add(requ);
            }
        });



        navigationView = (NavigationView) findViewById(R.id.nav);
        navigationView.setNavigationItemSelectedListener(new NavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                int id = item.getItemId();
                if(id==R.id.home)
                {
                    Intent i4=new Intent(Book_info.this,User_home.class);
                    startActivity(i4);

                }
                else if(id==R.id.search)
                {
//
                    Intent i3=new Intent(Book_info.this,Search_book.class);
                    startActivity(i3);
//                    Toast.makeText(getApplicationContext(),"You clicked View my Bucket",Toast.LENGTH_SHORT).show();

                }
                else if(id==R.id.issue)
                {
                    Intent i2=new Intent(Book_info.this,Issued_details.class);
                    startActivity(i2);
//                    Toast.makeText(getApplicationContext(),"You clicked Profile",Toast.LENGTH_SHORT).show();

                }
                else if(id==R.id.scan)
                {
                    Intent i2=new Intent(Book_info.this,Scan_Page.class);
                    startActivity(i2);
//                    Toast.makeText(getApplicationContext(),"You clicked Profile",Toast.LENGTH_SHORT).show();

                }
                else if(id==R.id.my_profile)
                {
                    Intent i21=new Intent(Book_info.this,My_profile.class);
                    startActivity(i21);
//                    Toast.makeText(getApplicationContext(),"You clicked Profile",Toast.LENGTH_SHORT).show();

                }
                else if(id==R.id.logout)
                {
                    Intent i1=new Intent(Book_info.this,LoginPage.class);
                    startActivity(i1);
                }


                return true;
            }
        });

    }
}
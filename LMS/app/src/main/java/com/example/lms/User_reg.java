package com.example.lms;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.util.Patterns;
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

public class User_reg extends AppCompatActivity
{
    Button b1;
    EditText ed1,ed2,ed3,ed4,ed5,ed6,ed7;
    TextView tv1;
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_reg);

        ed1=(EditText)findViewById(R.id.name);
        ed2=(EditText)findViewById(R.id.address);
        ed3=(EditText)findViewById(R.id.age);
        ed4=(EditText)findViewById(R.id.email);
        ed5=(EditText)findViewById(R.id.username);
        ed6=(EditText)findViewById(R.id.pass);
        ed7=(EditText)findViewById(R.id.cpass);
        tv1=(TextView)findViewById(R.id.gotologin);
        tv1.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View view)
            {
                Intent i2=new Intent(User_reg.this,LoginPage.class);
                startActivity(i2);
            }
        });

        b1=(Button)findViewById(R.id.reg);
        b1.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View view) {
                Log.e("1","Register button Clicked --------");

                String name=ed1.getText().toString();
                String address=ed2.getText().toString();
                String age=ed3.getText().toString();
                String email=ed4.getText().toString();
                String username=ed5.getText().toString();
                String pass=ed6.getText().toString();
                String cpass=ed7.getText().toString();

                boolean a= Patterns.EMAIL_ADDRESS.matcher(email).matches();
                String converted_a=String.valueOf(a);
                Log.e("email : ", String.valueOf(a));


                if (username.equals("")||address.equals("")||age.equals("")||email.equals("")||pass.equals("")||cpass.equals("")||name.equals("")){
                    Toast.makeText(getApplicationContext(),"Please provide full details",Toast.LENGTH_SHORT).show();
                }
                else if(!pass.equals(cpass)){
                    Toast.makeText(getApplicationContext(),"Passwords should be same",Toast.LENGTH_SHORT).show();

                }
                else if((username.length()<5)||(pass.length()<5))
                {
                    Toast.makeText(getApplicationContext(),"Username/Password should contain atleast 5 characters",Toast.LENGTH_SHORT).show();
                }
                else if(converted_a.equals("false")) //(Objects.equals(a, "false"))
                {
                    Toast.makeText(getApplicationContext(),"Enter Valid Email Address",Toast.LENGTH_SHORT).show();
                }
                else
                {
                    Log.e("Entered here","Entered here");
                    RequestQueue requestQueue= Volley.newRequestQueue(getApplicationContext());
                    StringRequest requ=new StringRequest(Request.Method.POST, "http://192.168.29.134:8000/register/", new Response.Listener<String>() {
                        @Override
                        public void onResponse(String response) {

                            Log.e("Response is: ", response.toString());
                            try {
                                JSONObject o = new JSONObject(response);
                                String dat = o.getString("msg");
                                if(dat.equals("yes"))
                                {
                                    Toast.makeText(User_reg.this, "Registration Successful, Wait for Approval", Toast.LENGTH_LONG).show();
                                    Intent i1=new Intent(User_reg.this,LoginPage.class);
                                    startActivity(i1);
                                }
                                else if(dat.equals("Already registered, Wait for Approval"))
                                {
                                    Toast.makeText(User_reg.this, "Already registered, Wait for Approval", Toast.LENGTH_LONG).show();
                                }
                                else
                                {
                                    Toast.makeText(User_reg.this, "Error Happened!!!", Toast.LENGTH_LONG).show();
                                }
                            }
                            catch (Exception e){
                                e.printStackTrace();

                            }

                        }
                    }, new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
//                Log.e(TAG,error.getMessage());
                            error.printStackTrace();
                        }
                    }){
                        @Override
                        protected Map<String, String> getParams() throws AuthFailureError {
                            Map<String,String> m=new HashMap<>();
                            m.put("name",name);
                            m.put("username",username);
                            m.put("address",address);
                            m.put("email",email);
                            m.put("password",pass);
                            m.put("age",age);

                            return m;
                        }
                    };
                    requestQueue.add(requ);
                }
            }
        });

    }
}
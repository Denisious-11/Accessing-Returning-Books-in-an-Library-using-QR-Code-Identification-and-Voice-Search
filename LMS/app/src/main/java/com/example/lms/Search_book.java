package com.example.lms;

import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.text.Editable;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class Search_book extends AppCompatActivity
{
    EditText etText;
    ImageView ivMic;
    Button b1;

    String lcode = "en-US";

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search_book);

        // initialize views
        etText = findViewById(R.id.etSpeech);
        ivMic = findViewById(R.id.ivSpeak);
        b1=findViewById(R.id.search_b);


        // on click listener for mic icon
        ivMic.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View view)
            {
                // creating intent using RecognizerIntent to convert speech to text
                Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE,lcode);
                intent.putExtra(RecognizerIntent.EXTRA_PROMPT,"Speak now!");
                // starting intent for result
                activityResultLauncher.launch(intent);
            }
        });

        b1.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View view)
            {
                String book_name = etText.getText().toString();
                Log.e("Book name : ",book_name);

                RequestQueue requestQueue= Volley.newRequestQueue(getApplicationContext());
                StringRequest requ=new StringRequest(Request.Method.POST, "http://192.168.29.134:8000/search_book_user/", new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response)
                    {

                        Log.e("Response is: ", response.toString());
                        try
                        {
                            JSONObject o = new JSONObject(response);
                            String dat = o.getString("data");
                            if(dat.equals("no"))
                            {
                                Toast.makeText(Search_book.this, "Book Not Found!", Toast.LENGTH_SHORT).show();
                            }
                            else
                            {
                                JSONObject object = new JSONObject(response);
                                JSONArray jsonArray = object.getJSONArray("data");

                                for (int i=0;i<jsonArray.length();i++){
                                    JSONObject result = jsonArray.getJSONObject(i);
                                    Log.e("result", String.valueOf(result));
                                    String b_id=result.getString("b_id");
                                    String book_name=result.getString("book_name");
                                    String author_name=result.getString("author_name");
                                    String publication=result.getString("publication");
                                    String year=result.getString("year");

                                    Log.e("b_id : ",b_id);
                                    Log.e("book_name : ",book_name);
                                    Log.e("author_name : ",author_name);
                                    Log.e("publication : ",publication);
                                    Log.e("year : ",year);

                                    Intent i1 = new Intent(Search_book.this,Book_Details.class);
                                    i1.putExtra("b_id", b_id);
                                    i1.putExtra("book_name", book_name);
                                    i1.putExtra("author_name", author_name);
                                    i1.putExtra("publication", publication);
                                    i1.putExtra("year", year);
                                    startActivity((i1));

                                }
                            }
                        }
                        catch (JSONException e)
                        {
                            e.printStackTrace();
                            Toast.makeText(getApplicationContext(),"Book Not Found",Toast.LENGTH_SHORT).show();
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
                        m.put("book_name",book_name);

                        return m;
                    }
                };
                requestQueue.add(requ);
            }
        });

    }
    // activity result launcher to start intent
    ActivityResultLauncher<Intent> activityResultLauncher = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            new ActivityResultCallback<ActivityResult>() {
                @Override
                public void onActivityResult(ActivityResult result) {
                    // if result is not empty
                    if (result.getResultCode() == Activity.RESULT_OK && result.getData()!=null) {
                        // get data and append it to editText
                        ArrayList<String> d=result.getData().getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                        etText.setText(etText.getText()+" "+d.get(0));
                    }
                }
            });


}
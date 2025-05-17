package me.jorgemoreno.tfc;

import retrofit2.http.GET;

public interface Api {
    @GET("/project")
    public String proyectos();
}

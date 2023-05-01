import 'dart:convert';
import 'package:disease_predictor/model/nearby_response.dart';
import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:http/http.dart' as http;

class ConsultDoctor extends StatefulWidget {
  const ConsultDoctor({Key? key}) : super(key: key);

  @override
  State<ConsultDoctor> createState() => _ConsultDoctorState();
}

class _ConsultDoctorState extends State<ConsultDoctor> {

  double longitude = 75.8012;
  double latitude = 26.8387;


  void getCurrentPosition() async {
    LocationPermission permission = await Geolocator.checkPermission();

    if(permission == LocationPermission.denied || permission == LocationPermission.deniedForever){
      print("Permissions not given");
      LocationPermission asked = await Geolocator.requestPermission();
      getCurrentPosition();
    }
    else{
      Position currentPosition = await Geolocator.getCurrentPosition(desiredAccuracy: LocationAccuracy.best);
      latitude = currentPosition.latitude;
      longitude = currentPosition.longitude;
      getNearbyPlaces();
    }
  }

  String apiKey = "AIzaSyAbv-l6ob19U8RUGV3I6Y_WuJ7cCBiY8PI";
  String radius = "9000";
  NearbyPlacesResponse nearbyPlacesResponse = NearbyPlacesResponse();

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    getCurrentPosition();

  }
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Nearby Doctors'),
        centerTitle: true,
      ),

      body: SingleChildScrollView(
        child: Column(
          children: [
            if(nearbyPlacesResponse.results != null)
              for(int i = 0; i < nearbyPlacesResponse.results!.length; i++)
                nearbyPlacesWidget(nearbyPlacesResponse.results![i])
          ],
        ),
      ),
    );
  }
  void getNearbyPlaces() async{
    var url = Uri.parse('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + latitude.toString() + ','
        + longitude.toString() + '&radius=' + radius + '&keyword=skindoctor' + '&key=' + apiKey);
    var response = await http.post(url);

    nearbyPlacesResponse = NearbyPlacesResponse.fromJson(jsonDecode(response.body));
    setState(() {});
  }

  Widget nearbyPlacesWidget(Results results){
    return Container(
      width: MediaQuery.of(context).size.width,
      margin: const EdgeInsets.only(top: 10,left: 10,right: 10),
      padding: const EdgeInsets.all(5),
      decoration: BoxDecoration(border: Border.all(color: Colors.black),borderRadius: BorderRadius.circular(10)),
      child: Column(
        children: [
          Text("Name: " + results.name!),
          SizedBox(height: 5,),
          Text("Address: " + results.vicinity!),
          SizedBox(height: 5,),
          Text("Rating: " + results.rating!.toString()),
          SizedBox(height: 5,),
          Text(results.openingHours != null ? "Currently: Open" : "Currently: Closed"),
        ],
      ),
    );
}}
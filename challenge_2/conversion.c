#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tools.h"


int main(int argc , char *argv[]) {

    printf("Program name %s\n", argv[0]);

    if (argc == 2 && strcmp(argv[1], "--help") == 0){
        printf("The '%s' program works in two modes:\n"\
               "-  ./conversion g2r lon1 lat1 lon2 lat2  (where lon and lat are in decimal degrees)\n"\
               "-  ./conversion r2g bearing distance lon1 lat1 (where lon, lat and bearing are in decimal degrees and distance is in meters)\n"\
               "Mode 'g2r' handles the conversion from GIS to Radar coordinates.\n"\
               "Mode 'r2g' handles the conversion from Radar to GIS coordinates.\n", argv[0]);
        return 1;
    }

    if (argc != 6) {
        printf("ERROR: You need five arguments!\n");
        return 1;
    }

    if (strcmp(argv[1], "r2g") == 0){
        printf("Converting from Radar to GIS coordinates.\n");
        double distance, bearing, lon1, lat1, lon2, lat2;
        distance = atof(argv[2]);
        bearing = atof(argv[3]);
        lon1= atof(argv[4]);
        lat1 = atof(argv[5]);
        lon2 = 0.0;
        lat2 = 0.0;
        int status = Radar2GIS(distance, bearing, lon1, lat1, &lon2, &lat2);
        if (status == 0){
            printf("The longitude and latitude of the end point are respectively: %f° and %f°.\n",
                    lon2, lat2);
            return 0;
        }
    }
    else if (strcmp(argv[1], "g2r") == 0){
        printf("Converting from GIS to Radar coordinates.\n");
        double distance, bearing, lon1, lat1, lon2, lat2;
        lon1= atof(argv[2]);
        lat1 = atof(argv[3]);
        lon2= atof(argv[4]);
        lat2 = atof(argv[5]);
        distance = 0.0;
        bearing = 0.0;
        int status = GIS2Radar(lon1, lat1, lon2, lat2, &distance, &bearing);
        if (status == 0){
            printf("The initial bearing and great-circle distance between the two points "\
                   "are respectively: %f° and %fm.\n", bearing, distance);
            return 0;
        }
    }
    else{
        printf("ERROR: Invalid conversion type!\n");
        return 1;
    }



}


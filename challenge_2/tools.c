//
// Utility functions to convert from radar to GIS coordinates
// and vice versa.
//
// The formulas used in these functions are outlined and described
// in the following website:
// http://www.movable-type.co.uk/scripts/latlong.html
// All these formulas are valid on the basis of a spherical Earth.
//
//

#include <math.h>
#include <stdio.h>
#include "tools.h"

#define PI 3.14159265358979323846

// Radius of the Earth in meters.
const double earthRadiusInMeters = 6371000.0;

// Converts degrees to radians.
static double ConvertDegreesToRadians(double degrees){
    return degrees * PI / 180.0;
}

// Converts radians to degrees.
static double ConvertRadiansToDegrees(double radians){
    return radians * 180.0 / PI;
}

// Calculates the end point location given distance and bearing from starting point.
int Radar2GIS (double distance, double bearing, double lon1, double lat1, double *lon2, double *lat2){
   if (fabs(lon1) > 180){
       printf("ERROR: The longitude of the starting point should be between -180° and 180°!\n");
       return 1;
   }
    if (fabs(lat1) > 90){
        printf("ERROR: The latitude of the starting point should be between -90° and 90°!\n");
        return 1;
    }
   if (distance < 0){
       printf("ERROR: The distance between starting and end points should be positive!\n");
       return 1;
   }
   if (bearing < 0 || bearing > 360){
       printf("ERROR: The initial bearing should be between 0° and 360°!\n");
       return 1;
   }

   double latRad = ConvertDegreesToRadians(lat1);
   double lonRad = ConvertDegreesToRadians(lon1);
   double bearingRad = ConvertDegreesToRadians(bearing);
   double ang_dist = distance / earthRadiusInMeters;

   double latFinalRad = asin(sin(latRad) * cos(ang_dist) + cos(latRad) * sin(ang_dist) * cos(bearingRad));
   double val1 = sin(bearingRad) * sin(ang_dist) * cos(latRad);
   double val2 = cos(ang_dist) - sin(latRad) * sin(latFinalRad);
   double lonFinalRad = lonRad + atan2(val1, val2);

   *lat2 = ConvertRadiansToDegrees(latFinalRad);
   *lon2 = ConvertRadiansToDegrees(lonFinalRad);
   if (fabs(*lon2) > 180){
       printf("ERROR: Unexpected result for the longitude of the end point: %f!\n", *lon2);
       return 1;
   }
   if (fabs(*lat2) > 90){
       printf("ERROR: Unexpected result for the latitude of the end point: %f!\n", *lat2);
       return 1;
   }
    return 0;
}

// Calculates the great-circle distance between two points using the "haversine" formula.
double GetDistance(double lon1, double lat1, double lon2, double lat2){
    double lat1_rad = ConvertDegreesToRadians(lat1);
    double lon1_rad = ConvertDegreesToRadians(lon1);
    double lat2_rad = ConvertDegreesToRadians(lat2);
    double lon2_rad = ConvertDegreesToRadians(lon2);
    double diff_lat = lat2_rad - lat1_rad;
    double diff_lon = lon2_rad - lon1_rad;
    // Square of half the chord length between the points.
    double a = sin(diff_lat / 2.0) * sin(diff_lat / 2.0) + cos(lat1_rad) * cos(lat2_rad) * sin(diff_lon / 2.0) * sin(diff_lon / 2.0);
    // Angular distance in radians.
    double c = 2.0 * atan2(sqrt(a), sqrt(1.0 - a));
    double dist = earthRadiusInMeters * c;
    return dist;
}

// Calculates the initial bearing between two points.
double GetBearing(double lon1, double lat1, double lon2, double lat2){
    double lat1_rad = ConvertDegreesToRadians(lat1);
    double lon1_rad = ConvertDegreesToRadians(lon1);
    double lat2_rad = ConvertDegreesToRadians(lat2);
    double lon2_rad = ConvertDegreesToRadians(lon2);
    double diff_lon = lon2_rad - lon1_rad;
    double val1 = sin(diff_lon) * cos(lat2_rad);
    double val2 = cos(lat1_rad) * sin(lat2_rad) - sin(lat1_rad) * cos(lat2_rad) * cos(diff_lon);
    double theta = atan2(val1, val2);
    double bearing = fmod(ConvertRadiansToDegrees(theta) + 360.0, 360.0);
    return bearing;
}

// Calculates the initial bearing and distance between two points.
int GIS2Radar(double lon1, double lat1, double lon2, double lat2, double *distance, double *bearing){
    if (fabs(lon1) > 180){
        printf("ERROR: The longitude of the starting point should be between -180° and 180°!\n");
        return 1;
    }
    if (fabs(lat1) > 90){
        printf("ERROR: The latitude of the starting point should be between -90° and 90°!\n");
        return 1;
    }
    if (fabs(lon2) > 180){
        printf("ERROR: The longitude of the end point should be between -180° and 180°!\n");
        return 1;
    }
    if (fabs(lat2) > 90){
        printf("ERROR: The latitude of the end point should be between -90° and 90°!\n");
        return 1;
    }

    *distance = GetDistance(lon1, lat1, lon2, lat2);
    *bearing = GetBearing(lon1, lat1, lon2, lat2);

    if (*distance < 0){
        printf("ERROR: Unexpected result for the distance between the starting and end points: %f!\n", *distance);
        return 1;
    }
    if (*bearing < 0 || *bearing > 360){
        printf("ERROR: Unexpected result for the initial bearing: %f!\n", *bearing);
        return 1;
    }
    return 0;
}
//
// Header file: conversion.h
//

#ifndef CHALLENGE_2_TOOLS_H
#define CHALLENGE_2_TOOLS_H

/*!
 * Calculates the location of the end point given the initial bearing and distance.
 *
 *  @param distance distance between starting and end points, in meters
 *  @param bearing initial bearing, in decimal degrees
 *  @param lon1 longitude of the starting point, in decimal degrees
 *  @param lat1 latitude of the starting point, in decimal degrees
 *  @param lon2 longitude of the end point, in decimal degrees
 *  @param lat2 latitude of the end point, in decimal degrees
 *
 *  @return Status of the calculation
 */
int Radar2GIS (double distance, double bearing, double lon1, double lat1, double *lon2, double *lat2);

/*!
 *  Calculates the great-circle distance between two points.
 *
 *  @param lon1 longitude of the starting point, in decimal degrees
 *  @param lat1 latitude of the starting point, in decimal degrees
 *  @param lon2 longitude of the end point, in decimal degrees
 *  @param lat2 latitude of the end point, in decimal degrees
 *
 *  @return The distance in meters between the starting and end points.
 */
double GetDistance(double lon1, double lat1, double lon2, double lat2);

/*!
 *  Calculates the bearing at the starting point.
 *
 *  @param lon1 longitude of the starting point, in decimal degrees
 *  @param lat1 latitude of the starting point, in decimal degrees
 *  @param lon2 longitude of the end point, in decimal degrees
 *  @param lat2 latitude of the end point, in decimal degrees
 *
 *  @return The initial bearing in decimal degrees
 */
double GetBearing(double lon1, double lat1, double lon2, double lat2);

/*!
 * Calculates the initial bearing and great-circle distance between two points.
 *
 *  @param distance distance between starting and end points, in meters
 *  @param bearing initial bearing, in decimal degrees
 *  @param lon1 longitude of the starting point, in decimal degrees
 *  @param lat1 latitude of the starting point, in decimal degrees
 *  @param lon2 longitude of the end point, in decimal degrees
 *  @param lat2 latitude of the end point, in decimal degrees
 *
 *  @return Status of the calculation
 */
int GIS2Radar(double lon1, double lat1, double lon2, double lat2, double *distance, double *bearing);

#endif //CHALLENGE_2_TOOLS_H

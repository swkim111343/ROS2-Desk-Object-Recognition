# ROS2 Desk Object Recognition

## 1. Project Title

C++-Based ROS2 Desk Object Recognition and Database Management System Using YOLO and MediaPipe

## 2. Project Description

This project is a ROS2-based desk object recognition system implemented in C++.

A USB camera captures objects on a desk, and YOLO detects objects and their bounding boxes. MediaPipe Hands tracks hand landmarks and extracts fingertip coordinates.

When a user points at an object with their index finger, the system identifies the selected object by comparing the fingertip coordinates with the object's bounding box.

The selected object's information, including its name, confidence score, coordinates, and selection time, is automatically stored in an SQLite database.

## 3. Motivation

- To combine AI-based object detection with computer vision.
- To provide an intuitive object selection method using finger pointing.
- To learn and apply ROS2 node-based communication and system integration.
- To build a system that manages recognized object information using a database.

## 4. Technologies

- C++
- ROS2 Jazzy
- Ubuntu 24.04
- OpenCV
- YOLOv8n
- MediaPipe Hands
- SQLite
- CMake
- colcon

## 5. Main Features

1. USB camera image acquisition
2. Object detection using YOLO
3. Hand landmark detection using MediaPipe
4. Fingertip-based object selection
5. Object information storage in SQLite
6. ROS2-based modular communication

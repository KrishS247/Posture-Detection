
//Including the header files so the C++ can operate properly
#include <iostream>
#include <fstream>

using namespace std;

//Defining a class to encapsulate the detected landmarks
class Landmarks {
public:
    //Defining the variables for each of the detected landmarks
    double leftShoulderX, leftShoulderY, rightShoulderX, rightShoulderY,
           leftHipX, leftHipY, rightHipX, rightHipY;
};

int main() {
    //Opening the input and output .txt files so the C++ code can read/write them
    ifstream poseDataFile("pose_data.txt");
    ofstream resultFile("result.txt", ofstream::trunc);

    //Checking if the C++ has opended the files
    if (!poseDataFile.is_open() || !resultFile.is_open()) {
        //If the files are not opened it gives us an error
        cerr << "Error opening files." << endl;
        return 1;
    }

    //This creates an instance for the "Landmarks" class so it can store the landmark data
    Landmarks landmarks;

    //Reading the landmark data from the input .txt file and then input 
    //them into the class variables
    poseDataFile >> landmarks.leftShoulderX >> landmarks.leftShoulderY
                 >> landmarks.rightShoulderX >> landmarks.rightShoulderY
                 >> landmarks.leftHipX >> landmarks.leftHipY
                 >> landmarks.rightHipX >> landmarks.rightHipY;

    //Logic for checking if person has bad posture
    //Logic checks if horizontal position of hips and shoulders are aligned
    //The threshold is 0.1 for "Bad Posture"
    bool isBadPosture = (abs(landmarks.leftShoulderX - landmarks.leftHipX) > 0.1) ||
                        (abs(landmarks.rightShoulderX - landmarks.rightHipX) > 0.1);

    //Save the result of Bad/Good posture to the output .txt file
    resultFile << (isBadPosture ? "Bad Posture!" : "Good Posture!") << endl;

    //This closes the files that C++ is using
    poseDataFile.close();
    resultFile.close();

    return 0;
}

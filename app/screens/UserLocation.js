import React, { useEffect, useState } from 'react';
import { startCounter, stopCounter } from 'react-native-accurate-step-counter';
import { SafeAreaView, StyleSheet, Text, View, ImageBackground, TouchableOpacity, Image } from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import {AnimatedCircularProgress} from 'react-native-circular-progress';
var Icon = require('react-native-vector-icons/Ionicons');
import Colors from '../utils/colors';
import {COLORS, SIZES} from '../constants';

const tintColor = "#8BBF71";
const backgroundColor = "#717BA5";
const rotation = 360;

const UserLocation = ({route}) => {
  const [steps, setSteps] = useState(0);

  const [time, setTime] = useState({
    seconds: 0,
    minutes: 0,
    hours: 0,
  });


  const dayDim = {
    size: 300,
    width: 20,
    iconSize: 50
};


  function getToday(){
    let today = new Date()
    let dayIndex = today.getDay()
    let daysArray = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    let dayName = daysArray[dayIndex];
    let monthsArray = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    let month = today.getMonth();
    let monthName = monthsArray[month];
    let dd = String(today.getDate()).padStart(2, '0')
    var yyyy = today.getFullYear();
    return dayName+', '+ dd + ' '+monthName+' '+yyyy;
  }

  useEffect(() => {
    const config = {
      default_threshold: 15.0,
      default_delay: 150000000,
      cheatInterval: 3000,
      onStepCountChange: (stepCount) => { setSteps(stepCount) },
      onCheat: () => { console.log("User is Cheating") }
    }
    startCounter(config);
    return () => { stopCounter() }
  }, []);

  useEffect(() => {
    let isCancelled = false;

    const advanceTime = () => {
      setTimeout(() => {
        let nSeconds = time.seconds;
        let nMinutes = time.minutes;
        let nHours = time.hours;

        nSeconds++;

        if (nSeconds > 59) {
          nMinutes++;
          nSeconds = 0;
        }
        if (nMinutes > 59) {
          nHours++;
          nMinutes = 0;
        }
        if (nHours > 24) {
          nHours = 0;
        }

        !isCancelled && setTime({ seconds: nSeconds, minutes: nMinutes, hours: nHours });
      }, 1000);
    };
    advanceTime();

    return () => {
      //final time:
      console.log(time);
      isCancelled = true;
    };
  }, [time]);


  return (
    <View style={styles.container}>
    <ImageBackground source={require('../assets/images/walk2.png')} resizeMode="cover" style={styles.image}>
      <View style={styles.overlay}/>
        <View style={{flex:1,justifyContent:'center',alignItems:'center', alignSelf:'center'}}>
          <View style={styles.label}>
            <Text style={styles.labelText}> {getToday()}  </Text>
          </View>
          <AnimatedCircularProgress
                  size={dayDim.size}
                  width={dayDim.width}
                  fill={steps}
                  tintColor={tintColor}
                  backgroundColor={backgroundColor}
                  rotation={rotation}
              >
                  {
                      (fill) => (
                          <View style={styles.dayFill}>
                          
                              <Text style={styles.steps}>
                                  { steps } Steps
                              </Text>
                              <Text style={styles.goal}>
                                Goal: 10000
                              </Text>
                          </View>
                      )
                  }
            </AnimatedCircularProgress>
        </View>
        <View style={{flexDirection:'row', justifyContent:'center', alignItems:'center'}}>
            <TouchableOpacity
                activeOpacity={0.8}
                style={{
                  backgroundColor: COLORS.white,
                  width: 0.5 * SIZES.width - 35,
                  margin: 10,
                  height: 200,
                  borderRadius: 10,
                  padding: 15,
                  shadowColor: '#9e9898',
                  elevation: 5,
                  borderWidth: 0.5
                }}>
                <Image
                  source={require('../assets/images/calorie2.png')}
                  style={{
                    width: 150,
                    resizeMode: 'cover',
                    flex: 1,
                    justifyContent: 'center',
                    alignSelf: 'center'
                  }}
                />
                <Text style={{marginTop: 20, textAlign: 'center', fontSize: 35, fontWeight: 'bold', color: '#375A7F'}}>
                  {Math.round(0.04*steps,2)} KCal
                </Text>
          </TouchableOpacity>
          <TouchableOpacity
                activeOpacity={0.8}
                style={{
                  backgroundColor: COLORS.white,
                  width: 0.5 * SIZES.width - 35,
                  margin: 10,
                  height: 200,
                  borderRadius: 10,
                  padding: 15,
                  shadowColor: '#9e9898',
                  elevation: 5,
                  borderWidth: 0.5
                }}>
                <Image
                  source={require('../assets/images/clock.png')}
                  style={{
                    width: '70%',
                    resizeMode: 'contain',
                    flex: 1,
                    justifyContent: 'center',
                    alignSelf: 'center'
                  }}
                />
                <Text style={{marginTop: 20, textAlign: 'center', fontSize: 35, fontWeight: 'bold', color: '#375A7F'}}>
                  {time.hours}:{time.minutes}:{time.seconds}
                </Text>
          </TouchableOpacity>
        </View>

    </ImageBackground>
    </View>
  );
};

const styles = StyleSheet.create({
  overlay: {
    position: 'absolute',
    top: 0,
    right: 0,
    bottom: 0,
    left: 0,
    backgroundColor: '#fff',
    opacity: 0.6
  },
  container: {
    flex: 1,
    backgroundColor: 'transparent'
},
image: {
  flex: 1,
  justifyContent: "center"
},
  screen: {
    width: '100%',
    height: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  },
  step: {
    fontSize: 45,
    fontWeight: 'bold'
  },
  gradient: {
    flex: 1
  },
  day: {
    color: Colors.text_color,
    fontWeight: '800'
},
steps: {
    backgroundColor: 'transparent',
    fontSize: 40,
    textAlign: 'center',
    color: '#375A7F',
    fontWeight: 'bold'
},
goal: {
    color: '#375A7F',
    fontSize: 20,
    fontWeight: 'bold'
},
labelText: {
  color: '#375A7F',//Colors.text_color,
  fontSize: 20,
  fontWeight: 'bold'

},
label: {
  marginBottom: 30,
  borderRadius: 20,
  borderWidth: 4,
  borderColor: '#375A7F',
  paddingHorizontal: 40,
  height: 40,
  alignItems: 'center',
  justifyContent: 'center'
},
dayFill: {
  backgroundColor: 'transparent',
  position: 'absolute',
  top: 0,
  left: 0,
  alignItems: 'center',
  justifyContent: 'center',
  width: 250,
  height: 250
},
});

export default UserLocation;
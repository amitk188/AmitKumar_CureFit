import React from 'react';
import {
  View,
  Text,
  SafeAreaView,
  StatusBar,
  Image,
  TextInput,
  FlatList,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import FontAwesome5Icons from 'react-native-vector-icons/FontAwesome5';
import {COLORS, SIZES} from '../constants';

let exercises = [
  {
    title: 'Bicep Curls',
    image: require('../assets/images/img1.png'),
    subTitle:
      'Live happier and healthier by learning the fundamentals of diet recommendation',
    duration: '5-20 MIN Course',
  },
  {
    title: 'Squats',
    image: require('../assets/images/squat.png'),
    subTitle:
      'Live happier and healthier by learning the fundamentals of diet recommendation',
    duration: '5-20 MIN Course',
  },
  {
    title: 'Push ups',
    image: require('../assets/images/push_up.png'),
    subTitle: 'Live happier and healthier by learning the fundamentals of Yoga',
    duration: '5-10 MIN Course',
  },
  {
    title: 'Lunges',
    image: require('../assets/images/lunge_squat.png'),
    subTitle:
      'Live happier and healthier by learning the fundamentals of meditation and mindfulness',
    duration: '3-10 MIN Course',
  },
  {
    title: 'Pilates',
    image: require('../assets/images/pilates.png'),
    subTitle:
      'Live happier and healthier by learning the fundamentals of diet recommendation',
    duration: '5-20 MIN Course',
  },
  {
    title: 'Plank',
    image: require('../assets/images/plank.png'),
    subTitle:
      'Live happier and healthier by learning the fundamentals of kegel exercises',
    duration: '10-20 MIN Course',
  },
  {
    title: 'Crunch',
    image: require('../assets/images/crunch.png'),
    subTitle:
      'Live happier and healthier by learning the fundamentals of kegel exercises',
    duration: '10-20 MIN Course',
  },
  {
    title: 'Capture',
    image: require('../assets/images/Capture.png'),
    subTitle:
      'Live happier and healthier by learning the fundamentals of kegel exercises',
    duration: '10-20 MIN Course',
  }
];

const RepCounterScreen = ({navigation}) => {

  const ExerciseItem = ({exercise}) => {
    return (
      <TouchableOpacity
        onPress={() => {
        }
        }
        activeOpacity={0.8}
        style={{
          backgroundColor: COLORS.white,
          width: 0.5 * SIZES.width - 35,
          margin: 10,
          height: 180,
          borderRadius: 10,
          padding: 15,
          shadowColor: '#9e9898',
          elevation: 5,
          borderWidth: 0.5
        }}>
        <Image
          source={exercise.image}
          style={{
            width: '100%',
            resizeMode: 'contain',
            flex: 1,
          }}
        />
        <Text style={{marginTop: 20, textAlign: 'center', fontSize: 16, fontWeight:'bold'}}>
          {exercise.title}
        </Text>
      </TouchableOpacity>
    );
  };

  return (
    <SafeAreaView style={{flex: 1, position: 'relative'}}>
      <StatusBar
        backgroundColor={COLORS.accent + '30'}
        barStyle="dark-content"
        animated={true}
      />
      <ScrollView>      
       <View
        style={{
          width: '100%',
          height: 0.25 * SIZES.height,
          padding: 30,
          backgroundColor: '#C7B8F5',
          position: 'relative',
        }}>
        <Image
          source={require('../assets/images/BgPurple.png')}
          style={{
            position: 'absolute',
            top: 60,
            left: -50,
          }}
        />
        <Text style={{fontSize: 30, lineHeight: 45}}>Rep Counter</Text>
        <Text style={{fontSize: 16, opacity: 0.6, marginVertical: 10}}>
          Infinite
        </Text>
        <Text style={{fontSize: 16, width: '85%'}}>Let us count the repetitions while you focus on exercising</Text>
          <View
            style={{
              width: 60,
              height: 60,
              borderRadius: 30,
              backgroundColor: COLORS.accent + '55',
              position: 'absolute',
              right: -30,
              bottom: 50,
            }}></View>
        </View>

        <FlatList
          data={exercises}
          style={{
            paddingHorizontal: 20,
            marginTop: 5,
          }}
          contentContainerStyle={{
            flex: 1,
            alignItems: 'center',
          }}
          showsVerticalScrollIndicator={false}
          numColumns={2}
          keyExtractor={item => item.title}
          renderItem={({item}) => <ExerciseItem exercise={item} />}
        />
      </ScrollView>
    </SafeAreaView>
  );
};

export default RepCounterScreen;
